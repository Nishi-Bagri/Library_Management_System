import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { FaUser, FaEnvelope, FaUserTag } from "react-icons/fa";

function Register() {
  const navigate = useNavigate();

  const loggedInRole = localStorage.getItem("role");

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    role: "USER",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("access");

      const response = await api.post("accounts/users/", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log(response.data);

      setMessage("✅ User created successfully. Password setup email sent.");

      setFormData({
        username: "",
        email: "",
        role: "USER",
      });
    } catch (error) {
      console.log(error);

      if (error.response?.data?.error) {
        setMessage(`❌ ${error.response.data.error}`);
      } else {
        setMessage("❌ Failed to create user.");
      }
    }
  };

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

  return (
    <div className="page-container">
      <div className="form-card">
        <h1>Create User</h1>
        <p className="form-subtitle">Add a new library user account</p><br /><br></br>

        <form onSubmit={handleSubmit}>
          <div className="form-group-row">
            <label>
              <FaUser />
              Username
            </label>

            <input
              type="text"
              name="username"
              placeholder="Enter username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group-row">
            <label>
              {" "}
              <FaEnvelope />
              Email
            </label>

            <input
              type="email"
              name="email"
              placeholder="Enter email address"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group-row">
            <label>
              <FaUserTag />
              Role
            </label>

            <select name="role" value={formData.role} onChange={handleChange}>
              <option value="USER">USER</option>

              {loggedInRole === "ADMIN" && (
                <option value="LIBRARIAN">LIBRARIAN</option>
              )}
            </select>
            
          </div><br>
          </br>
          <button className="submit-btn" type="submit">
            Create User
          </button>
        </form>

        {message && <p className="message">{message}</p>}

        <button className="back-btn" onClick={handleBack}>
          ← Dashboard
        </button>
      </div>
    </div>
  );
}

export default Register;
