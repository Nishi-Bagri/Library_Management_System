import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard";
import LibrarianDashboard from "./pages/LibrarianDashboard";
import UserDashboard from "./pages/UserDashboard";
import Books from "./pages/Books";
import IssuedBooks from "./pages/IssuedBooks";
import CreatePassword from "./pages/CreatePassword";
import IssueBook from "./pages/IssueBook";
import Reports from "./pages/Reports";
import ForgotPassword from "./pages/ForgotPassword";
import Register from "./pages/Register";
import PasswordResetRequests from "./pages/PasswordResetRequests";
import ResetPassword from "./pages/ResetPassword";
import Users from "./pages/Users";
import Librarians from "./pages/Librarians";
import FineSummary from "./pages/FineSummary";
import FineHistory from "./pages/FineHistory";
import DeactivationRequests from "./pages/DeactivationRequests";
import RequestDeactivation from "./pages/RequestDeactivation";
import Settings from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/librarian" element={<LibrarianDashboard />} />
        <Route path="/user" element={<UserDashboard />} />
        <Route path="/books" element={<Books />} />
        <Route path="/issue-book" element={<IssueBook />} />
        <Route path="/issued-books" element={<IssuedBooks />} />
        <Route
          path="/create-password/:token"
          element={<CreatePassword />}
        />
        <Route path="/reports" element={<Reports />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/password-reset-requests"
          element={<PasswordResetRequests />}
        />
        <Route
          path="/reset-password/:token"
          element={<ResetPassword />}
        />
        <Route path="/users" element={<Users />} />
        <Route path="/librarians" element={<Librarians />} />
        <Route path="/fine-summary" element={<FineSummary />} />
        <Route
          path="/fine-history/:userId"
          element={<FineHistory />}
        />
        <Route
          path="/deactivation-requests"
          element={<DeactivationRequests />}
        />
        <Route
          path="/request-deactivation"
          element={<RequestDeactivation />}
        />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;