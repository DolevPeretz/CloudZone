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
  <Card title="API Connection Settings">
    <div className="grid md:grid-cols-2 gap-3">
      <LabeledInput
        label="API Base URL (Invoke URL)"
        value={baseUrl}
        onChange={(e) => setBaseUrl(e.target.value)}
        placeholder="https://xxxxxx.execute-api.eu-central-1.amazonaws.com/prod"
      />
      <LabeledInput
        label="x-api-key (if any)"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="API key or leave empty if none"
      />
    </div>
    <Status
      kind="info"
      text="Client-side keys are visible; make sure Usage Plan/Throttling and CORS are configured in API Gateway. For production, consider server-side signing."
    />
  </Card>
);
