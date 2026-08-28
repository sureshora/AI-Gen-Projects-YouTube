from openai import OpenAI

client = OpenAI()

prompt = """
Classify customer messages as Positive or Negative.

Example:
Message: "The app is amazing!"
Classification: Positive

Now classify:

Message: "The app keeps crashing."
"""

response = client.responses.create(
    model="gpt-5.6",
    input=prompt,
)

print("AI Classification:")
print(response.output_text)
