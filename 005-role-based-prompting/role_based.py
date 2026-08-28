from openai import OpenAI

client = OpenAI()

prompt = """
You are a senior software architect.

Explain how to design a scalable
AI-powered SaaS application.

Keep the explanation practical
and beginner-friendly.
"""

response = client.responses.create(
    model="gpt-5.6",
    input=prompt,
)

print("AI Response:")
print(response.output_text)
