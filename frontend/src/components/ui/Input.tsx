import React from "react";

export const LabeledInput: React.FC<{
  label: string;
  value?: string;
  placeholder?: string;
  disabled?: boolean;
  onChange?: React.ChangeEventHandler<HTMLInputElement>;
}> = ({ label, ...props }) => (
  <label className="block">
    <span className="text-sm text-slate-700">{label}</span>
    <input
      {...props}
      className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400 disabled:bg-slate-100"
    />
  </label>
);
