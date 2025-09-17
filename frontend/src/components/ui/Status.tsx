import React from "react";
import type { StatusKind } from "../../lib/types";

export const Status: React.FC<{ kind?: StatusKind; text?: string | null }> = ({
  kind = "info",
  text,
}) => {
  if (!text) return null;
  const cls =
    kind === "error"
      ? "bg-red-50 text-red-700 border-red-200"
      : kind === "success"
      ? "bg-green-50 text-green-700 border-green-200"
      : "bg-slate-50 text-slate-700 border-slate-200";
  return (
    <div className={`rounded-xl border px-3 py-2 text-sm ${cls}`}>{text}</div>
  );
};
