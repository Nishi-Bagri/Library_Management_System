import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Swal from "sweetalert2";

function ForgotPassword() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");

  const handleVerify = async () => {
    try {
      const response = await api.post("accounts/forgot-password/", {
        username,
      });

      await Swal.fire({
        icon: "success",
        title: "Request Submitted",
        text: "Your password reset request has been submitted successfully. Please wait for Admin/Librarian approval. A password reset email will be sent to your registered email address after approval.",
        confirmButtonColor: "#16a34a",
      });

      navigate("/");

      if (response.data.user_exists) {
        navigate("/reset-password", {
          state: {
            username,
          },
        });
      }
    } catch (error) {
      console.log(error.response?.data);
      setMessage("❌ User not found.");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Forgot Password</h1>

        <input
          type="text"
          placeholder="Enter Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <button onClick={handleVerify}>Verify</button>

        {message && <p className="error-message">{message}</p>}
      </div>
    </div>
  );
}

export default ForgotPassword;
