
import uuid
import os
import gradio as gr

from agents.travel_agent import TravelAgent
from agents.conversation_memory import ConversationMemory
from database.db_connection import init_db, seed_db


# ============================================================
# 1. INITIALIZE APPLICATION
# ============================================================

print("Initializing Trip Buddy...")

init_db()
seed_db()

agent = TravelAgent()
memory = ConversationMemory()

print("Database initialized successfully!")


# ============================================================
# 2. CUSTOM CSS
# ============================================================

CUSTOM_CSS = """
:root {
    --trip-primary: #0d9488;
    --trip-primary-dark: #0f766e;
    --trip-bg: #f5f8fa;
}

.gradio-container {
    max-width: 1450px !important;
    margin: auto !important;
    background: var(--trip-bg) !important;
}

#trip-header {
    background: linear-gradient(120deg, #134e4a, #0d9488);
    color: white;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 18px;
}

#trip-header h1 {
    color: white !important;
    font-size: 34px !important;
    margin-bottom: 8px;
}

#trip-header p {
    color: #d9fffa !important;
}

#sidebar {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 18px;
}

#chat-panel {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 12px;
}

#chatbot {
    border: none !important;
    border-radius: 14px !important;
}

#message-box textarea {
    border-radius: 14px !important;
    padding: 14px !important;
}

.primary-action {
    background: #0d9488 !important;
    color: white !important;
    border: none !important;
}

.primary-action:hover {
    background: #0f766e !important;
}

.quick-button {
    border-radius: 12px !important;
    text-align: left !important;
    white-space: normal !important;
}

.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 16px;
}

.status-card {
    background: #f0fdfa;
    border: 1px solid #ccfbf1;
    border-radius: 12px;
    padding: 12px;
}

@media (max-width: 768px) {
    #trip-header {
        padding: 20px;
    }

    #trip-header h1 {
        font-size: 26px !important;
    }
}
"""


# ============================================================
# 3. CHAT RESPONSE HANDLER WITH MEMORY
# ============================================================

