import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function FineSummary() {
  const navigate = useNavigate();

  const [summary, setSummary] = useState([]);
  const [search, setSearch] = useState("");

  const [totalFineCollected, setTotalFineCollected] = useState(0);
  const [usersWithFine, setUsersWithFine] = useState(0);
  const [totalFinedBooks, setTotalFinedBooks] = useState(0);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get(
          "transactions/reports/fine-summary/"
        );

        setSummary(response.data.results);
        setTotalFineCollected(response.data.total_fine_collected);
        setUsersWithFine(response.data.users_with_fine);
        setTotalFinedBooks(response.data.total_fined_books);
      } catch (error) {
        console.log(error.response?.data);
      }
    };

    fetchSummary();
  }, []);

  const filteredData = summary.filter((item) =>
    item.username.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="page-container">
      <div className="books-card">

        <h1>💰 Fine Collection</h1>

        {/* Summary Cards */}

        <div className="dashboard-grid">

          <div className="stat-card">
            <h3>Total Fine Collected</h3>
            <p>₹{totalFineCollected}</p>
          </div>

          <div className="stat-card">
            <h3>Users with Fine</h3>
            <p>{usersWithFine}</p>
          </div>

          <div className="stat-card">
            <h3>Total Fined Books</h3>
            <p>{totalFinedBooks}</p>
          </div>

        </div>

        {/* Search */}

        <input
          className="search-box"
          type="text"
          placeholder="🔍 Search User..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {/* Table */}

        <table>

          <thead>

            <tr>
              <th>Username</th>
              <th>Books With Fine</th>
              <th>Total Fine</th>
              <th>Action</th>
            </tr>

          </thead>

          <tbody>

            {filteredData.length > 0 ? (

              filteredData.map((item) => (

                <tr key={item.user}>

                  <td>{item.username}</td>

                  <td>{item.books_with_fine}</td>

                  <td>₹{item.total_fine}</td>

                  <td>

                    <button
                      className="edit-btn"
                      onClick={() =>
                        navigate(`/fine-history/${item.user}`)
                      }
                    >
                      View Details
                    </button>

                  </td>

                </tr>

              ))

            ) : (

              <tr>

                <td colSpan="4">
                  No users with fine found.
                </td>

              </tr>

            )}

          </tbody>

        </table>

        <button
          className="back-btn"
          onClick={() => navigate("/reports")}
        >
          ← Reports
        </button>

      </div>
    </div>
  );
}

export default FineSummary;