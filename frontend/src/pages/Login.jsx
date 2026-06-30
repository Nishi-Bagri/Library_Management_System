import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import libraryImage from "../assets/library.jpg";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const [welcomeText] = useState(() => {
    const showWelcome = sessionStorage.getItem("showWelcome");

    if (showWelcome === "true") {
      sessionStorage.removeItem("showWelcome");
      return "Welcome";
    }

    return "Welcome Back!";
  });

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("accounts/login/", {
        username,
        password,
      });

      // Store authentication details
      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);
      localStorage.setItem("role", response.data.role);

      // Redirect based on role
      if (response.data.role === "ADMIN") {
        navigate("/admin");
      } else if (response.data.role === "LIBRARIAN") {
        navigate("/librarian");
      } else {
        navigate("/user");
      }
    } catch (error) {
      console.log(error.response?.data);

      setErrorMessage(
        error.response?.data?.error ||
          error.response?.data?.detail ||
          "Invalid username or password.",
      );
    }
  };

  return (
    <div className="login-page">
      <div className="login-wrapper">
        {/* Left Side */}
        <div
          className="login-left"
          style={{
            backgroundImage: `
              linear-gradient(
                rgba(22,163,74,0.80),
                rgba(21,128,61,0.80)
              ),
              url(${libraryImage})
            `,
          }}
        >
          <div className="overlay">
            <h1>📚</h1>

            <h2>{welcomeText}</h2>

            <p>Library Management System</p>

            <div className="features">
              <div>📖 Manage Books</div>
              <div>👥 Manage Users</div>
              <div>📊 Reports</div>
            </div>
          </div>
        </div>

        {/* Right Side */}
        <div className="login-right">
          <h1>Login</h1>

          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Enter Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {errorMessage && <p className="login-error">{errorMessage}</p>}

            <button type="submit">Login</button>

            <p
              className="forgot-password"
              onClick={() => navigate("/forgot-password")}
            >
              Forgot Password?
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
