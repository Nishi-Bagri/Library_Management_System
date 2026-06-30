import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Navbar from "../components/Navbar";
import {
  FaUsers,
  FaBook,
  FaUserTie,
  FaCheckCircle,
  FaKey,
  FaUserSlash,
  FaEdit,
  FaTrash,
  FaExchangeAlt,
  FaUndo,
  FaSync,
} from "react-icons/fa";

import { MdMenuBook } from "react-icons/md";

const getActivityIcon = (action) => {
  switch (action) {
    case "BOOK_ADDED":
      return <FaBook className="activity-icon green" />;

    case "BOOK_UPDATED":
      return <FaEdit className="activity-icon blue" />;

    case "BOOK_DELETED":
      return <FaTrash className="activity-icon red" />;

    case "BOOK_ISSUED":
      return <FaExchangeAlt className="activity-icon purple" />;

    case "BOOK_RETURNED":
      return <FaUndo className="activity-icon teal" />;

    case "BOOK_RENEWED":
      return <FaSync className="activity-icon orange" />;

    case "DEACTIVATION_REQUESTED":
      return <FaUserSlash className="activity-icon orange" />;

    case "DEACTIVATION_REJECTED":
      return <FaUserSlash className="activity-icon red" />;

    case "USER_DEACTIVATED":
      return <FaUserSlash className="activity-icon red" />;

    default:
      return <FaCheckCircle className="activity-icon gray" />;
  }
};

function AdminDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [activities, setActivities] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access");

    if (!token) {
      navigate("/");
      return;
    }

    const fetchDashboard = async () => {
      try {
        const dashboardResponse = await api.get("accounts/admin/dashboard/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setDashboardData(dashboardResponse.data);

        const activityResponse = await api.get("activity/recent-activities/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setActivities(activityResponse.data);
      } catch (error) {
        console.log(error);
        navigate("/");
      }
    };

    fetchDashboard();
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
        <h2>Welcome Back, Admin 👋</h2>

        <p>
          Manage books, users, librarians and monitor library activities from
          one place.
        </p>
      </div>

      <div className="dashboard-grid">
        {/* Librarians */}
        <div
          className="stat-card clickable"
          onClick={() => navigate("/librarians")}
        >
          <FaUserTie className="card-icon" />
          <h3>Librarians</h3>
          <p>{dashboardData.Total_librarians}</p>
        </div>

        {/* Users */}
        <div className="stat-card clickable" onClick={() => navigate("/users")}>
          <FaUsers className="card-icon" />
          <h3>Users</h3>
          <p>{dashboardData.Total_users}</p>
        </div>

        {/* Books */}
        <div className="stat-card clickable" onClick={() => navigate("/books")}>
          <FaBook className="card-icon" />
          <h3>Total Books</h3>
          <p>{dashboardData.Total_books}</p>
        </div>

        {/* Available Books */}
        <div
          className="stat-card clickable"
          onClick={() => navigate("/books?filter=available")}
        >
          <FaCheckCircle className="card-icon" />
          <h3>Available Books</h3>
          <p>{dashboardData.Available_books}</p>
        </div>

        {/* Issued Books */}
        <div
          className="stat-card clickable"
          onClick={() => navigate("/issued-books")}
        >
          <MdMenuBook className="card-icon" />
          <h3>Issued Books</h3>
          <p>{dashboardData.Issued_books}</p>
        </div>

        {/* Issue Book */}
        <div
          className="stat-card clickable"
          onClick={() => navigate("/issue-book")}
        >
          <MdMenuBook className="card-icon" />

          <h3>Issue Book</h3>

          <p className="issue-action">Click to Issue</p>
        </div>

        {/* Password Requests */}
        <div
          className="stat-card clickable"
          onClick={() => navigate("/password-reset-requests")}
        >
          <FaKey className="card-icon" />

          <h3>Password Requests</h3>

          <p className="request-total">
            Total: {dashboardData.Total_password_requests}
          </p>

          <p className="request-pending">
            Pending: {dashboardData.Pending_password_requests}
          </p>
        </div>

        <div
          className="stat-card clickable"
          onClick={() => navigate("/deactivation-requests")}
        >
          <FaUserSlash className="card-icon" />

          <h3>Deactivation Requests</h3>

          <p className="request-total">
            Total: {dashboardData.Total_deactivation_requests}
          </p>

          <p className="request-pending">
            Pending: {dashboardData.Pending_deactivation_requests}
          </p>
        </div>
      </div>
      <div className="activity-card">
        <div className="activity-header">
          <h2>🕒 Recent Activity</h2>
        </div>

        {activities.length === 0 ? (
          <p className="empty-activity">No recent activities found.</p>
        ) : (
          activities.map((activity) => (
            <div className="activity-item" key={activity.id}>
              <div className="activity-left">
                {getActivityIcon(activity.action)}

                <div className="activity-content">
                  <h4>{activity.action.replaceAll("_", " ")}</h4>

                  <p>{activity.description}</p>

                  <span>By {activity.performed_by}</span>
                </div>
              </div>

              <small>{new Date(activity.created_at).toLocaleString()}</small>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
