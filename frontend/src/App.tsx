import React, { useState } from "react";

const API_URL = "http://localhost:8000";

function App() {
  const [documents, setDocuments] = useState("");
  const [files, setFiles] = useState<FileList | null>(null);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleRemoveFile = (idx: number) => {
    if (!files) return;
    const fileArr = Array.from(files);
    fileArr.splice(idx, 1);
    const dt = new DataTransfer();
    fileArr.forEach(f => dt.items.add(f));
    setFiles(dt.files);
  };

  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleSelectFiles = () => {
    fileInputRef.current?.click();
  };

  const handleIngest = async () => {
    setLoading(true);
    let docsString = "";
    if (files && files.length > 0) {
      const fileContents = await Promise.all(
        Array.from(files).map(file =>
          new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = () => reject(reader.error);
            reader.readAsText(file);
          })
        )
      );
      docsString = fileContents.join("\n");
    } else {
      docsString = documents;
    }
    await fetch(`${API_URL}/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ documents: docsString.split("\n").filter(Boolean) })
    });
    setLoading(false);
    alert("Documents ingested!");
  };

  const handleQuery = async () => {
    setLoading(true);
    const res = await fetch(`${API_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    setAnswer(data.answer);
    setDocs(data.documents);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>RAG Demo</h1>
      <h2>Ingest Documents</h2>
      <div style={{ marginBottom: "1rem" }}>
        <button
          type="button"
          style={{ width: "100%", padding: "0.75rem", fontSize: "1rem", cursor: "pointer" }}
          onClick={handleSelectFiles}
        >
          Select Files
        </button>
      </div>
      {files && files.length > 0 && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            overflowY: "auto",
            gap: "0.5rem",
            marginBottom: "1rem",
            maxHeight: "200px",
            paddingBottom: "0.5rem"
          }}
        >
          {Array.from(files).map((file, idx) => (
            <div
              key={file.name + idx}
              style={{
                minHeight: "40px",
                maxHeight: "60px",
                width: "95%",
                border: "1px solid #ccc",
                borderRadius: "8px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                background: "#f9f9f9",
                fontSize: "0.95rem",
                boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
                whiteSpace: "nowrap",
                paddingLeft: "1rem",
                paddingRight: "0.5rem"
              }}
            >
              <span>{file.name}</span>
              <button
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#888",
                  fontSize: "1.2rem",
                  cursor: "pointer",
                  marginLeft: "1rem"
                }}
                onClick={() => handleRemoveFile(idx)}
                aria-label={`Remove ${file.name}`}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}
      <button
        onClick={handleIngest}
        disabled={loading || !(files && files.length > 0)}
      >
        Ingest
      </button>
      <h2>Ask a Question</h2>
      <input
        style={{ width: "100%" }}
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Enter your question"
      />
      <button onClick={handleQuery} disabled={loading || !query.trim()}>
        Query
      </button>
      {loading && <p>Loading...</p>}
      {answer && (
        <div>
          <h3>Answer</h3>
          <p>{answer}</p>
          <h4>Retrieved Documents</h4>
          <ul>
            {docs.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
