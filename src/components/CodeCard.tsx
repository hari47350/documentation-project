import React from "react";
import CodeBlock from "@theme/CodeBlock";

type CodeCardProps = {
  language?: string;
  title?: string;
  filename?: string;
  children: string;
};

export default function CodeCard({
  language = "javascript",
  title = "Code snippet",
  filename,
  children,
}: CodeCardProps) {
  const fileLabel = filename || title;

  return (
    <div className="code-panel" role="region" aria-label={title}>
      <div className="panel-controls" aria-hidden="true">
        <div className="panel-meta">
          <span className="pill">
            <span className="dot" aria-hidden="true" />
            {language.toUpperCase()}
          </span>
          {fileLabel && (
            <span className="label">
              <code>{fileLabel}</code>
            </span>
          )}
        </div>
        <div className="actions" role="toolbar" aria-label="Code actions">
          <button
            type="button"
            className="action-btn"
            onClick={() => alert("Explain feature is not wired yet.")}
          >
            Explain
          </button>
        </div>
      </div>

      {/* Built-in Docusaurus CodeBlock → Prism + copy button + line numbers */}
      <CodeBlock language={language} showLineNumbers={true}>
        {children}
      </CodeBlock>
    </div>
  );
}