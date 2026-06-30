import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useEffect, useState } from "react";
import api from "../services/api";

import {
  FaUserCircle,
  FaUserSlash,
  FaCheckCircle,
  FaShieldAlt,
} from "react-icons/fa";

function Settings() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get("accounts/profile/");
        setProfile(response.data);
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };

    fetchProfile();
  }, []);

  const handleDashboard = () => {
    switch (profile.role) {
      case "ADMIN":
        navigate("/admin");
        break;

      case "LIBRARIAN":
        navigate("/librarian");
        break;

      case "USER":
        navigate("/user");
        break;

      default:
        navigate("/");
    }
  };
  if (!profile) {
    return (
      <div className="loading-container">
        <h2>Loading Settings...</h2>
      </div>
    );
  }

  const handleChangePassword = async () => {
    if (!currentPassword || !newPassword || !confirmPassword) {
      setMessage("All fields are required.");
      setMessageType("error");

      setTimeout(() => setMessage(""), 3000);
      return;
    }

    try {
      const response = await api.post("accounts/change-password/", {
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });

      setMessage(response.data.message);
      setMessageType("success");

      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");

      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      if (error.response?.data?.error) {
        setMessage(error.response.data.error);
      } else if (error.response?.data?.confirm_password) {
        setMessage(error.response.data.confirm_password[0]);
      } else {
        setMessage("Something went wrong.");
      }

      setMessageType("error");

      setTimeout(() => setMessage(""), 3000);
    }
  };

  return (
    <div className="dashboard-container">
      <Navbar />

      {/* Welcome Banner */}

      <div className="welcome-banner">
        <h2>⚙️ Account Settings</h2>
        <p>Manage your profile and account preferences.</p>
      </div>

      {/* Profile & Account */}

      <div className="settings-grid">
        {/* Profile Card */}

        <div className="settings-card">
          <h3>
            <FaUserCircle /> Profile
          </h3>

          <div className="avatar-circle">
            {profile.username?.charAt(0).toUpperCase()}
          </div>

          <div className="info-row">
            <span>Username</span>
            <strong>{profile.username}</strong>
          </div>

          <div className="info-row">
            <span>Email</span>
            <strong>{profile.email}</strong>
          </div>
        </div>

        {/* Account Card */}

        <div className="settings-card">
          <h3>
            <FaShieldAlt /> Account
          </h3>

          <div className="info-row">
            <span>Status</span>

            <strong className="active">
              <FaCheckCircle /> Active
            </strong>
          </div>

          <div className="info-row">
            <span>Role</span>
            <strong>{profile.role}</strong>
          </div>

          <div className="info-row">
            <span>Account Type</span>
            <strong>
              {profile.role === "ADMIN"
                ? "Administrator"
                : profile.role === "LIBRARIAN"
                  ? "Librarian"
                  : "Library Member"}
            </strong>
          </div>
        </div>
      </div>

      {/* Security Card */}

      <div className="security-card">
        <h3>🔐 Security</h3>

        <div className="password-group">
          <label>Current Password</label>
          <input
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            placeholder="Enter current password"
          />
        </div>

        <div className="password-group">
          <label>New Password</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            placeholder="Enter new password"
          />
        </div>

        <div className="password-group">
          <label>Confirm Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm new password"
          />
        </div>

        <button className="update-password-btn" onClick={handleChangePassword}>
          Update Password
        </button>

        {message && <div className={`message-box ${messageType}`}>{message}</div>}
      </div>

      {/* Back Button */}

      <div className="back-dashboard">
        <button className="dashboard-btn" onClick={handleDashboard}>
          ← Back to Dashboard
        </button>
      </div>

      {/* Danger Zone */}

      {(profile.role === "USER" || profile.role === "LIBRARIAN") && (
        <div className="danger-card">
          <h3>
            <FaUserSlash /> Danger Zone
          </h3>

          <h4>Account Deactivation</h4>

          <p>
            Once your request is approved, your account will be permanently
            deactivated and you will no longer be able to access the Library
            Management System.
          </p>

          <button
            className="delete-btn"
            onClick={() => navigate("/request-deactivation")}
          >
            Request Account Deactivation
          </button>
        </div>
      )}
    </div>
  );
}

export default Settings;
