
import tempfile
import unittest
from pathlib import Path

from agents.conversation_memory import ConversationMemory


class TestConversationMemory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        db_path = Path(self.temp_dir.name) / "test_memory.db"

        self.memory = ConversationMemory(db_path)
        self.session_id = "test-session-001"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_extract_trip_details(self):
        profile = self.memory.extract_profile(
            "We are 4 friends planning Goa for 3 nights "
            "with ₹12,000 each in July"
        )

        self.assertEqual(profile["destination"], "Goa")
        self.assertEqual(profile["friends"], 4)
        self.assertEqual(profile["nights"], 3)
        self.assertEqual(profile["budget_per_person"], 12000)
        self.assertEqual(profile["travel_month"], "July")

    def test_profile_merge(self):
        first = self.memory.extract_profile(
            "Plan Goa for 4 friends, 3 nights"
        )

        self.memory.update_profile(self.session_id, first)

        second = self.memory.extract_profile(
            "Make it 4 nights"
        )

        profile = self.memory.update_profile(
            self.session_id,
            second
        )

        self.assertEqual(profile["destination"], "Goa")
        self.assertEqual(profile["friends"], 4)
        self.assertEqual(profile["nights"], 4)

    def test_message_persistence(self):
        self.memory.save_message(
            self.session_id,
            "user",
            "Plan a Goa trip"
        )

        self.memory.save_message(
            self.session_id,
            "assistant",
            "Sure, how many nights?"
        )

        messages = self.memory.get_recent_messages(
            self.session_id
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]["role"], "assistant")

    def test_followup_context(self):
        profile = self.memory.extract_profile(
            "Goa for 4 friends, 3 nights, ₹12000 each"
        )

        self.memory.update_profile(
            self.session_id,
            profile
        )

        self.memory.save_message(
            self.session_id,
            "user",
            "Plan Goa for 4 friends"
        )

        context = self.memory.build_context(
            self.session_id,
            "Make it cheaper"
        )

        self.assertIn("Goa", context)
        self.assertIn("friends: 4", context)
        self.assertIn("Make it cheaper", context)

    def test_clear_session(self):
        self.memory.save_message(
            self.session_id,
            "user",
            "Hello"
        )

        self.memory.clear_session(self.session_id)

        self.assertEqual(
            self.memory.get_profile(self.session_id),
            {}
        )

        self.assertEqual(
            self.memory.get_recent_messages(self.session_id),
            []
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
