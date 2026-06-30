import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import api from "../services/api";
import "../App.css";

function CreatePassword() {
  const { token } = useParams();

  const navigate = useNavigate();

  const [password, setPassword] = useState("");

  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      Swal.fire({
        icon: "error",
        title: "Passwords do not match",
        confirmButtonColor: "#16a34a",
      });

      return;
    }

    try {
      await api.post(`accounts/create-password/${token}/`, {
        password,
      });

      await Swal.fire({
        icon: "success",
        title: "Password Created",
        text: "Your account has been activated successfully.",
        confirmButtonColor: "#16a34a",
      });

      sessionStorage.setItem("showWelcome", "true");

      navigate("/");
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Failed",
        text: error.response?.data?.error || "Failed to create password.",
        confirmButtonColor: "#dc3545",
      });
    }
  };

  return (
    <div className="create-password-page">
      <div className="create-password-card">
        <div className="create-password-header">
          <h1>📚 Library Management System</h1>

          <h2>Create Your Password</h2>

          <p>
            Welcome! Your account has been created successfully. Please create a
            secure password to activate your account.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="create-password-form">
          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          <button type="submit">Create Password</button>
        </form>

        <div className="security-note">
          🔒 Your password is securely encrypted before being stored.
        </div>
      </div>
    </div>
  );
}

export default CreatePassword;
