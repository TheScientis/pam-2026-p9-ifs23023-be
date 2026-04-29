from app.extensions import db
from app.models.motivation import Motivation
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_motivations(theme: str, total: int, user_id: int = None):
    """
    Generate kata-kata motivasi menggunakan Gemini AI
    berdasarkan tema yang diberikan, lalu simpan ke database.
    """
    try:
        prompt = f"""
        Kamu adalah seorang motivator handal dan inspiratif.
        Dalam format JSON, berikan {total} kata-kata motivasi yang bertemakan "{theme}".

        Setiap motivasi harus:
        - Membangkitkan semangat dan menginspirasi pembaca
        - Relevan dengan tema "{theme}"
        - Menggunakan bahasa Indonesia yang natural dan mudah dipahami
        - Singkat, padat, namun bermakna dalam (1-3 kalimat)

        WAJIB gunakan struktur JSON murni seperti di bawah ini tanpa tambahan teks apapun:
        {{
            "motivations": [
                {{"text": "kata motivasi 1 yang inspiratif"}},
                {{"text": "kata motivasi 2 yang inspiratif"}}
            ]
        }}
        """

        # Kirim prompt ke Gemini
        result = generate_from_llm(prompt)

        # Ambil string response dari dict
        if isinstance(result, dict):
            raw_response = result.get("response", "")
        else:
            raw_response = result

        # Parse JSON response menjadi list Python
        motivations = parse_llm_response(raw_response)

        # Simpan log permintaan ke database
        req_log = RequestLog(theme=theme, user_id=user_id)
        db.session.add(req_log)
        db.session.flush()

        saved_texts = []
        for item in motivations:
            text = item.get("text")
            new_m = Motivation(text=text, category=theme, request_id=req_log.id)
            db.session.add(new_m)
            saved_texts.append(text)

        db.session.commit()
        return saved_texts

    except Exception as e:
        db.session.rollback()
        print(f"Error di create_motivations: {e}")
        raise e


def get_all_motivations(page: int = 1, per_page: int = 10, category: str = None):
    """
    Ambil daftar motivasi dari database dengan pagination.
    Bisa difilter berdasarkan kategori/tema.
    """
    try:
        query = Motivation.query

        # Filter berdasarkan kategori jika diberikan
        if category:
            query = query.filter(Motivation.category.ilike(f"%{category}%"))

        total = query.count()
        total_pages = (total + per_page - 1) // per_page

        data = (
            query
            .order_by(Motivation.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": m.id,
                "text": m.text,
                "category": m.category,
                "created_at": m.created_at.isoformat() if m.created_at else None
            }
            for m in data
        ]

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "data": result
        }

    except Exception as e:
        print(f"Error di get_all_motivations: {e}")
        raise e


def get_motivation_by_id(motivation_id: int):
    """Ambil satu motivasi berdasarkan ID."""
    try:
        m = Motivation.query.get(motivation_id)
        if not m:
            return None
        return {
            "id": m.id,
            "text": m.text,
            "category": m.category,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
    except Exception as e:
        print(f"Error di get_motivation_by_id: {e}")
        raise e


def delete_motivation(motivation_id: int):
    """Hapus motivasi berdasarkan ID."""
    try:
        m = Motivation.query.get(motivation_id)
        if not m:
            return False
        db.session.delete(m)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error di delete_motivation: {e}")
        raise e
