# 📚 Library Management System

A full-stack Library Management System built using **Django REST Framework** and **React.js**. The application provides role-based access for **Admin**, **Librarian**, and **User**, enabling efficient management of books, users, borrowing transactions, fines, reports, and system activities.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- JWT Authentication
- Role-Based Access Control (Admin, Librarian, User)
- Secure Login
- Create Password via Email
- Forgot Password
- Password Reset Approval Workflow
- Password History Tracking

### 👥 User Management
- Create Users and Librarians
- Update User Information
- Delete Users
- User Pagination
- Account Deactivation Requests
- Approve/Reject Deactivation Requests

### 📚 Book Management
- Add Books
- Update Books
- Delete Books
- View Books
- Pagination
- Book Availability Tracking

### 📖 Book Transactions
- Issue Books
- Return Books
- Renew Books
- Due Date Management
- Fine Calculation
- Issue Number Generation

### 💰 Fine Management
- Automatic Fine Calculation
- Fine Summary
- Fine History

### 📊 Dashboard & Reports
#### Admin Dashboard
- Total Users
- Total Librarians
- Total Books
- Available Books
- Issued Books
- Pending Password Requests
- Pending Deactivation Requests
- Recent Activities

#### Librarian Dashboard
- Total Users
- Total Books
- Available Books
- Issued Books
- Recent Activities

#### Reports
- User Report
- Book Report
- Transaction Report
- Fine Report

### 📜 Activity Logging
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

### ⚙️ Settings
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
- SQLite

## Frontend
- React.js
- React Router
- Axios
- SweetAlert2
- React Icons

---

# 📂 Project Structure

```
Library_Management_System/
│
├── backend/
│   ├── accounts/
│   ├── activity/
│   ├── books/
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
- View Dashboard
- Change Password
- Request Password Reset
- Request Account Deactivation

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

Activate Virtual Environment

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

---

# 📈 Future Enhancements

- Email Notifications using HTML Templates
- Book Reservation System
- Barcode / QR Code Integration
- Book Search & Filters
- Export Reports to PDF/Excel
- Docker Deployment
- PostgreSQL Support
- Unit Testing
- CI/CD Pipeline

---

# 👩‍💻 Author

**Nishi Bagri**

Python Developer

GitHub:
https://github.com/Nishi-Bagri

LinkedIn:
(Add your LinkedIn Profile)

---

## ⭐ If you found this project useful, don't forget to star the repository.
