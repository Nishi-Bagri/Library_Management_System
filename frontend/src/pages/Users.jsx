import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Users() {
  const navigate = useNavigate();

  const [users, setUsers] = useState([]);

  const [search, setSearch] = useState("");

  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("access");

        const response = await api.get(`accounts/normal-users/?page=${page}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setUsers(response.data.results);
        setCount(response.data.count);
      } catch (error) {
        console.log(error);
      }
    };

    fetchUsers();
  }, [page]);

  const filteredUsers = users.filter(
    (user) =>
      user.username.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase()),
  );

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
      <div className="books-card">
        <h1>Users List</h1>

        <input
          className="search-box"
          type="text"
          placeholder="Search user..."
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
            {filteredUsers.length > 0 ? (
              filteredUsers.map((user) => (
                <tr key={user.id}>
                  <td>{user.username}</td>

                  <td>{user.email}</td>

                  <td>{user.is_active ? "Active" : "Inactive"}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3">No users found</td>
              </tr>
            )}
          </tbody>
        </table>

        <div className="pagination">
          <button disabled={page === 1} onClick={() => setPage(page - 1)}>
            Previous
          </button>

          <span>Page {page}</span>

          <button
            disabled={page * 10 >= count}
            onClick={() => setPage(page + 1)}
          >
            Next
          </button>
        </div>

        <button className="back-btn" onClick={handleBack}>
          ← Dashboard
        </button>
      </div>
    </div>
  );
}

export default Users;