def respond(message, history, session_id):

    history = list(history or [])

    if not message or not message.strip():
        return history, "", session_id

    message = message.strip()

    # Ensure a session ID exists.
    if not session_id:
        session_id = str(uuid.uuid4())

    try:
        print(f"Session: {session_id}")
        print(f"User question: {message}")

        # Step 1: Extract new trip details.
        new_profile = memory.extract_profile(message)

        # Step 2: Merge with previously saved trip details.
        profile = memory.update_profile(
            session_id,
            new_profile
        )

        # Step 3: Build context from previous conversation.
        context_prompt = memory.build_context(
            session_id,
            message
        )

        # Step 4: Save current user message.
        memory.save_message(
            session_id,
            "user",
            message
        )

        # Step 5: Call existing MCP-enabled TravelAgent.
        answer = agent.ask(context_prompt)

        if not isinstance(answer, str):
            answer = str(answer)

        # Step 6: Save assistant response.
        memory.save_message(
            session_id,
            "assistant",
            answer
        )

        print("Memory updated successfully.")

    except Exception as exc:

        print(
            f"Application error: "
            f"{type(exc).__name__}: {exc}"
        )

        answer = (
            "Sorry, I encountered an issue while planning "
            "your trip.\n\n"
            f"Error: {type(exc).__name__}: {exc}"
        )

    history.append({
        "role": "user",
        "content": message
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    return history, "", session_id


# ============================================================
# 4. CLEAR CHAT AND MEMORY
# ============================================================

def clear_chat(session_id):

    if session_id:
        memory.clear_session(session_id)

    print("Conversation and memory cleared.")

    return [], "", session_id


# ============================================================
# 5. QUICK PROMPT HANDLER
# ============================================================

def quick_prompt(prompt, history, session_id):
    return respond(prompt, history, session_id)


# ============================================================
# 6. BUILD GRADIO APPLICATION
# ============================================================

with gr.Blocks(
    title="Trip Buddy | AI Travel Planner",
    css=CUSTOM_CSS
) as demo:

    # One unique session identifier per browser session.
    session_state = gr.State(
        value=lambda: str(uuid.uuid4())
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    gr.HTML("""
        <div id="trip-header">
            <h1>✈️ Trip Buddy</h1>
            <p>
                Your AI-powered travel companion.
                Discover destinations, calculate group budgets,
                and get smarter travel recommendations.
            </p>
        </div>
    """)

    with gr.Row(equal_height=False):

        # ====================================================
        # LEFT SIDEBAR
        # ====================================================

        with gr.Column(
            scale=1,
            min_width=260,
            elem_id="sidebar"
        ):

            gr.Markdown("## 🧭 Explore Trip Buddy")

            gr.Markdown(
                "Plan your next adventure with your friends."
            )

            gr.Markdown("### ⚡ Quick actions")

            btn_list = gr.Button(
                "📍 Explore destinations",
                elem_classes=["quick-button"]
            )

            btn_goa = gr.Button(
                "🏖️ Plan a Goa trip",
                elem_classes=["quick-button"]
            )

            btn_manali = gr.Button(
                "🏔️ Manali seasonal advice",
                elem_classes=["quick-button"]
            )

            btn_hampi = gr.Button(
                "🏛️ Calculate Hampi budget",
                elem_classes=["quick-button"]
            )

            btn_budget = gr.Button(
                "💰 Find trips within budget",
                elem_classes=["quick-button"]
            )

            gr.Markdown("---")

            gr.Markdown("### 🛠️ What I can do")

            gr.Markdown("""
            - 📍 Discover destinations
            - 💰 Calculate trip costs
            - 👥 Plan group travel
            - 🧠 Remember previous conversations
            - 🌦️ Provide seasonal guidance
            - 📚 Retrieve travel knowledge
            """)

            gr.Markdown("---")

            gr.Markdown("### 🧠 Conversation Memory")

            gr.HTML("""
                <div class="status-card">
                    <p>🟢 Session memory enabled</p>
                    <p>🟢 SQLite persistence enabled</p>
                    <p>🟢 Context retrieval enabled</p>
                </div>
            """)

            gr.Markdown("""
                <div class="footer-note">
                    Demo estimates only. Not live travel quotes.
                </div>
            """)

        # ====================================================
        # RIGHT CHAT PANEL
        # ====================================================

        with gr.Column(
            scale=3,
            min_width=320,
            elem_id="chat-panel"
        ):

            with gr.Row():

                gr.Markdown("## 💬 Travel Assistant")

                clear_btn = gr.Button(
                    "🗑️ Clear chat and memory",
                    size="sm",
                    variant="secondary"
                )

            chatbot = gr.Chatbot(
                height=520,
                show_label=False,
                placeholder=(
                    "👋 Welcome to Trip Buddy!\n\n"
                    "Tell me where you want to travel, "
                    "your budget and how many friends are joining."
                ),
                elem_id="chatbot"
            )

            # ------------------------------------------------
            # INPUT AREA
            # ------------------------------------------------

            with gr.Row():

                msg = gr.Textbox(
                    placeholder=(
                        "Ask me anything... e.g. "
                        "Plan Goa for 4 friends, 3 nights"
                    ),
                    show_label=False,
                    lines=2,
                    max_lines=5,
                    scale=8,
                    elem_id="message-box"
                )

                send_btn = gr.Button(
                    "➤ Send",
                    variant="primary",
                    scale=1,
                    elem_classes=["primary-action"]
                )

            gr.Markdown("""
                <div class="footer-note">
                    Trip Buddy remembers trip details during your
                    session. Verify live prices and conditions
                    before booking.
                </div>
            """)

    # ========================================================
    # 7. EVENT HANDLERS
    # ========================================================

    # Enter key
    msg.submit(
        fn=respond,
        inputs=[msg, chatbot, session_state],
        outputs=[chatbot, msg, session_state]
    )

    # Send button
    send_btn.click(
        fn=respond,
        inputs=[msg, chatbot, session_state],
        outputs=[chatbot, msg, session_state]
    )

    # Quick prompts
    quick_prompts = [
        (
            btn_list,
            "List destinations"
        ),
        (
            btn_goa,
            "We are 4 friends with ₹12,000 each. "
            "Can we do Goa for 3 nights?"
        ),
        (
            btn_manali,
            "Is Manali a good idea in July?"
        ),
        (
            btn_hampi,
            "How much is Hampi for 5 friends, 2 nights?"
        ),
        (
            btn_budget,
            "Which trips fit ₹8,000 each for "
            "3 friends, 2 nights?"
        )
    ]

    for button, prompt in quick_prompts:

        button.click(
            fn=quick_prompt,
            inputs=[
                gr.State(value=prompt),
                chatbot,
                session_state
            ],
            outputs=[
                chatbot,
                msg,
                session_state
            ]
        )

    # Clear conversation and saved memory
    clear_btn.click(
        fn=clear_chat,
        inputs=[session_state],
        outputs=[chatbot, msg, session_state],
        queue=False
    )


# ============================================================
# 8. LAUNCH APPLICATION
# ============================================================

if __name__ == "__main__":

    print("\nStarting Trip Buddy AI Travel Planner...")

    # demo.queue().launch(
    #     server_name="127.0.0.1",
    #     server_port=7860,
    #     theme=gr.themes.Soft(),
    #     show_error=True
    # )
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
        show_error=True
    )
