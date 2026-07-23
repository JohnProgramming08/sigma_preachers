![Header](chatterbox-banner.svg)

# Chatterbox

Chatterbox is a real-time community chat platform built with Flask, Socket.IO, SQLAlchemy, and Flask-Login. It supports public rooms, private rooms, user profiles, account recovery, moderation workflows, and searchable room/user discovery.

The project is structured as a clean Flask application with blueprints for routes, a service layer for business logic, and a database layer for persistence. It is designed to feel like a full product rather than a demo: users can sign up, log in, chat in real time, join private rooms, update their profiles, verify emails, reset passwords, and interact with admin tools.

## Highlights

- Real-time messaging with Flask-SocketIO
- Public and private chat rooms
- Signup, login, logout, and password reset flows
- Email verification and email-change verification
- Profile editing and profile viewing
- User and room search endpoints
- Role-based moderation for MASTER and ADMIN users
- Ban, unban, and promote workflows
- Admin inbox for contact messages and moderation requests
- Automated test coverage for routes, services, database helpers, and Socket.IO behavior

## Tech Stack

- Python 3.14+
- Flask
- Flask-Login
- Flask-SocketIO
- Flask-WTF
- SQLAlchemy
- PostgreSQL-compatible database support
- Requests for email delivery
- Pytest for testing

## Getting Started

### Requirements

- Python 3.14 or newer
- A database available through a SQLAlchemy connection string
- Environment variables configured before startup

### Environment Variables

Create a `.env` file with the values your app needs:

```env
database_uri=postgresql+psycopg2://username:password@localhost:5432/chat_app
secret_key=your-secret-key
master_username=MASTER
master_password=MASTER
```

### Run the App

From the project root, start the server with:

```bash
python main.py
```