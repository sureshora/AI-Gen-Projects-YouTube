from openai import OpenAI

client = OpenAI()

prompt = """
Classify the following customer message
as Positive, Negative, or Neutral.

Message:
"The product arrived early and works perfectly."
"""

response = client.responses.create(
    model="gpt-5.6",
    input=prompt,
)

print("Customer Message:")
print("The product arrived early and works perfectly.")
print("\nAI Classification:")
print(response.output_text)
