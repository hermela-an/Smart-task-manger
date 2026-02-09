# 🎯 Smart Task Manager

A strong, internship-level Django REST Framework application designed to help users manage tasks with smart features and secure authentication.

## 🚀 Key Features

-   **✅ Secure Authentication**: JWT Token system with protected routes.
-   **✅ Dashboard**: Comprehensive overview of task statistics.
-   **✅ Task Management (CRUD)**: Create, Read, Update, and Delete tasks with ease.
-   **✅ Smart Recommendations**: Priority-based task suggestions considering due dates.
-   **✅ Email Reminders**: Automated management command to notify users of tasks due tomorrow.
-   **✅ Environment Security**: Sensitive data protected via `.env` files.

## 🛠️ Tech Stack

-   **Backend**: Django, Django REST Framework
-   **Database**: SQLite (Development)
-   **Security**: SimpleJWT, Python-dotenv
-   **Documentation**: Swagger (DRF-YASG)

## 📦 Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Smart-task-manger.git
    cd Smart-task-manger
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Environment Variables**:
    Create a `.env` file in the root directory and add the following:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    ```

5.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6.  **Start the Server**:
    ```bash
    python manage.py runserver
    ```

## 📬 Special Commands

### Send Email Reminders
To trigger the email reminders for tasks due tomorrow:
```bash
python manage.py send_task_reminders
```

## 🛡️ API Documentation
Once the server is running, visit:
-   `http://127.0.0.1:8000/swagger/` - Interactive API docs.

## 💡 Why this project?
This project demonstrates more than just CRUD. It shows an understanding of:
- **Scalability**: Decoupling long-running tasks like emails.
- **Security**: Proper handling of secrets and tokens.
- **User Experience**: Providing proactive value via recommendations and reminders.
