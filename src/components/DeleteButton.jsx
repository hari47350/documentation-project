// src/components/DeleteButton.jsx
import React, { useState } from "react";

/**
 * DeleteButton - small UI to call POST /delete/
 * module: "module1"
 * team:   "teamA"
 * week:   "week1"
 */
export default function DeleteButton({ module, team, week }) {
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleDelete() {
    if (!confirm("Are you sure? This will remove the current document (it will be backed up).")) {
      return;
    }
    setBusy(true);
    setStatus("Deleting...");

    try {
      const form = new FormData();
      form.append("module", module);
      form.append("team", team);
      form.append("week", week);

      const res = await fetch("http://localhost:9000/delete/", {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        const text = await res.text();
        setStatus("Delete failed: " + (text || res.statusText));
        setBusy(false);
        return;
      }
      const data = await res.json();
      if (data.ok) {
        setStatus("Deleted. Refreshing...");
        // small delay so user sees message
        setTimeout(() => window.location.reload(), 900);
      } else {
        setStatus("Delete failed: " + JSON.stringify(data));
        setBusy(false);
      }
    } catch (err) {
      setStatus("Error: " + String(err));
      setBusy(false);
    }
  }

  return (
    <div style={{ margin: "0.5rem 0 1rem 0" }}>
      <button
        onClick={handleDelete}
        disabled={busy}
        style={{
          background: "#ff4d4f",
          color: "white",
          padding: "8px 12px",
          borderRadius: 8,
          border: "none",
          cursor: busy ? "not-allowed" : "pointer",
          fontWeight: 700,
          marginRight: 12,
        }}
        title="Delete uploaded doc for this week (backup saved)"
      >
        🗑️ Delete this document
      </button>
      {status && (
        <span style={{ fontSize: 13, color: "#444", marginLeft: 6 }}>
          {status}
        </span>
      )}
    </div>
  );
}