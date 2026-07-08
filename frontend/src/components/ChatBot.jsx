import { useState } from "react";
import api from "../services/api";

function ChatBot() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: `👋 Welcome to LibraryGPT!

I'm your AI-powered Library Assistant.

I can help you with:

📚 Search books
👤 Find books by author
📖 Explore book categories
📘 View book details
❓ Answer library-related questions
💡 Recommend books

Try asking:

• Search Python books
• Show available books
• Books by Eric Matthes
• Tell me about Clean Code
• What is the fine policy?`,
    },
  ]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const res = await api.post("chat/", {
        message: userMessage,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: res.data.reply,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "⚠️ Something went wrong.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        position: "fixed",
        bottom: 20,
        right: 20,
        width: 350,
        background: "#fff",
        border: "1px solid #ddd",
        borderRadius: 12,
        padding: 15,
        boxShadow: "0 4px 12px rgba(0,0,0,.2)",
        zIndex: 9999,
      }}
    >
      <h3 style={{ marginTop: 0 }}>🤖 LibraryGPT</h3>

      <div
        style={{
          height: 320,
          overflowY: "auto",
          border: "1px solid #eee",
          padding: 10,
          marginBottom: 10,
          borderRadius: 8,
          background: "#fafafa",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              marginBottom: 12,
            }}
          >
            <div
              style={{
                display: "inline-block",
                maxWidth: "90%",
                padding: "10px 12px",
                borderRadius: 10,
                background:
                  msg.sender === "user" ? "#d1f5d3" : "#f1f1f1",
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ marginTop: 10 }}>
            🤖 <em>LibraryGPT is thinking...</em>
          </div>
        )}
      </div>

      <input
        type="text"
        placeholder="Ask something about the library..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            sendMessage();
          }
        }}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
          borderRadius: 6,
          border: "1px solid #ccc",
          boxSizing: "border-box",
        }}
      />

      <button
        onClick={sendMessage}
        style={{
          width: "100%",
          padding: "10px",
          background: "#2e7d32",
          color: "#fff",
          border: "none",
          borderRadius: 6,
          cursor: "pointer",
        }}
      >
        Send
      </button>
    </div>
  );
}

export default ChatBot;