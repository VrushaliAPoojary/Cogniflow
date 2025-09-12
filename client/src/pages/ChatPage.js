import React, { useState } from "react";
import { queryAPI, uploadFile } from "../api";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);

  const send = async () => {
    if (!input) return;
    setMessages((m) => [...m, { sender: "you", text: input }]);
    try {
      const res = await queryAPI(input, true);
      setMessages((m) => [...m, { sender: "you", text: input }, { sender: "bot", text: res.data.answer }]);
      setInput("");
    } catch (err) {
      console.error(err);
      setMessages((m) => [...m, { sender: "bot", text: "Error calling API" }]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    const resp = await uploadFile(file);
    alert("Uploaded: " + resp.data.filename);
  };

  return (
    <div style={{ padding: 16 }}>
      <h2>Chat</h2>
      <div style={{ border: "1px solid #ddd", padding: 8, height: 400, overflow: "auto" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ textAlign: m.sender === "you" ? "right" : "left" }}>
            <b>{m.sender}:</b> {m.text}
          </div>
        ))}
      </div>

      <div style={{ marginTop: 12 }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask a question..." style={{ width: "70%" }} />
        <button onClick={send}>Send</button>
      </div>

      <div style={{ marginTop: 12 }}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload PDF</button>
      </div>
    </div>
  );
}
