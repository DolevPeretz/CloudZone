import { useMemo } from "react";
import { createApiClient } from "./lib/api";
import { useLocalStorage } from "./lib/useLocalStorage";
import { Settings } from "./features/settings/Settings";
import { AddIdForm } from "./features/add/AddIdForm";
import { CheckIdForm } from "./features/check/CheckIdForm";
import { DeleteIdForm } from "./features/delete/DeleteIdForm";
import { Toaster } from "react-hot-toast";

export default function App() {
  const [baseUrl, setBaseUrl] = useLocalStorage(
    "api_base_url",
    import.meta?.env?.VITE_DEFAULT_API_BASE_URL || ""
  );
  const [apiKey, setApiKey] = useLocalStorage(
    "api_key",
    import.meta?.env?.VITE_DEFAULT_API_KEY || ""
  );
  const api = useMemo(
    () => createApiClient(baseUrl, apiKey),
    [baseUrl, apiKey]
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-100 to-slate-200">
      <Toaster position="top-center" />
      <div className="max-w-5xl mx-auto px-4 py-8">
        <header className="mb-6">
          <h1 className="text-2xl font-bold">Customer IDs Console</h1>
          <p className="text-slate-600">
            ניהול מזהים: הוספה, בדיקה ומחיקה מול ה־API שלך.
          </p>
        </header>

        <div className="space-y-6">
          <Settings
            baseUrl={baseUrl}
            setBaseUrl={setBaseUrl}
            apiKey={apiKey}
            setApiKey={setApiKey}
          />

          <div className="grid md:grid-cols-3 gap-4">
            <AddIdForm api={api} />
            <CheckIdForm api={api} />
            <DeleteIdForm api={api} />
          </div>

          <div className="bg-white/60 rounded-2xl p-4 border border-slate-200">
            <ol className="list-decimal pl-5 space-y-2 text-sm text-slate-700">
              <li>
                הדביקי למעלה את ה־Invoke URL של API Gateway (Stage: prod) ואת
                ה־x-api-key אם נדרש.
              </li>
              <li>
                PUT שולח גוף JSON: {`{ id: "..." }`} · GET/DELETE שולחים query
                param: <code>?id=...</code>.
              </li>
              <li>
                ב-API Gateway הפעילי CORS ל:{" "}
                <code>GET, PUT, DELETE, OPTIONS</code> + headers:{" "}
                <code>Content-Type, X-Api-Key</code>.
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}
