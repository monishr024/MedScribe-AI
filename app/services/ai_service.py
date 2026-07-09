import time

from google import genai

from app.config import Config


class AIService:

    def __init__(self):

        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

    def generate_report(self, prompt: str) -> str:

        MODELS = [

            "gemini-3.5-flash",

            "gemini-3.1-flash-lite",

            "gemini-3.1-flash-lite-preview"

        ]

        MAX_RETRIES = 3

        last_error = None

        for model in MODELS:

            print("=" * 60)
            print(f"Trying Model: {model}")
            print("=" * 60)

            for attempt in range(MAX_RETRIES):

                try:

                    response = self.client.models.generate_content(

                        model=model,

                        contents=prompt

                    )

                    if not response:
                        raise Exception("No response received from Gemini.")

                    if not hasattr(response, "text"):
                        raise Exception("Gemini response has no text.")

                    if response.text is None or response.text.strip() == "":
                        raise Exception("Gemini returned an empty response.")

                    print(f"SUCCESS using {model}")

                    return response.text.strip()

                except Exception as e:

                    last_error = e

                    error = str(e)

                    print(f"Attempt {attempt+1} failed")

                    print(error)

                    # Retry only for temporary server errors
                    if (
                        "503" in error or
                        "UNAVAILABLE" in error or
                        "429" in error or
                        "RESOURCE_EXHAUSTED" in error
                    ):

                        if attempt < MAX_RETRIES - 1:

                            wait = 2 ** attempt

                            print(f"Retrying in {wait} seconds...")

                            time.sleep(wait)

                            continue

                    break

        raise Exception(f"Gemini API Error:\n\n{last_error}")