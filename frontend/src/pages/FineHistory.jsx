import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

function FineHistory() {
  const { userId } = useParams();

  const navigate = useNavigate();

  const [history, setHistory] = useState([]);

  const [totalFine, setTotalFine] = useState(0);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get(
          `transactions/reports/fine-history/${userId}/`,
        );

        setHistory(response.data.history);
        setTotalFine(response.data.total_fine);

        
      } catch (error) {
        console.log(error.response?.data);
      }
    };

    fetchHistory();
  }, [userId]);

  return (
    <div className="page-container">
      <div className="books-card">
        <h1>Fine History</h1>

        <h3>Total Fine : ₹{totalFine}</h3>

        <table>
          <thead>
            <tr>
              <th>Book</th>

              <th>Issue Date</th>

              <th>Due Date</th>

              <th>Return Date</th>

              <th>Late Days</th>

              <th>Fine / Day</th>

              <th>Total Fine</th>
            </tr>
          </thead>

          <tbody>
            {history.map((item, index) => (
              <tr key={index}>
                <td>{item.book_title}</td>

                <td>{item.issue_date}</td>

                <td>{item.due_date}</td>

                <td>{item.return_date}</td>

                <td>{item.late_days}</td>

                <td>₹{item.fine_per_day}</td>

                <td>₹{item.fine_amount}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <button className="back-btn" onClick={() => navigate("/fine-summary")}>
          ← Back
        </button>
      </div>
    </div>
  );
}

export default FineHistory;
