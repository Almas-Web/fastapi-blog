# 🚀 FastAPI Blog API

A scalable and modular Blog API built with **FastAPI**, **SQLAlchemy**, and **Pydantic**, following a clean **Repository Pattern Architecture**.

---

## ✨ Features

- 👤 User registration and management
- 📝 Create, update, and delete blog posts
- 📄 Get all blogs with pagination support
- 🔍 Get single blog by ID
- 🔗 ORM relationships (User → Blogs)
- 🔥 Auto slug generation for blogs
- 🏗️ Clean repository-based architecture
- ✅ Pydantic validation (v1)

---

## 🛠️ Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic v1
- Uvicorn
- Python 3.11+

---

## 📁 Project Structure

```text
fastapi_blog/
│
├── apis/
│   └── v1/
│       ├── user.py
│       └── blog.py
│
├── repositories/
│   ├── user.py
│   └── blog.py
│
├── schemas/
│   ├── user.py
│   └── blog.py
│
├── db/
│   ├── models/
│   ├── session.py
│   └── base_class.py
│
├── core/
│   └── config.py
│
├── main.py
└── requirements.txt
```

---

## 🚀 How to Run

### 1️⃣ Clone repo
```bash
git clone https://github.com/your-username/fastapi-blog.git
cd fastapi-blog
```

### 2️⃣ Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run server
```bash
uvicorn main:app --reload
```

---

## 📌 API Endpoints

### 👤 Users
- `POST /users` → Create user

### 📝 Blogs
- `POST /blogs` → Create blog
- `GET /blogs` → Get all blogs
- `GET /blogs/{id}` → Get single blog
- `PUT /blogs/{id}` → Update blog

---

## 📖 Example Response

```json
{
  "id": 1,
  "content": "My first blog",
  "slug": "fastapi-blog-12345",
  "created_at": "2026-04-23T10:00:00",
  "author": {
    "id": 1,
    "email": "user@gmail.com",
    "is_active": true
  }
}
```

---

## 👨‍💻 Author

- Name: Almas Hossen  
- Role: Backend Developer (FastAPI)