
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "conversation_memory.db"

KNOWN_DESTINATIONS = [
    "Goa",
    "Hampi",
    "Jaipur",
    "Kerala",
    "Manali",
    "Pondicherry",
    "Udaipur",
]


class ConversationMemory:

    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_database(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_sessions (
                    session_id TEXT PRIMARY KEY,
                    profile_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(session_id)
                        REFERENCES conversation_sessions(session_id)
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session
                ON conversation_messages(session_id, id)
            """)

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat()

    def get_profile(self, session_id):
        with self._connect() as conn:
            row = conn.execute("""
                SELECT profile_json
                FROM conversation_sessions
                WHERE session_id = ?
            """, (session_id,)).fetchone()

        if not row:
            return {}

        try:
            return json.loads(row["profile_json"])
        except (json.JSONDecodeError, TypeError):
            return {}

    def extract_profile(self, message):
        """
        Extract trip details explicitly mentioned
        in the latest user message.
        """
        profile = {}
        text = message.lower()

        # Destination
        for destination in KNOWN_DESTINATIONS:
            if re.search(
                rf"\b{re.escape(destination.lower())}\b",
                text
            ):
                profile["destination"] = destination
                break

        # Group size
        patterns = [
            r"\b(\d+)\s+(?:friends|people|persons|travellers|travelers)\b",
            r"\b(?:we are|we're|group of)\s+(\d+)\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                profile["friends"] = int(match.group(1))
                break

        # Nights
        match = re.search(r"\b(\d+)\s*nights?\b", text)
        if match:
            profile["nights"] = int(match.group(1))

        # Budget per person
        budget_patterns = [
            r"(?:₹|rs\.?\s*)([\d,]+)\s*(?:each|per person|/person)?",
            r"\b([\d,]+)\s*(?:rupees|inr)\s*(?:each|per person)?",
        ]

        for pattern in budget_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    profile["budget_per_person"] = float(
                        match.group(1).replace(",", "")
                    )
                    break
                except ValueError:
                    pass

        # Month
        months = [
            "january", "february", "march", "april",
            "may", "june", "july", "august",
            "september", "october", "november", "december"
        ]

        for month in months:
            if re.search(rf"\b{month}\b", text):
                profile["travel_month"] = month.title()
                break

        # Travel preferences
        preference_keywords = [
            "adventure", "beach", "nature", "heritage",
            "relaxation", "budget", "luxury", "family"
        ]

        preferences = [
            item for item in preference_keywords
            if re.search(rf"\b{item}\b", text)
        ]

        if preferences:
            profile["preferences"] = preferences

        return profile

    def update_profile(self, session_id, new_profile):
        now = self._now()

        with self._connect() as conn:
            row = conn.execute("""
                SELECT profile_json
                FROM conversation_sessions
                WHERE session_id = ?
            """, (session_id,)).fetchone()

            if row:
                try:
                    profile = json.loads(row["profile_json"])
                except (json.JSONDecodeError, TypeError):
                    profile = {}
            else:
                profile = {}

            # Update only fields explicitly extracted.
            profile.update(new_profile)

            conn.execute("""
                INSERT INTO conversation_sessions (
                    session_id, profile_json, created_at, updated_at
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    profile_json = excluded.profile_json,
                    updated_at = excluded.updated_at
            """, (
                session_id,
                json.dumps(profile),
                now,
                now
            ))

        return profile

    def save_message(self, session_id, role, content):
        now = self._now()

        with self._connect() as conn:
            conn.execute("""
                INSERT INTO conversation_sessions (
                    session_id, profile_json, created_at, updated_at
                )
                VALUES (?, '{}', ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    updated_at = excluded.updated_at
            """, (session_id, now, now))

            conn.execute("""
                INSERT INTO conversation_messages (
                    session_id, role, content, created_at
                )
                VALUES (?, ?, ?, ?)
            """, (session_id, role, content, now))

    def get_recent_messages(self, session_id, limit=10):
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT role, content
                FROM conversation_messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
            """, (session_id, limit)).fetchall()

        return [
            {"role": row["role"], "content": row["content"]}
            for row in reversed(rows)
        ]

    def build_context(self, session_id, current_message):
        profile = self.get_profile(session_id)
        recent_messages = self.get_recent_messages(
            session_id,
            limit=8
        )

        context = []

        if profile:
            context.append("KNOWN TRIP DETAILS:")

            for key, value in profile.items():
                context.append(f"- {key}: {value}")

        if recent_messages:
            context.append("\nRECENT CONVERSATION:")

            for item in recent_messages:
                context.append(
                    f"{item['role'].upper()}: {item['content']}"
                )

        context.append("\nCURRENT USER REQUEST:")
        context.append(current_message)

        context.append(
            "\nUse the known trip details and recent conversation "
            "to understand follow-up questions. Preserve existing "
            "details unless the user explicitly changes them. "
            "Do not invent missing details."
        )

        return "\n".join(context)

    def clear_session(self, session_id):
        with self._connect() as conn:
            conn.execute("""
                DELETE FROM conversation_messages
                WHERE session_id = ?
            """, (session_id,))

            conn.execute("""
                DELETE FROM conversation_sessions
                WHERE session_id = ?
            """, (session_id,))
