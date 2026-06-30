import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import api from "../services/api";
import "../App.css";

function ResetPassword() {

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

      await api.post(
        `accounts/reset-password/${token}/`,
        {
          password,
        }
      );

      await Swal.fire({
        icon: "success",
        title: "Password Reset Successful",
        text: "Your password has been updated successfully. Please login with your new password.",
        confirmButtonColor: "#16a34a",
      });

      navigate("/");

    } catch (error) {

      Swal.fire({
        icon: "error",
        title: "Reset Failed",
        text:
          error.response?.data?.error ||
          "Password reset link is invalid or has expired.",
        confirmButtonColor: "#dc3545",
      });

    }

  };

  return (

    <div className="create-password-page">

      <div className="create-password-card">

        <div className="create-password-header">

          <h1>📚 Library Management System</h1>

          <h2>Reset Your Password</h2>

          <p>
            Your password reset request has been approved.
            Please enter a new password below.
          </p>

        </div>

        <form
          onSubmit={handleSubmit}
          className="create-password-form"
        >

          <input
            type="password"
            placeholder="Enter New Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
          />

          <input
            type="password"
            placeholder="Confirm New Password"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(e.target.value)
            }
            required
          />

          <button type="submit">
            Reset Password
          </button>

        </form>

        <div className="security-note">
          🔒 Your new password will be securely encrypted before being stored.
        </div>

      </div>

    </div>

  );
}

export default ResetPassword;