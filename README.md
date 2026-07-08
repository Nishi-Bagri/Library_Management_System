# 📚 AI-Powered Library Management System (LibraryGPT)

An AI-powered **Library Management System** built using **Django REST Framework**, **React.js**, and **OpenRouter**. The application provides role-based access for **Admin**, **Librarian**, and **User**, enabling efficient management of books, users, borrowing transactions, fines, reports, and system activities.

A key feature of the project is **LibraryGPT**, an AI-powered inquiry-based chatbot that helps users discover books, answer library-related questions, explain library policies, and recommend books using OpenAI-compatible Function Calling.

---

# 🚀 Features

## 🔐 Authentication & Authorization

- JWT Authentication
- Role-Based Access Control (Admin, Librarian, User)
- Secure Login
- Create Password via Email
- Forgot Password
- Password Reset Approval Workflow
- Password History Tracking

---

## 👥 User Management

- Create Users and Librarians
- Update User Information
- Delete Users
- User Pagination
- Account Deactivation Requests
- Approve/Reject Deactivation Requests

---

## 📚 Book Management

- Add Books
- Update Books
- Delete Books
- View Books
- Pagination
- Book Availability Tracking

---

## 📖 Book Transactions

- Issue Books
- Return Books
- Renew Books
- Due Date Management
- Automatic Fine Calculation
- Issue Number Generation

---

## 💰 Fine Management

- Automatic Fine Calculation
- Fine Summary
- Fine History

---

## 📊 Dashboard & Reports

### 👨‍💼 Admin Dashboard

- Total Users
- Total Librarians
- Total Books
- Available Books
- Issued Books
- Pending Password Requests
- Pending Deactivation Requests
- Recent Activities

### 📚 Librarian Dashboard

- Total Users
- Total Books
- Available Books
- Issued Books
- Recent Activities

### 👤 User Dashboard

- Active Borrowed Books
- Due Soon Books
- Returned Books
- Fine Details
- Borrowed Book History

### Reports

- User Report
- Book Report
- Transaction Report
- Fine Report

---

# 🤖 LibraryGPT (AI Chatbot)

LibraryGPT is an AI-powered inquiry-based chatbot integrated into the Library Management System.

Instead of navigating multiple pages, users can simply ask questions in natural language.

## Current Capabilities

- Search books by title
- Search books by author
- Search books by category
- Show available books
- View complete book details
- Answer library-related questions
- Explain library policies
- Guide users in using the Library Management System
- Recommend books based on available categories
- Help users contact the librarian or administrator

## Library Information

LibraryGPT can answer questions related to:

- Fine Policy
- Borrowing Policy
- Renewal Policy
- Library Timings
- Contact Information
- Password Reset Guidance

## Current Limitations

LibraryGPT is intentionally designed as an **Inquiry-Based Assistant**.

It **cannot**:

- Issue Books
- Return Books
- Renew Books
- Modify Library Records
- Manage Users
- Perform Administrative Actions

---

# 🧠 AI Architecture

LibraryGPT uses **OpenRouter** with **OpenAI-compatible Function Calling**.

```
User
        │
        ▼
React ChatBot
        │
        ▼
Django REST API
        │
        ▼
AIService
        │
        ▼
OpenRouter LLM
        │
        ▼
Function Calling
        │
        ▼
Tool Dispatcher
        │
        ▼
Library Tools
        │
        ▼
SQLite Database
```

Instead of relying on the LLM's own knowledge, the chatbot retrieves real-time information directly from the library database using backend tools.

---

# ⚡ AI Function Calling

LibraryGPT currently supports the following backend tools:

- `search_books()`
- `available_books()`
- `search_by_author()`
- `search_by_category()`
- `book_details()`
- `library_information()`
- `recommend_books()`

---

# 📜 Activity Logging

The system automatically records important activities including:

- Book Added
- Book Updated
- Book Deleted
- Book Issued
- Book Returned
- Book Renewed
- User Created
- Librarian Created
- Password Approved
- Password Rejected
- Fine Collected
- Deactivation Requested
- User Deactivated
- Deactivation Rejected

---

# ⚙️ Settings

- Update Profile
- Change Password
- Request Account Deactivation

---

# 🛠️ Tech Stack

## Backend

- Python
- Django
- Django REST Framework
- Simple JWT

## Frontend

- React.js
- React Router
- Axios
- SweetAlert2
- React Icons

## AI

- OpenRouter
- OpenAI-Compatible Function Calling
- GPT-OSS Models
- Google Gemma Models

## Database

- SQLite

---

# 📂 Project Structure

```
Library_Management_System/
│
├── backend/
│   ├── accounts/
│   ├── activity/
│   ├── books/
│   ├── chatbot/
│   ├── transactions/
│   └── config/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── assets/
│   └── package.json
│
└── README.md
```

---

# 🔑 User Roles

## 👨‍💼 Admin

- Manage Librarians
- Manage Users
- Manage Books
- Issue Books
- View Issued Books
- View Reports
- View Dashboard
- Approve Password Requests
- Approve Deactivation Requests
- View Activities

---

## 📚 Librarian

- Manage Users
- Manage Books
- Issue Books
- Return Books
- Renew Books
- View Reports
- View Dashboard

---

## 👤 User

- Login
- Browse Books
- View Dashboard
- View Borrowed Books
- Change Password
- Request Password Reset
- Request Account Deactivation
- Interact with LibraryGPT

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Nishi-Bagri/Library_Management_System.git
```

```bash
cd Library_Management_System
```

---

## Backend Setup

```bash
cd backend
```

Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Migrations

```bash
python manage.py migrate
```

Start Backend

```bash
python manage.py runserver
```

---

## Frontend Setup

```bash
cd frontend
```

Install Packages

```bash
npm install
```

Start React

```bash
npm run dev
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

```env
SECRET_KEY=your_secret_key

OPENROUTER_API_KEY=your_openrouter_api_key

EMAIL_HOST_USER=your_email

EMAIL_HOST_PASSWORD=your_email_password
```

---

# 📌 API Highlights

### Authentication

- Login
- Forgot Password
- Reset Password
- Create Password

### User Management

- Users CRUD
- Librarians CRUD

### Book Management

- Books CRUD

### Transactions

- Issue Book
- Return Book
- Renew Book

### Reports

- Dashboard APIs
- Fine Summary
- Fine History
- Activity APIs

### AI Chatbot

- Chat API
- AI Function Calling
- Book Search
- Library Information
- Book Recommendation

---

# 📈 Future Enhancements

- Conversation History
- AI Conversation Memory
- Voice-Based Library Assistant
- Multi-language Support
- Book Reservation System
- Barcode / QR Code Integration
- Export Reports to PDF/Excel
- PostgreSQL Migration
- Docker Deployment
- Unit Testing
- CI/CD Pipeline

---

# 👩‍💻 Author

**Nishi Bagri**

Python Developer | Django Developer | AI Enthusiast

**GitHub**
https://github.com/Nishi-Bagri

**LinkedIn**
(Add your LinkedIn Profile)

---

## 🌐 Live Demo

Coming Soon...

---

## ⭐ If you found this project useful, don't forget to star the repository.
