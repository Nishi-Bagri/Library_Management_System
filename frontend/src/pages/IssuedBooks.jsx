import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Swal from "sweetalert2";

function IssuedBooks() {
  const navigate = useNavigate();

  const [issuedBooks, setIssuedBooks] = useState([]);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  const [search, setSearch] = useState("");

  const loadIssuedBooks = async () => {
    try {
      const response = await api.get("transactions/");
      console.log(JSON.stringify(response.data, null, 2));
      setIssuedBooks(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("transactions/");
        setIssuedBooks(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchData();
  }, []);

  const handleReturn = async (id) => {
    const token = localStorage.getItem("access");

    try {
      // First attempt to return the book
      await api.post(
        `transactions/${id}/return/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      await Swal.fire({
        icon: "success",
        title: "Book Returned",
        text: "The book has been returned successfully.",
        confirmButtonColor: "#198754",
      });

      loadIssuedBooks();
    } catch (error) {
      const data = error.response?.data;

      console.log("Status:", error.response?.status);
      console.log("Response:", data);

      // If the book is overdue, ask for fine confirmation
      if (data?.overdue) {
        const result = await Swal.fire({
          title: "Fine Payment",
          html: `
          <div style="text-align:left">
            <p><strong>⚠ Book is overdue!</strong></p>
            <hr>
            <p><b>Late Days:</b> ${data.late_days}</p>
            <p><b>Fine / Day:</b> ₹${data.fine_per_day}</p>
            <p><b>Total Fine:</b>
              <span style="color:red;font-size:18px;">
                ₹${data.fine_amount}
              </span>
            </p>
            <br>
            <p>Has the fine been paid?</p>
          </div>
        `,
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Yes",
          cancelButtonText: "No",
          confirmButtonColor: "#198754",
          cancelButtonColor: "#dc3545",
          reverseButtons: true,
        });

        // Librarian clicked YES
        if (result.isConfirmed) {
          try {
            await api.post(
              `transactions/${id}/return/`,
              {
                fine_collected: true,
              },
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              },
            );

            await Swal.fire({
              icon: "success",
              title: "Book Returned",
              text: "The fine has been collected and the book has been returned successfully.",
              confirmButtonColor: "#198754",
            });

            loadIssuedBooks();
          } catch (error) {
            await Swal.fire({
              icon: "error",
              title: "Return Failed",
              text: error.response?.data?.error || "Failed to return the book.",
              confirmButtonColor: "#dc3545",
            });
          }
        } else {
          // Librarian clicked NO
          await Swal.fire({
            icon: "info",
            title: "Return Cancelled",
            text: "Please collect the fine before returning the book.",
            confirmButtonColor: "#0d6efd",
          });
        }

        return;
      }

      // Handle other errors
      await Swal.fire({
        icon: "error",
        title: "Return Failed",
        text: data?.error || "Failed to return the book.",
        confirmButtonColor: "#dc3545",
      });
    }
  };

  const handleRenew = async (id) => {
    console.log("Renew clicked for ID:", id);

    try {
      const token = localStorage.getItem("access");

      await api.post(
        `transactions/${id}/renew/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      setMessage("✅ Book renewed successfully!");
      setMessageType("success");

      loadIssuedBooks();
    } catch (error) {
      setMessage("❌ Failed to renew book.");
      setMessageType("error");

      console.log(error.response?.data);
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

  const filteredBooks = issuedBooks.filter(
    (issue) =>
      issue.user_name?.toLowerCase().includes(search.toLowerCase()) ||
      issue.book_name?.toLowerCase().includes(search.toLowerCase()) ||
      issue.display_status?.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="page-container">
      <div className="books-card">
        <h1>Issued Books</h1>

        <input
          type="text"
          className="search-box"
          placeholder="Search by user, book or status..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {message && (
          <p
            className={
              messageType === "success" ? "success-message" : "error-message"
            }
          >
            {message}
          </p>
        )}

        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Book</th>
              <th>Issue Date</th>
              <th>Due Date</th>
              <th>Status</th>
              <th>Renewals</th>
              <th>Overdue Days</th>
              <th>Fine/Day</th>
              <th>Total Fine</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {filteredBooks.length > 0 ? (
              filteredBooks.map((issue) => (
                <tr key={issue.id}>
                  <td>{issue.user_name}</td>
                  <td>{issue.book_name}</td>
                  <td>{issue.issue_date}</td>
                  <td>{issue.due_date}</td>

                  <td>
                    <span
                      className={`status ${issue.display_status.toLowerCase()}`}
                    >
                      {issue.display_status}
                    </span>
                  </td>

                  <td>{issue.renewal_count}</td>

                  <td>{issue.late_days}</td>

                  <td>₹{issue.fine_per_day}</td>

                  <td>₹{issue.fine_amount}</td>

                  <td>
                    {issue.status !== "RETURNED" ? (
                      <div className="action-buttons">
                        <button
                          className="edit-btn"
                          onClick={() => handleReturn(issue.id)}
                        >
                          Return
                        </button>

                        <button
                          className="delete-btn"
                          onClick={() => handleRenew(issue.id)}
                        >
                          Renew
                        </button>
                      </div>
                    ) : (
                      "-"
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="8">No issued books found</td>
              </tr>
            )}
          </tbody>
        </table>

        <button className="back-btn" onClick={handleBack}>
          ← Dashboard
        </button>
      </div>
    </div>
  );
}

export default IssuedBooks;
