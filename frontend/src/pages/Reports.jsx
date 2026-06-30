import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

import {
  FaBook,
  FaUsers,
  FaBookOpen,
  FaUndoAlt,
  FaExclamationTriangle,
  FaMoneyBillWave,
} from "react-icons/fa";

function Reports() {
  const navigate = useNavigate();

  const [reportData, setReportData] = useState(null);

  useEffect(() => {
    const loadReports = async () => {
      try {
        const response = await api.get("accounts/reports/");
        setReportData(response.data);
      } catch (error) {
        console.log(error.response?.data);
      }
    };

    loadReports();
  }, []);

  const handleBack = () => {
    const role = localStorage.getItem("role");

    if (role === "ADMIN") {
      navigate("/admin");
    } else if (role === "LIBRARIAN") {
      navigate("/librarian");
    } else {
      navigate("/user");
    }
  };

  if (!reportData) {
    return (
      <div className="loading-container">
        <h2>Loading Reports...</h2>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="books-card">
        <h1>📊 Library Reports</h1>
        <p className="report-subtitle">
          Monitor your library statistics and reports.
        </p>

        <div className="dashboard-grid">
          <div className="stat-card">
            <FaBook className="report-icon" />
            <h3>Book Titles</h3>
            <p>{reportData["Total Books"]}</p>
          </div>

          <div className="stat-card">
            <FaUsers className="report-icon" />
            <h3>Library Members</h3>
            <p>{reportData["Total Users"]}</p>
          </div>

          <div className="stat-card">
            <FaBookOpen className="report-icon" />
            <h3>Issued Books</h3>
            <p>{reportData["Issued Books"]}</p>
          </div>

          <div className="stat-card">
            <FaUndoAlt className="report-icon" />
            <h3>Returned Books</h3>
            <p>{reportData["Returned Books"]}</p>
          </div>

          <div className="stat-card">
            <FaExclamationTriangle className="report-icon overdue-icon" />
            <h3>Overdue Books</h3>
            <p>{reportData["Overdue Books"]}</p>
          </div>

          <div
            className="stat-card clickable"
            onClick={() => navigate("/fine-summary")}
          >
            <FaMoneyBillWave className="report-icon fine-icon" />

            <h3>Fine Collection</h3>

            <p>₹ {reportData["Total Fine"]}</p>
          </div>
        </div>

        <button className="back-btn" onClick={handleBack}>
          ← Back to Dashboard
        </button>
      </div>
    </div>
  );
}

export default Reports;
