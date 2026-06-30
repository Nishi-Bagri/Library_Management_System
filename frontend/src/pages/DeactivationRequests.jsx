import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import api from "../services/api";

function DeactivationRequests() {
  const navigate = useNavigate();

  const [requests, setRequests] = useState([]);

  const [search, setSearch] = useState("");

  const loadRequests = async () => {
    try {
      const token = localStorage.getItem("access");

      const response = await api.get("accounts/deactivation-requests/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setRequests(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const token = localStorage.getItem("access");

        const response = await api.get("accounts/deactivation-requests/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setRequests(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchRequests();
  }, []);

  const handleApprove = async (id) => {
    const result = await Swal.fire({
      title: "Approve Account Deactivation Request?",
      text: "Are you sure you want to approve this request?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#198754",
      cancelButtonColor: "#dc3545",
      confirmButtonText: "Approve",
    });

    if (!result.isConfirmed) return;

    try {
      const token = localStorage.getItem("access");

      await api.post(
        `accounts/deactivation-request/${id}/approve/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      await Swal.fire({
        icon: "success",
        title: "Approved",
        text: "Account deactivation request approved successfully.",
        confirmButtonColor: "#198754",
      });

      loadRequests();
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.response?.data?.error || "Approval failed.",
      });
    }
  };

  const handleReject = async (id) => {
    const result = await Swal.fire({
      title: "Reject Account Deactivation?",
      text: "This request will be rejected.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Reject",
      confirmButtonColor: "#dc3545",
    });

    if (!result.isConfirmed) return;

    try {
      const token = localStorage.getItem("access");

      await api.post(
        `accounts/deactivation-request/${id}/reject/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      Swal.fire({
        icon: "success",
        title: "Rejected",
        text: "Account deactivation request rejected.",
      });

      loadRequests();
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: error.response?.data?.error || "Reject failed.",
      });
    }
  };

  const handleBack = () => {
    const role = localStorage.getItem("role");

    if (role === "ADMIN") {
      navigate("/admin");
    } else {
      navigate("/librarian");
    }
  };

  const filteredRequests = requests.filter((request) =>
    request.username?.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="page-container">
      <div className="books-card">
        <h1>Account Deactivation Requests</h1>

        <input
          type="text"
          className="search-box"
          placeholder="Search Username..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Reason</th>
              <th>Remarks</th>
              <th>Status</th>
              <th>Requested On</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {filteredRequests.length > 0 ? (
              filteredRequests.map((request) => (
                <tr key={request.id}>
                  <td>{request.username}</td>

                  <td>{request.reason}</td>

                  <td>{request.remarks || "-"}</td>

                  <td>
                    <span className={`status ${request.status.toLowerCase()}`}>
                      {request.status}
                    </span>
                  </td>

                  <td>{new Date(request.requested_at).toLocaleString()}</td>

                  <td>
                    {request.status === "PENDING" ? (
                      <div className="action-buttons">
                        <button
                          className="edit-btn"
                          onClick={() => handleApprove(request.id)}
                        >
                          Approve
                        </button>

                        <button
                          className="delete-btn"
                          onClick={() => handleReject(request.id)}
                        >
                          Reject
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
                <td colSpan="6">No account deactivation requests found.</td>
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

export default DeactivationRequests;
