// src/pages/index.js
import React from "react";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";

export default function Home() {
  return (
    <Layout
      title="SmartIDH Docs"
      description="Internal documentation and weekly reports for SmartIDH3"
    >
      <main
        style={{
          minHeight: "70vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "2rem 1rem",
        }}
      >
        <div style={{ maxWidth: 720, width: "100%", textAlign: "center" }}>
          <h1>Welcome to <strong>SmartIDH Documentation</strong></h1>

          <p>
            Browse weekly team documentation, notes all in one place.
          </p>

          <div style={{ marginTop: "1rem" }}>
            <Link className="button button--primary button--lg"
              to="/docs/modules/module1/teamA/week1">
              📚 Open Docs
            </Link>
            <span style={{ margin: "0 0.5rem" }}></span>
            <Link className="button button--secondary button--lg"
              to="/upload">
              📤 Upload Doc
            </Link>
          </div>
        </div>
      </main>
    </Layout>
  );
}