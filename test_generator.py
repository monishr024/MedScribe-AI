from google import genai
from app.config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

models = [
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.5-flash"
]

for model in models:
    try:
        print(f"\nTesting: {model}")

        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: Hello"
        )

        print("SUCCESS:", response.text)

    except Exception as e:
        print("FAILED:", e)