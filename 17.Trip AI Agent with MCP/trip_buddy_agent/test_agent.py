
from agents.travel_agent import TravelAgent

agent = TravelAgent()

test_questions = [
    "List destinations",
    "We are 4 friends with ₹12,000 each. Can we do Goa for 3 nights?",
    "Is Manali a good idea in July?",
    "Which trips fit ₹8,000 each for 3 friends, 2 nights?"
]

for index, question in enumerate(test_questions, start=1):

    print("\n" + "=" * 70)
    print(f"TEST {index}")
    print("QUESTION:", question)
    print("=" * 70)

    answer = agent.ask(question)

    print("\nANSWER:")
    print(answer)

print("\nAll tests completed.")
