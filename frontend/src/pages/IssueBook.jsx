import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function IssueBook() {
  const navigate = useNavigate();

  const [users, setUsers] = useState([]);
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [userSummary, setUserSummary] = useState(null);

  const [issueData, setIssueData] = useState({
    user: "",
    book: "",
  });

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("access");

        // Users
        const usersResponse = await api.get("accounts/users/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log("Users:", usersResponse.data);

        // Supports both paginated and non-paginated responses
        if (usersResponse.data.results) {
          setUsers(usersResponse.data.results);
        } else {
          setUsers(usersResponse.data);
        }

        // Books
        const booksResponse = await api.get("books/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (booksResponse.data.results) {
          setBooks(booksResponse.data.results);
        } else {
          setBooks(booksResponse.data);
        }

      } catch (error) {
        console.log("Error:", error.response?.data);
        console.log(error);
      }
    };

    fetchData();
  }, []);

  const handleIssueBook = async () => {
    try {
      const token = localStorage.getItem("access");

      await api.post("transactions/", issueData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setMessage("✅ Book issued successfully!");
      setMessageType("success");

      setIssueData({
        user: "",
        book: "",
      });

      setSelectedBook(null);
      setUserSummary(null);

      setTimeout(() => {
        setMessage("");
      }, 3000);

    } catch (error) {
      setMessage("❌ Failed to issue book.");
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

  return (
    <div className="page-container">
      <div className="form-card">
        <h1>Issue Book</h1>

        <p className="form-subtitle">
          Assign books to library members
        </p>

        <div className="form-group">
          <label>Select User</label>

          <select
            value={issueData.user}
            onChange={async (e) => {
              const userId = e.target.value;

              setIssueData({
                ...issueData,
                user: userId,
              });

              try {
                const response = await api.get(
                  `transactions/user-summary/${userId}/`
                );

                setUserSummary(response.data);

              } catch (error) {
                console.log(error.response?.data);
              }
            }}
          >
            <option value="">Select User</option>

            {users.map((user) => (
              <option
                key={user.id}
                value={user.id}
              >
                {user.username} ({user.role})
              </option>
            ))}
          </select>
        </div>

        {userSummary && (
          <div className="info-card">
            <h3>User Information</h3>

            <p>
              <strong>Books Issued:</strong>{" "}
              {userSummary.books_issued} / 3
            </p>

            <p>
              <strong>Remaining Limit:</strong>{" "}
              {userSummary.remaining_limit}
            </p>

            <p>
              <strong>Overdue Books:</strong>{" "}
              {userSummary.overdue_books}
            </p>
          </div>
        )}

        <div className="form-group">
          <label>Select Book</label>

          <select
            value={issueData.book}
            onChange={(e) => {
              const bookId = Number(e.target.value);

              setIssueData({
                ...issueData,
                book: bookId,
              });

              const book = books.find(
                (b) => b.id === bookId
              );

              setSelectedBook(book);
            }}
          >
            <option value="">
              Select Book
            </option>

            {books.map((book) => (
              <option
                key={book.id}
                value={book.id}
              >
                {book.title}
              </option>
            ))}
          </select>
        </div>

        {selectedBook && (
          <div className="info-card">
            <h3>Book Information</h3>

            <p><strong>Serial No:</strong> {selectedBook.serial_no}</p>
            <p><strong>Title:</strong> {selectedBook.title}</p>
            <p><strong>Author:</strong> {selectedBook.author}</p>
            <p><strong>Category:</strong> {selectedBook.category}</p>
            <p><strong>Total Pages:</strong> {selectedBook.total_pages}</p>
            <p><strong>Available Copies:</strong> {selectedBook.available_quantity}</p>
          </div>
        )}

        <button
          className="submit-btn"
          onClick={handleIssueBook}
        >
          Issue Book
        </button>

        {message && (
          <p
            className={
              messageType === "success"
                ? "success-message"
                : "error-message"
            }
          >
            {message}
          </p>
        )}

        <button
          className="back-btn"
          onClick={handleBack}
        >
          ← Dashboard
        </button>
      </div>
    </div>
  );
}

export default IssueBook;