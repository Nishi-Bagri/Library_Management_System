# 📚 Library Management System

A full-stack **Library Management System** built using **React.js**, **Django**, **Django REST Framework**, and **SQLite**. The application provides role-based access for Admin, Librarian, and Users to efficiently manage books, users, and library transactions.

---

# 🚀 Features

## Authentication & Authorization

* JWT Authentication
* Role-based Login (Admin, Librarian, User)
* Forgot Password
* Reset Password
* Create Password using Email Link
* Protected Routes
* Automatic Token Refresh

---

## Admin Features

* Dashboard with Statistics
* Manage Books (Add, Update, Delete, View)
* Manage Users
* Create Librarian Accounts
* View Issued Books
* View Returned Books
* View Activity Logs
* Approve/Reject Account Deactivation Requests
* Manage Library Reports

---

## Librarian Features

* Dashboard
* Issue Books
* Return Books
* Renew Books
* View Issued Books
* Calculate Late Fine Automatically
* Manage Book Inventory

---

## User Features

* Login
* View Issued Books
* View Profile
* Request Account Deactivation
* Change Password

---

## Book Management

* Add New Books
* Edit Book Details
* Delete Books
* Search Books
* View Available Copies
* Track Book Quantity

---

## Issue & Return Management

* Issue Books
* Return Books
* Renew Books
* Due Date Calculation
* Fine Calculation
* Late Days Calculation
* Issue Number Generation

---

## Activity Logging

Tracks every important activity including:

* Book Added
* Book Updated
* Book Deleted
* Book Issued
* Book Returned
* Book Renewed
* User Created
* User Updated
* User Deleted
* Account Deactivation Requests

---

## Dashboard

Displays:

* Total Books
* Available Books
* Issued Books
* Total Users
* Librarians
* Pending Requests

---

## Responsive Design

The application is fully responsive and supports:

* Desktop
* Laptop
* Tablet
* Mobile Devices

---

# 🛠 Tech Stack

## Frontend

* React.js
* React Router DOM
* Axios
* SweetAlert2
* React Icons
* CSS3

## Backend

* Python
* Django
* Django REST Framework
* Simple JWT

## Database

* SQLite

---

# 📂 Project Structure

```
library-management-system/

├── backend/
│   ├── accounts/
│   ├── books/
│   ├── transactions/
│   ├── activity/
│   ├── library_management/
│   ├── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── assets/
│   │   └── App.jsx
│
└── README.md
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/library-management-system.git
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

Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Migrations

```bash
python manage.py migrate
```

Start Server

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

Run Project

```bash
npm run dev
```

---

# 🔐 Default Roles

* Admin
* Librarian
* User

---

# 📊 Modules

* Authentication
* User Management
* Book Management
* Transactions
* Activity Logs
* Dashboard
* Reports
* Settings

---

# 📷 Screens

* Login
* Admin Dashboard
* Librarian Dashboard
* User Dashboard
* Add Book
* View Books
* Issue Book
* Issued Books
* Activity Logs
* Settings
* Profile

---

# Future Enhancements

* Email Notifications
* PDF Report Generation
* Excel Export
* Barcode Scanner
* QR Code Support
* Book Reservation
* Online Book Search
* Dark Mode
* Charts & Analytics

---

# 👩‍💻 Developed By

**Nishi Bagri**

Python Django Developer

---

# 📄 License

This project is developed for educational and portfolio purposes.
