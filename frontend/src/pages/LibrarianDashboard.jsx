import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Navbar from "../components/Navbar";
import {
  FaUsers,
  FaBook,
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

    case "PASSWORD_APPROVED":
      return <FaKey className="activity-icon green" />;

    case "PASSWORD_REJECTED":
      return <FaKey className="activity-icon red" />;

    case "DEACTIVATION_REQUESTED":
      return <FaUserSlash className="activity-icon orange" />;

    case "USER_DEACTIVATED":
      return <FaUserSlash className="activity-icon red" />;

    case "DEACTIVATION_REJECTED":
      return <FaUserSlash className="activity-icon red" />;

    default:
      return <FaCheckCircle className="activity-icon gray" />;
  }
};

function LibrarianDashboard() {
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
        const dashboardResponse = await api.get(
          "accounts/librarian/dashboard/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

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
        <h2>Welcome Back, Librarian 👋</h2>

        <p>Manage books, issue records and assist library members.</p>
      </div>

      <div className="dashboard-grid">
        <div className="stat-card clickable" onClick={() => navigate("/users")}>
          <FaUsers className="card-icon" />
          <h3>Total Users</h3>
          <p>{dashboardData.Total_Users}</p>
        </div>

        <div className="stat-card clickable" onClick={() => navigate("/books")}>
          <FaBook className="card-icon" />
          <h3>Total Books</h3>
          <p>{dashboardData.Total_Books}</p>
        </div>

        <div
          className="stat-card clickable"
          onClick={() => navigate("/books?filter=available")}
        >
          <FaCheckCircle className="card-icon" />
          <h3>Available Books</h3>
          <p>{dashboardData.Available_Books}</p>
        </div>

        <div
          className="stat-card clickable"
          onClick={() => navigate("/issue-book")}
        >
          <MdMenuBook className="card-icon" />
          <h3>Issue Book</h3>
          <p className="issue-action">Click to Issue</p>
        </div>

        <div
          className="stat-card clickable"
          onClick={() => navigate("/issue-book")}
        >
          <MdMenuBook className="card-icon" />
          <h3>Issue Book</h3>
        </div>

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
                  <h4>
                    {activity.action
                      .replaceAll("_", " ")
                      .toLowerCase()
                      .replace(/\b\w/g, (c) => c.toUpperCase())}
                  </h4>

                  <p>{activity.description}</p>

                  <span>Performed by {activity.performed_by}</span>
                </div>
              </div>

              <small>
                {new Date(activity.created_at).toLocaleString("en-IN", {
                  day: "numeric",
                  month: "short",
                  year: "numeric",
                  hour: "numeric",
                  minute: "2-digit",
                })}
              </small>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default LibrarianDashboard;
