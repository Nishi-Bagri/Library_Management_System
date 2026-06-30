import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Librarians() {
  const navigate = useNavigate();

  const [librarians, setLibrarians] = useState([]);

  const [search, setSearch] = useState("");

  useEffect(() => {
  const fetchLibrarians = async () => {
    try {
      const token = localStorage.getItem("access");

      const response = await api.get("accounts/librarians/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setLibrarians(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  fetchLibrarians();
}, []);

  const filteredLibrarians = librarians.filter(
    (librarian) =>
      librarian.username.toLowerCase().includes(search.toLowerCase()) ||
      librarian.email.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="page-container">

      <div className="books-card">
        <h1>Librarians</h1>

        <input
          className="search-box"
          type="text"
          placeholder="Search librarian..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <table>
          <thead>
            <tr>
              <th>Username</th>

              <th>Email</th>

              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {filteredLibrarians.length > 0 ? (
              filteredLibrarians.map((librarian) => (
                <tr key={librarian.id}>
                  <td>{librarian.username}</td>

                  <td>{librarian.email}</td>

                  <td>{librarian.is_active ? "Active" : "Inactive"}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3">No librarians found</td>
              </tr>
            )}
          </tbody>
        </table>

        <button className="back-btn" onClick={() => navigate("/admin")}>
          ← Dashboard
        </button>
      </div>
    </div>
  );
}

export default Librarians;
