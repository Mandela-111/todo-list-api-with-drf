# Build Your Own To-Do List API

A robust, feature-rich Task Management and To-Do List backend API built with **Django** and **Django REST Framework (DRF)**. This project implements modern API design patterns, clean database architecture with audit trails, custom action endpoints, and flexible query filtering.

---

## Features

- **Audited Models:** Built using an abstract base model (`TimeStampedModel`) to automatically track creation and update timestamps across entities.
- **RESTful Endpoints:** Full CRUD (Create, Read, Update, Delete) support for task management.
- **Dual-Purpose Views:** Efficient request handling supporting both list operations and single-resource retrieval through shared view classes.
- **Custom Actions:** Dedicated endpoints for specialized state changes, such as toggling or marking task completion status (`/api/tasks/<id>/mark/`).
- **User-Specific Filtering:** Query parameters and endpoints designed to retrieve filtered task lists (e.g., viewing completed tasks by user).
- **Robust Validation:** Tailored error handling and validation logic to ensure data integrity.

---

## Tech Stack

- **Python 3.14+**
- **Django 5.x+**
- **Django REST Framework (DRF)**
- **SQLite** (Development Database)

---

## Project Structure

```text
todo_list/
│
├── backend/            # Project configuration package (settings, urls, wsgi, asgi)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── todo_app/           # Core task management application
│   ├── migrations/
│   ├── models.py       # Tasks model inheriting from TimeStampedModel
│   ├── serializers.py  # DRF serializers for Tasks
│   ├── views.py        # APIViews handling CRUD and custom status toggles
│   └── urls.py         # App-level routing
│
├── utils/              # Shared project utilities
│   └── models.py       # Abstract TimeStampedModel
│
├── .venv/              # Python virtual environment
├── db.sqlite3          # Development database
├── manage.py           # Django project management script
└── README.md
```

---

## Getting Started

Follow these instructions to set up and run the project locally on your machine (optimized for IDEs like PyCharm Community Edition).

### Prerequisites

- Python 3.14+ installed
- Git

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/todo_list.git
   cd todo_list
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

---

## Configuration Note (PyCharm Community Edition)

If you are debugging or running this project inside PyCharm Community Edition using a generic Python run configuration pointing to `manage.py`, ensure your environment variables are set correctly to avoid `ImproperlyConfigured` errors:

* **Working Directory:** `/path/to/todo_list`
* **Environment Variables:** `PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=backend.settings`
* **Script Parameters:** `runserver`

---

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/tasks/` | Retrieve a list of all tasks |
| `POST` | `/api/tasks/` | Create a new task |
| `GET` | `/api/tasks/<id>/` | Retrieve a single task by ID |
| `PUT` | `/api/tasks/<id>/` | Update an existing task |
| `DELETE` | `/api/tasks/<id>/` | Delete a specific task |
| `PUT` | `/api/tasks/<id>/mark/` | Mark/toggle a task as complete or incomplete |

---

## Author

* **Mandela-the-gr8**
