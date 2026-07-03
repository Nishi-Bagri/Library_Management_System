import { useState } from "react";
import api from "../services/api";

function ChatBot() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");

  const sendMessage = async () => {
    if (!message.trim()) return;

    try {
      const res = await api.post("chat/", {
        message: message,
      });

      setReply(res.data.reply);
    } catch (error) {
      console.error(error);
      setReply("Something went wrong.");
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        bottom: 20,
        right: 20,
        width: 320,
        background: "#fff",
        border: "1px solid #ddd",
        borderRadius: 10,
        padding: 15,
        boxShadow: "0 0 10px rgba(0,0,0,.2)",
        zIndex: 9999,
      }}
    >
      <h3>🤖 Library Assistant</h3>

      <input
        type="text"
        placeholder="Type a message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{
          width: "100%",
          padding: "8px",
          marginBottom: "10px",
        }}
      />

      <button onClick={sendMessage}>Send</button>

      <hr />

      <strong>Bot:</strong>

      <p>{reply}</p>
    </div>
  );
}

export default ChatBot;