import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import api from "../services/api";

function RequestDeactivation() {
  const navigate = useNavigate();

  const [reason, setReason] = useState("");
  const [remarks, setRemarks] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("access");

      await api.post(
        "accounts/deactivation-request/",
        {
          reason,
          remarks,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      Swal.fire({
        icon: "success",
        title: "Request Submitted",
        text: "Your account deactivation request has been submitted successfully.",
      });

      navigate("/user");

    } catch (error) {

      Swal.fire({
        icon: "error",
        title: "Error",
        text:
          error.response?.data?.error ||
          "Unable to submit request.",
      });
    }
  };

  return (
    <div className="page-container">
      <div className="books-card">

        <h1>Request Account Deactivation</h1>

        <form onSubmit={handleSubmit}>

          <label>Reason</label>

          <select
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            required
          >
            <option value="">Select Reason</option>
            <option value="NO_LONGER_USING">
              No Longer Using Library
            </option>
            <option value="MOVING">
              Moving to Another City
            </option>
            <option value="PRIVACY">
              Privacy Concerns
            </option>
            <option value="DUPLICATE">
              Duplicate Account
            </option>
            <option value="OTHER">
              Other
            </option>
          </select>

          <br /><br />

          <label>Remarks</label>

          <textarea
            rows="4"
            value={remarks}
            onChange={(e) => setRemarks(e.target.value)}
            placeholder="Additional remarks..."
          />

          <br /><br />

          <button className="edit-btn" type="submit">
            Submit Request
          </button>

          <button
            type="button"
            className="back-btn"
            onClick={() => navigate("/user")}
          >
            Cancel
          </button>

        </form>

      </div>
    </div>
  );
}

export default RequestDeactivation;