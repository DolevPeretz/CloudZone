import React from "react";
import { Card } from "../../components/ui/Card";
import { LabeledInput } from "../../components/ui/Input";
import { Status } from "../../components/ui/Status";

export const Settings: React.FC<{
  baseUrl: string;
  setBaseUrl: (v: string) => void;
  apiKey: string;
  setApiKey: (v: string) => void;
}> = ({ baseUrl, setBaseUrl, apiKey, setApiKey }) => (
  <Card title="הגדרות חיבור ל־API">
    <div className="grid md:grid-cols-2 gap-3">
      <LabeledInput
        label="API Base URL (Invoke URL)"
        value={baseUrl}
        onChange={(e) => setBaseUrl(e.target.value)}
        placeholder="https://xxxxxx.execute-api.eu-central-1.amazonaws.com/prod"
      />
      <LabeledInput
        label="x-api-key (אם יש)"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="מפתח API או ריק אם אין"
      />
    </div>
    <Status
      kind="info"
      text="מפתחות בצד לקוח גלויים; ודאי Usage Plan/Throttling ו-CORS ב-API Gateway. לפרודקשן שקלי חתימה בצד-שרת."
    />
  </Card>
);
