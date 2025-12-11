// src/theme/DocItem/index.js
import React from "react";
import OriginalDocItem from "@theme-original/DocItem";
import DeleteButton from "@site/src/components/DeleteButton";

/**
 * Wrapper around the default DocItem.
 * Adds Upload + Delete buttons for docs under:
 *   docs/modules/<module>/<team>/weekN.md
 */
export default function DocItemWrapper(props) {
  // Try to read metadata from the MDX content
  const metadata = props?.content?.metadata || props?.content?.frontMatter || {};

  // Some Docusaurus setups expose different fields for source path
  const sourceHint =
    metadata?.source ||
    metadata?.sourceFilePath ||
    metadata?.sourcePath ||
    null;

  // URL path (for fallback parsing)
  let pathname = "";
  if (typeof window !== "undefined") {
    pathname = window.location.pathname; // e.g. /docs/modules/module1/teamA/week1
  } else {
    pathname = metadata?.permalink || "";
  }

  // Helper to extract {module, team, week} from a path-like string
  function extractParts(p) {
    if (!p) return null;

    const normalized = p.replace(/^\/+|\/+$/g, ""); // trim leading/trailing /
    const parts = normalized.split("/").filter(Boolean);

    // Look for "modules" in path: docs/modules/module1/teamA/week1.md
    const idx = parts.indexOf("modules");
    if (idx >= 0 && parts.length >= idx + 4) {
      const moduleName = parts[idx + 1];
      const team = parts[idx + 2];
      const weekRaw = parts[idx + 3]; // week1, week-01.md, etc.
      const week = weekRaw.replace(/\.mdx?$/i, "").replace(/\.md$/i, "");
      return { module: moduleName, team, week };
    }

    // Fallback: docs/module1/teamA/week1
    const idxDocs = parts.indexOf("docs");
    if (idxDocs >= 0 && parts.length >= idxDocs + 4) {
      const moduleName = parts[idxDocs + 1];
      const team = parts[idxDocs + 2];
      const weekRaw = parts[idxDocs + 3];
      const week = weekRaw.replace(/\.mdx?$/i, "").replace(/\.md$/i, "");
      return { module: moduleName, team, week };
    }

    return null;
  }

  // Try from source path, then from URL
  let info = extractParts(sourceHint) || extractParts(pathname);

  // Final fallback: use metadata.id like "modules/module1/teamA/week1"
  if (!info && metadata?.id) {
    const idParts = metadata.id.split("/").filter(Boolean);
    const idx = idParts.indexOf("modules");
    if (idx >= 0 && idParts.length >= idx + 4) {
      info = {
        module: idParts[idx + 1],
        team: idParts[idx + 2],
        week: idParts[idx + 3],
      };
    }
  }

  // ✅ Define showControls INSIDE the component (this was missing / moved earlier)
  const showControls =
    !!info &&
    info.module?.startsWith("module") &&
    info.team &&
    info.week &&
    /week/i.test(info.week);

  return (
    <div>
      {showControls && (
        <div style={{ marginBottom: 12, display: "flex", gap: "0.5rem" }}>
          <a
            href={`/upload?module=${info.module}&team=${info.team}&week=${info.week}`}
            className="button button--secondary"
          >
            📤 Upload Doc
          </a>
          <DeleteButton module={info.module} team={info.team} week={info.week} />
        </div>
      )}

      {/* Render the original doc content */}
      <OriginalDocItem {...props} />
    </div>
  );
}