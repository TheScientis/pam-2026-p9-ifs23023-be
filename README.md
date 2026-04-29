# 🚀 AI Motivation API - Backend Flask

Backend untuk aplikasi AI Motivation berbasis Flutter. Menggunakan **Gemini API** untuk generate kata-kata motivasi.

---

## 📁 Struktur Proyek

```
ai_motivation_be/
├── app/
│   ├── __init__.py             # App factory (create_app)
│   ├── config.py               # Konfigurasi & env variables
│   ├── extensions.py           # SQLAlchemy instance
│   ├── middleware/
│   │   └── auth_middleware.py  # JWT token guard
│   ├── models/
│   │   ├── user.py             # Model User
│   │   ├── motivation.py       # Model Motivation
│   │   └── request_log.py      # Model log permintaan
│   ├── routes/
│   │   ├── auth_routes.py      # Endpoint auth (login, register, verify)
│   │   └── motivation_routes.py# Endpoint motivasi (CRUD + generate)
│   ├── services/
│   │   ├── llm_service.py      # Koneksi ke Gemini API
│   │   └── motivation_service.py # Logika bisnis motivasi
│   └── utils/
│       └── parser.py           # Parser JSON response LLM
├── .env                        # Environment variables (API Key dll)
├── requirements.txt
├── run.py                      # Entry point
└── api_test.http               # REST Client untuk testing
```

---

## ⚙️ Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Konfigurasi `.env`
```env
SECRET_KEY=motivation-app-secret-key
DATABASE_URL=sqlite:///motivation.db
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
APP_PORT=5000
```

### 3. Jalankan Server
```bash
python run.py
```

Server berjalan di: `http://127.0.0.1:5000`

> **Akun default:** `username=admin`, `password=motivation123`

---

## 📡 Daftar Endpoint

### Auth
| Method | Endpoint | Auth | Deskripsi |
|--------|----------|------|-----------|
| POST | `/auth/register` | ❌ | Daftar akun baru |
| POST | `/auth/login` | ❌ | Login & dapat token JWT |
| GET | `/auth/verify` | ✅ | Verifikasi token |

### Motivation
| Method | Endpoint | Auth | Deskripsi |
|--------|----------|------|-----------|
| GET | `/` | ❌ | Cek status API |
| POST | `/motivations/generate` | ✅ | Generate motivasi via Gemini |
| GET | `/motivations` | ✅ | Ambil semua motivasi (paginasi) |
| GET | `/motivations/<id>` | ✅ | Ambil motivasi by ID |
| DELETE | `/motivations/<id>` | ✅ | Hapus motivasi |

### Query Params untuk GET `/motivations`
- `page` (default: 1)
- `per_page` (default: 10, max: 50)
- `category` (opsional, filter by tema)

---

## 🔐 Autentikasi

Semua endpoint yang memerlukan auth harus menyertakan header:
```
Authorization: Bearer <token_jwt>
```

Token berlaku selama **24 jam**.

---

## 📤 Contoh Request & Response

### Generate Motivasi
**Request:**
```json
POST /motivations/generate
{
  "theme": "semangat belajar",
  "total": 3
}
```

**Response:**
```json
{
  "message": "Berhasil generate 3 motivasi",
  "theme": "semangat belajar",
  "total": 3,
  "data": [
    "Setiap buku yang kamu buka adalah pintu menuju versi terbaik dirimu.",
    "Belajar mungkin terasa berat hari ini, tapi hasilnya akan kamu nikmati seumur hidup.",
    "Konsistensi kecil setiap hari akan menghasilkan perubahan besar di masa depan."
  ]
}
```
