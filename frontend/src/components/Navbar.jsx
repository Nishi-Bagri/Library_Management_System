import { useNavigate } from "react-router-dom";
import { FaBookOpen } from "react-icons/fa";

function Navbar() {
  const navigate = useNavigate();

  const role = localStorage.getItem("role");

  const handleLogout = () => {
    localStorage.clear();

    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="logo">
        <FaBookOpen className="logo-icon" />

        <span>Library Management System</span>
      </div>

      <div className="nav-links">
        {(role === "ADMIN" || role === "LIBRARIAN") && (
          <>
            <button className="nav-btn" onClick={() => navigate("/books")}>
              Manage Books
            </button>

            <button className="nav-btn" onClick={() => navigate("/register")}>
              Create User
            </button>

            <button className="nav-btn" onClick={() => navigate("/reports")}>
              Reports
            </button>
          </>
        )}

        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>

         <button className="nav-btn" onClick={() => navigate("/settings")}>
          ⚙️ Settings
        </button>
        
      </div>
    </nav>
  );
}

export default Navbar;
