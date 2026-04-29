import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_from_llm(prompt: str):
    """
    Mengirim prompt ke Gemini API dan mengembalikan respons teks.
    API Key dibaca dari environment variable GEMINI_API_KEY.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY tidak ditemukan di environment variables")

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw_text = response.text

        # Bersihkan markdown code block jika ada
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1)
            raw_text = raw_text.replace("```", "")
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "")

        raw_text = raw_text.strip()

        return {"response": raw_text}

    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")
