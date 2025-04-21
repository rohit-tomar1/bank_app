---

# Lincoln Bank

**Lincoln Bank** is a web-based banking application built with Django. It enables users to manage accounts, transfer funds, view transactions, and perform basic banking operations securely.

---

##  Features

- User registration and authentication  
- Account creation and balance tracking  
- Fund transfers between accounts  
- Transaction history and account statements  
- Admin dashboard for managing users and accounts

---

##  Tech Stack

- **Backend**: Django (Python)  
- **Database**: SQLite (default, can be configured to use PostgreSQL/MySQL)  
- **Frontend**: HTML, CSS, Bootstrap (can be extended to React or Vue)

---

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/DjangoBank.git
cd DjangoBank
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

---

##  Configuration

- To switch databases, update `DATABASES` settings in `settings.py`
- For production, configure environment variables and use `django-environ` or `python-decouple`

---

##  To-Do

- [ ] Add multi-factor authentication  
- [ ] Integrate real-time notifications  
- [ ] Add support for recurring payments  
- [ ] Implement user roles (e.g., banker, auditor)

---
