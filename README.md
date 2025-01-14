# Basic CRM System with Django

## Project Overview
This is a Basic Customer Relationship Management (CRM) system built using Django. The system enables organizations to manage leads, agents, and categories efficiently. It provides role-based access control, CRUD operations for leads and agents, and a user-friendly interface styled with `crispy_forms` and Tailwind.

---

## Features

### User Management
- **Custom User Model**: Supports `is_organizer` and `is_agent` roles.
- **Authentication**: Login, logout, and signup functionalities.
- **Role-Based Access Control**: Ensures users can only access authorized resources.

### Lead Management
- Add, update, and delete leads.
- Assign leads to agents.
- Categorize leads for better organization.
- Filter leads based on assignment status and category.

### Agent Management
- Add, update, and delete agents.
- Assign agents to organizations.
- Automatically send email notifications to agents upon creation.

### Miscellaneous
- Responsive design with Tailwind CSS.
- Email integration for notifications.
- Pagination and optimized query handling.

---

## Installation

### Prerequisites
- Python 3.7+
- Django 3.1+
- Node.js 12.22.0+
- SQLite (default) or PostgreSQL/MySQL (recommended for production)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/django-crm.git
   cd django-crm
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000` in your browser.

---




## Key Technologies

- **Backend**: Django 3.1
- **Frontend**: Tailwind CSS, crispy-forms
- **Database**: SQLite (default), PostgreSQL/MySQL (recommended for production)
- **Authentication**: Custom User Model
- **Email**: Django email backend

---

