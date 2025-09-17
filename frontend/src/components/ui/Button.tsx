import React from "react";

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  loading?: boolean;
};

export const Button: React.FC<Props> = ({
  className = "",
  loading = false,
  children,
  ...props
}) => (
  <button
    {...props}
    disabled={loading || props.disabled}
    className={
      `inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 font-medium border transition ` +
      `${
        loading || props.disabled
          ? "bg-slate-200 text-slate-500 border-slate-200 cursor-not-allowed"
          : "bg-slate-900 text-white border-slate-900 hover:opacity-90"
      } ` +
      className
    }
  >
    {loading && (
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/80 border-t-transparent" />
    )}
    {children}
  </button>
);
