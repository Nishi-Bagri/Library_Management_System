import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const PAGE_SIZE = 10; // change this to match your DRF PAGE_SIZE setting

function Books() {
  const navigate = useNavigate();

  const [books, setBooks] = useState([]);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  const [isEditing, setIsEditing] = useState(false);
  const [editBookId, setEditBookId] = useState(null);

  const [nextPage, setNextPage] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [count, setCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);

  const [deleteId, setDeleteId] = useState(null);

  const role = localStorage.getItem("role");

  const [bookData, setBookData] = useState({
    serial_no: "",
    title: "",
    author: "",
    category: "",
    total_pages: "",
    quantity: "",
    available_quantity: "",
  });

  const fetchBooks = async (page) => {
    try {
      const response = await api.get(`books/?page=${page}`);

      setBooks(response.data.results);
      setNextPage(response.data.next);
      setPreviousPage(response.data.previous);
      setCount(response.data.count);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchBooks(currentPage);
  }, [currentPage]);

  const handleEdit = (book) => {
    setBookData({
      serial_no: book.serial_no,
      title: book.title,
      author: book.author,
      category: book.category,
      total_pages: book.total_pages,
      quantity: book.quantity,
      available_quantity: book.available_quantity,
    });

    setEditBookId(book.id);
    setIsEditing(true);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    try {
      const token = localStorage.getItem("access");

      await api.delete(`books/${id}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // If we deleted the last item on this page and it's not page 1,
      // go back a page; otherwise refetch the current page.
      const isLastItemOnPage = books.length === 1 && currentPage > 1;
      const pageToFetch = isLastItemOnPage ? currentPage - 1 : currentPage;

      if (isLastItemOnPage) {
        setCurrentPage(pageToFetch);
      } else {
        await fetchBooks(pageToFetch);
      }

      setDeleteId(null);

      setMessage("✅ Book deleted successfully!");
      setMessageType("success");

      setTimeout(() => {
        setMessage("");
      }, 3000);
    } catch (error) {
      setMessage("❌ Failed to delete book.");
      setMessageType("error");

      console.log(error.response?.data);
    }
  };

  const handleAddBook = async () => {
    try {
      const token = localStorage.getItem("access");

      if (isEditing) {
        await api.put(`books/${editBookId}/`, bookData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setMessage("✅ Book updated successfully!");

        await fetchBooks(currentPage);
      } else {
        await api.post("books/", bookData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setMessage("✅ Book added successfully!");

        // New books typically appear on the last page; jump there.
        await fetchBooks(currentPage);
      }

      setMessageType("success");

      setIsEditing(false);
      setEditBookId(null);

      setTimeout(() => {
        setShowForm(false);
        setMessage("");
      }, 3000);

      setBookData({
        serial_no: "",
        title: "",
        author: "",
        category: "",
        total_pages: "",
        quantity: "",
        available_quantity: "",
      });
    } catch (error) {
      setMessage("❌ Operation failed.");
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

  const filteredBooks = books.filter(
    (book) =>
      book.title?.toLowerCase().includes(search.toLowerCase()) ||
      book.author?.toLowerCase().includes(search.toLowerCase()) ||
      book.category?.toLowerCase().includes(search.toLowerCase()),
  );

  const totalPages = Math.max(1, Math.ceil(count / PAGE_SIZE));

  const handlePreviousPage = () => {
    if (previousPage) {
      setCurrentPage((prev) => Math.max(1, prev - 1));
    }
  };

  const handleNextPage = () => {
    if (nextPage) {
      setCurrentPage((prev) => Math.min(totalPages, prev + 1));
    }
  };

  return (
    <div className="page-container">
      <div className="books-card">
        <h1>{role === "USER" ? "Library Books" : "Books Management"}</h1>

        <div className="books-header">
          <input
            type="text"
            className="search-box"
            placeholder="Search books by title, author or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          {(role === "ADMIN" || role === "LIBRARIAN") && (
            <button
              className="add-book-btn"
              onClick={() => setShowForm(!showForm)}
            >
              {showForm ? "Close" : "Add Book"}
            </button>
          )}
        </div>

        {search && (
          <p className="search-note">
            ⚠️ Search only applies to the current page (
            {filteredBooks.length} of {books.length} shown). For full
            results across all books, consider implementing server-side
            search.
          </p>
        )}

        {(role === "ADMIN" || role === "LIBRARIAN") && showForm && (
          <div className="form-card">
            <h2>{isEditing ? "Edit Book" : "Add New Book"}</h2>

            <br />

            <div className="book-form-grid">
              <div className="input-group">
                <label>Serial Number</label>

                <input
                  type="text"
                  placeholder="Enter serial number"
                  value={bookData.serial_no}
                  onChange={(e) =>
                    setBookData({
                      ...bookData,
                      serial_no: e.target.value,
                    })
                  }
                />
              </div>

              <div className="input-group">
                <label>Book Title</label>

                <input
                  type="text"
                  placeholder="Enter title"
                  value={bookData.title}
                  onChange={(e) =>
                    setBookData({
                      ...bookData,
                      title: e.target.value,
                    })
                  }
                />
              </div>

              <div className="input-group">
                <label>Author</label>

                <input
                  type="text"
                  placeholder="Enter author"
                  value={bookData.author}
                  onChange={(e) =>
                    setBookData({
                      ...bookData,
                      author: e.target.value,
                    })
                  }
                />
              </div>

              <div className="input-group">
                <label>Category</label>

                <input
                  type="text"
                  placeholder="Enter category"
                  value={bookData.category}
                  onChange={(e) =>
                    setBookData({
                      ...bookData,
                      category: e.target.value,
                    })
                  }
                />
              </div>

              <div className="input-group">
                <label>Total Pages</label>

                <input
                  type="number"
                  value={bookData.total_pages}
                  onChange={(e) =>
                    setBookData({
                      ...bookData,
                      total_pages: e.target.value,
                    })
                  }
                />
              </div>

              <div className="input-group">
                <label>Quantity</label>

                <input
                  type="number"
                  value={bookData.quantity}
                  onChange={(e) =>
                    setBookData({
                      ...bookData,
                      quantity: e.target.value,
                      available_quantity: e.target.value,
                    })
                  }
                />
              </div>
            </div>

            <button className="submit-btn" onClick={handleAddBook}>
              {isEditing ? "Update Book" : "Save Book"}
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
          </div>
        )}

        <table>
          <thead>
            <tr>
              <th>Serial No</th>
              <th>Title</th>
              <th>Author</th>
              <th>Category</th>
              <th>Total Pages</th>
              <th>Quantity</th>
              <th>Available</th>

              {(role === "ADMIN" || role === "LIBRARIAN") && <th>Actions</th>}
            </tr>
          </thead>

          <tbody>
            {filteredBooks.length > 0 ? (
              filteredBooks.map((book) => (
                <tr key={book.id || book.serial_no}>
                  <td>{book.serial_no}</td>
                  <td>{book.title}</td>
                  <td>{book.author}</td>
                  <td>{book.category}</td>
                  <td>{book.total_pages}</td>
                  <td>{book.quantity}</td>
                  <td>{book.available_quantity}</td>

                  <td>
                    {(role === "ADMIN" || role === "LIBRARIAN") && (
                      <>
                        <button
                          className="edit-btn"
                          onClick={() => handleEdit(book)}
                        >
                          Edit
                        </button>

                        <button
                          className="delete-btn"
                          onClick={() => setDeleteId(book.id)}
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7">No books found</td>
              </tr>
            )}
          </tbody>
        </table>

        {deleteId && (
          <div className="delete-confirmation">
            <p>⚠️ Are you sure you want to delete this book?</p>

            <div className="delete-actions">
              <button
                className="confirm-delete-btn"
                onClick={() => handleDelete(deleteId)}
              >
                Yes, Delete
              </button>

              <button
                className="cancel-delete-btn"
                onClick={() => setDeleteId(null)}
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        <div className="pagination-controls">
          <button
            className="pagination-btn"
            disabled={!previousPage}
            onClick={handlePreviousPage}
          >
            ← Previous
          </button>

          <span className="pagination-info">
            Page {currentPage} of {totalPages} ({count} total books)
          </span>

          <button
            className="pagination-btn"
            disabled={!nextPage}
            onClick={handleNextPage}
          >
            Next →
          </button>
        </div>

        <button className="back-btn" onClick={handleBack}>
          ← Dashboard
        </button>
      </div>
    </div>
  );
}

export default Books;
