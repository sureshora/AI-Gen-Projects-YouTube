from openai import OpenAI

client = OpenAI()

prompt = """
Classify each message as Positive, Negative, or Neutral.

Example 1:
Message: "I love this product."
Classification: Positive

Example 2:
Message: "This product is terrible."
Classification: Negative

Example 3:
Message: "The package arrived today."
Classification: Neutral

Now classify:

Message: "The quality is excellent!"
"""

response = client.responses.create(
    model="gpt-5.6",
    input=prompt,
)

print("AI Classification:")
print(response.output_text)
