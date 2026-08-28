from openai import OpenAI

client = OpenAI()

prompts = [
    "Explain Artificial Intelligence in simple words.",
    "Explain Python programming to a complete beginner.",
    "Give me 5 practical ways AI can help a small business.",
    "Create a simple 3-day travel itinerary for Chennai.",
]

for prompt in prompts:
    response = client.responses.create(
        model="gpt-5.6",
        input=prompt,
    )

    print("\nPROMPT:", prompt)
    print("AI:", response.output_text)
