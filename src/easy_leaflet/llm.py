from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

# The worker that talks to the LLM
class LLMClient:

    def __init__(self, model="gemini-3.5-flash-lite"):
        # Read the .env file, so the library can find GEMINI_API_KEY
        load_dotenv()
        self.model = model
        # Stop waiting after 60 seconds, so the app never hangs
        self.client = genai.Client(http_options=types.HttpOptions(timeout=60000))

  
    def ask(self, prompt, retries=3, wait_seconds=10):
        # Send the prompt to the LLM and return the answer as text.
        # If the API fails (timeout, error 503), wait and try again.
        for attempt in range(1, retries + 1):
            try:
                interaction = self.client.interactions.create(
                    model=self.model,
                    input=prompt,
                )
                return interaction.output_text
            except Exception as error:
                if attempt == retries:
                    raise
                print(f"   LLM error (attempt {attempt} of {retries}): {error}")
                print(f"   Waiting {wait_seconds} seconds before trying again...")
                time.sleep(wait_seconds)