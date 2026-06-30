import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Navbar from "../components/Navbar";

import {
  FaBook,
  FaCheckCircle,
  FaClock,
  FaMoneyBillWave,
  FaBookOpen,
} from "react-icons/fa";

function UserDashboard() {
  const navigate = useNavigate();

  const [dashboardData, setDashboardData] = useState(null);
  const [myBooks, setMyBooks] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("access");

      if (!token) {
        navigate("/");
        return;
      }

      try {
        const dashboardResponse = await api.get("accounts/user/dashboard/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setDashboardData(dashboardResponse.data);

        const booksResponse = await api.get("transactions/my-books/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setMyBooks(booksResponse.data);
      } catch (error) {
        console.log(error.response?.data);
        navigate("/");
      }
    };

    fetchData();
  }, [navigate]);

  if (!dashboardData) {
    return (
      <div className="loading-container">
        <h2>Loading Dashboard...</h2>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Navbar />

      <div className="welcome-banner">
        <h2>Welcome Back, {dashboardData.Username} 👋</h2>
        <p>View your borrowed books, due dates and fines.</p>
      </div>

      <div className="dashboard-grid">
        <div className="stat-card">
          <FaBook className="card-icon" />
          <h3>Active Books</h3>
          <p>{dashboardData["Active Books"]}</p>
        </div>

        <div className="stat-card">
          <FaCheckCircle className="card-icon" />
          <h3>Returned</h3>
          <p>{dashboardData["Returned Books"]}</p>
        </div>

        <div className="stat-card">
          <FaClock className="card-icon" />
          <h3>Due Soon</h3>
          <p>{dashboardData["Due Soon"]}</p>
        </div>

        <div className="stat-card">
          <FaMoneyBillWave className="card-icon" />
          <h3>Total Fine</h3>
          <p>₹{dashboardData["Total Fine"]}</p>
        </div>

        <div className="stat-card clickable" onClick={() => navigate("/books")}>
          <FaBookOpen className="card-icon" />

          <h3> Browse Books</h3>

          <p className="card-value">📚</p>
        </div>
      </div>

      <div className="books-card">
        <h2>My Borrowed Books</h2>

        <table>
          <thead>
            <tr>
              <th>Book</th>
              <th>Issue Date</th>
              <th>Due Date</th>
              <th>Status</th>
              <th>Fine</th>
            </tr>
          </thead>

          <tbody>
            {myBooks.length > 0 ? (
              myBooks.map((book) => (
                <tr key={book.id}>
                  <td>{book.book_name}</td>

                  <td>{book.issue_date}</td>

                  <td>{book.due_date}</td>

                  <td>
                    <span className={`status ${book.status.toLowerCase()}`}>
                      {book.status}
                    </span>
                  </td>

                  <td>
                    <strong>₹{book.fine_amount}</strong>

                    {book.fine_amount > 0 && (
                      <>
                        <br />
                        <small>
                          {book.late_days} × ₹{book.fine_per_day}/day
                        </small>
                      </>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">No borrowed books found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default UserDashboard;
