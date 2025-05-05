from openai import OpenAI

api_key = "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"  # Replace with your Perplexity API key
client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Give concise and accurate answers."},
        {"role": "user", "content": "How to treat a lung cancer"}
    ]
)

print(response.choices[0].message.content)
