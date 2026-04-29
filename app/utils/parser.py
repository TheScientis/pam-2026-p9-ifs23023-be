import json
import re

def parse_llm_response(content):
    """
    Parse respons JSON dari Gemini LLM menjadi list motivasi.
    Menangani berbagai format output yang mungkin dikembalikan model.
    """
    try:
        # Pastikan content adalah string
        if isinstance(content, dict):
            content = content.get("response", "")

        # Hapus markdown code block jika masih ada
        content = re.sub(r"```json\s*|\s*```", "", content)
        content = content.strip()

        parsed = json.loads(content)
        return parsed.get("motivations", [])

    except json.JSONDecodeError as e:
        raise Exception(f"Gagal parsing JSON dari LLM: {str(e)} | Content: {content[:200]}")
    except Exception as e:
        raise Exception(f"Error saat parsing respons LLM: {str(e)}")
