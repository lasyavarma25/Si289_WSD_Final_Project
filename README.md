# Dosa Restaurant API

This project is a simple backend API built for a dosa restaurant using **FastAPI** and **SQLite**. It was created as part of final project to practice RESTful API design and working with relational databases where you can create, update, retrive and delete data.

## Key Features

- Complete CRUD functionality for:
  - Customers
  - Items
  - Orders

- SQLite database with enforced primary and foreign key relationships
- This project has integrated API documentation available at `/docs`
- Default route (`/`) redirects users to API documentation
- Clean and minimal implementation using only FastAPI and SQLite

---

## Getting Started

### Step 1: Clone the Repository

```bash
git clone https://github.com/lasyavarma25/Si289_WSD_Final_Project.git
cd Si289_WSD_Final_Project
```

### Step 2: Set Up a Virtual Environment

```bash
python -m venv myenv
```

#### On Windows

```bash
myenv\Scripts\activate
```

#### On macOS/Linux

```bash
source myenv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create the SQLite Database

```bash
python init_db.py
```

### Step 5: Launch the API Server

```bash
uvicorn main:app --reload
```

You can access the Interactive Swagger documentation at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

Enjoy exploring and testing the Dosa Restaurant API!
