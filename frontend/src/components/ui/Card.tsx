import React from "react";

export const Card: React.FC<{
  title: string;
  footer?: React.ReactNode;
  children: React.ReactNode;
}> = ({ title, footer, children }) => (
  <div className="bg-white/80 backdrop-blur rounded-2xl shadow p-5 border border-slate-200">
    <h2 className="text-xl font-semibold mb-3">{title}</h2>
    <div className="space-y-3">{children}</div>
    {footer && (
      <div className="pt-4 mt-4 border-t border-slate-200">{footer}</div>
    )}
  </div>
);
