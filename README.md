<div align="center">

  
# 🌸 Her-Flowmate Backend API

*The robust, high-performance backend powering the Her-Flowmate open-source mobile application.*

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 📖 Overview

This repository contains the backend services for **Her-Flowmate**. Built with modern Python web frameworks, it is designed to be blazingly fast, secure, and highly scalable to handle mobile client requests efficiently. 

The architecture strictly separates concerns, utilizing relational database modeling and secure third-party authentication flows to provide a seamless user experience.

## ✨ Key Features

* ⚡ **High Performance:** Asynchronous request handling powered by **FastAPI**.
* 🔐 **Authentication & Security:** Integrated **Google Authentication** (OAuth2) for secure, frictionless user sign-ins, alongside JWT session management.
* 🗄️ **Robust Data Integrity:** Relational data persistence using **PostgreSQL**, with models tightly defined via ORM (SQLAlchemy/SQLModel).
* 📄 **Auto-Generated Documentation:** Interactive API documentation available out-of-the-box via Swagger UI and ReDoc.
* 🛠️ **Modular Architecture:** Clean routing, scalable folder structure, and dependency injection for easy testing and maintenance.

---

## 🧰 Tech Stack

| Component | Technology |
| :--- | :--- | 
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | 
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) | 
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Server** | [Uvicorn](https://www.uvicorn.org/) | 

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your local machine:
* **Python** (v3.10 or higher)
* **PostgreSQL** (Running locally or via Docker)
* **Git**

### 1️⃣ Installation

Clone the repository to your local machine:
```bash
git clone [https://github.com/saurabh-zz007/Her-Flowmate_Backend.git](https://github.com/saurabh-zz007/Her-Flowmate_Backend.git)
cd Her-Flowmate_Backend
```

Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2️⃣ Environment Variables

Create a `.env` file in the root directory. You can copy the provided example file:
```bash
cp .env.example .env
```

Update the `.env` file with your specific configuration, especially your Google Auth credentials and Database URL:

```ini
# --- Database Configuration ---
DATABASE_URL=postgresql://user:password@localhost:5432/herflowmate_db

# --- Security & Authentication ---
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# --- Google OAuth2 Credentials ---
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 3️⃣ Database Setup

Run the Alembic migrations to generate your PostgreSQL tables from the backend models:
```bash
alembic upgrade head
```

### 4️⃣ Running the Server

Start the FastAPI server using Uvicorn with live reloading enabled:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will now be accessible at `http://localhost:8000`.

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation. Once your server is running, you can explore and test the endpoints directly from your browser:

* **Swagger UI (Interactive):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc (Detailed view):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📂 Project Structure

```text
Her-Flowmate_Backend/
├── src/                   
│   ├── auth/               
│   |  ├── controller.py
│   |  ├── data_transfer_objects.py
│   |  ├── models.py
│   |  ├── router.py
│   ├── logs/              
│   |  ├── controller.py
│   |  ├── data_transfer_objects.py
│   |  ├── models.py
│   |  ├── router.py
│   ├── pregnancy/                 
│   |  ├── controller.py
│   |  ├── data_transfer_objects.py
│   |  ├── models.py
│   |  ├── router.py
│   ├── user/             
│   |  ├── controller.py
│   |  ├── data_transfer_objects.py
│   |  ├── models.py
│   |  ├── router.py
│   ├── utils/           
│   |  ├── consent.py
│   |  ├── db.py
│   |  ├── helpers.py
│   |  ├── settings.py
├── .gitignore            
├── main.py            
├── requirements.txt        # Python dependencies
└── README.md               
```

---

## 🤝 Contributing

We welcome contributions to make Her-Flowmate even better! 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Maintainer

* **Saurabh Kumar Vishwakarma**

---
