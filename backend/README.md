# Customer IDs Backend (AWS Lambda + API Gateway + DynamoDB)

Serverless backend providing a secure **REST API** for managing customer IDs.  
Implemented with **AWS Lambda (Python)**, **API Gateway**, and **DynamoDB**, plus an event-driven workflow using **Step Functions** and **EventBridge**.

---

## Tech Stack

- Python 3.11 (Lambda runtime)
- AWS Lambda (business logic)
- API Gateway (REST endpoints, secured with API Key)
- DynamoDB (NoSQL table, partition key `id`)
- Step Functions + EventBridge (workflow orchestration)
- CloudWatch (logs & metrics, alarms)
- pytest (unit tests)

---

## Project Structure

```
backend/
  app/                # Shared application code
    config.py
    logging.py
    errors.py
    http.py
    dynamodb_repo.py
    validation.py

  lambdas/
    get_customer_id/handler.py
    put_customer_id/handler.py
    delete_customer_id/handler.py
    validate_exists/handler.py
    log_event/handler.py
    insert_id/handler.py

  tests/
    test_get_customer_id.py
    test_put_customer_id.py
    test_delete_customer_id.py
    test_validate_exists.py

  docs/
    screenshots/   # CloudWatch logs, SFN graphs, EventBridge rules, alarms
    diagrams/      # architecture diagrams
```

---

## DynamoDB

### Create Table

```powershell
aws dynamodb create-table `
  --table-name customer_ids `
  --attribute-definitions AttributeName=id,AttributeType=S `
  --key-schema AttributeName=id,KeyType=HASH `
  --billing-mode PAY_PER_REQUEST `
  --region eu-central-1
```

### Check Table Status

```powershell
aws dynamodb describe-table `
  --table-name customer_ids `
  --region eu-central-1 `
  --query "Table.TableStatus"
```

### Sample Operations

```powershell
# Put item
aws dynamodb put-item --table-name customer_ids --item file://item.json --region eu-central-1

# Get item
aws dynamodb get-item --table-name customer_ids --key '{"id":{"S":"user_123"}}' --region eu-central-1

# Delete item
aws dynamodb delete-item --table-name customer_ids --key '{"id":{"S":"user_123"}}' --region eu-central-1
```

---

## Lambda Deployment

### Package into ZIP

```powershell
Compress-Archive -Path backend\app, backend\infrastructure, backend\interfaces -DestinationPath backend\dist\backend_bundle.zip -Force
```

### Update Lambda Functions

```powershell
aws lambda update-function-code --function-name get_customer_id --zip-file fileb://backend/dist/backend_bundle.zip --region eu-central-1
aws lambda update-function-code --function-name put_customer_id --zip-file fileb://backend/dist/backend_bundle.zip --region eu-central-1
aws lambda update-function-code --function-name delete_customer_id --zip-file fileb://backend/dist/backend_bundle.zip --region eu-central-1
```

Or with loop:

```powershell
$zip = "C:\tmp\customer_service.zip"
$region = "eu-central-1"
$funcs = @("put_customer_id","get_customer_id","delete_customer_id","validate_exists")
foreach ($f in $funcs) {
  aws lambda update-function-code --function-name $f --zip-file fileb://$zip --region $region
}
```

---

## API Contract

### Endpoints

- `PUT    /customers/{id}` → insert new ID
- `GET    /customers/{id}` → check if ID exists
- `DELETE /customers/{id}` → delete ID

### Required Headers

- `x-api-key` (mandatory)
- `Content-Type: application/json` (for PUT requests with body)

### Example Requests

```powershell
# PUT create
curl -Method PUT "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/user_test" `
  -Headers @{ "Content-Type"="application/json"; "x-api-key"="<API_KEY>" }

# GET exists
curl -Method GET "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/user_test" `
  -Headers @{ "x-api-key"="<API_KEY>" }

# DELETE
curl -Method DELETE "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/user_test" `
  -Headers @{ "x-api-key"="<API_KEY>" }

# OPTIONS preflight (CORS)
curl.exe -i -X OPTIONS "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/user_abc" `
  -H "Origin: http://localhost:5173" `
  -H "Access-Control-Request-Method: PUT" `
  -H "Access-Control-Request-Headers: content-type,x-api-key"
```

### Example Responses

```json
// GET /customers/user_test (exists)
{
  "id": "user_test",
  "exists": true
}

// GET /customers/unknown (does not exist)
{
  "id": "unknown",
  "exists": false
}
```

---

## Workflow (Step Functions)

Triggered when submitting workflow events.

### Flow

```
ValidateExists → Choice (exists?) → [AlreadyExists | InsertId]
```

- If ID exists → Step Function routes to **log event Lambda**
- If ID does not exist → Step Function routes to **insert Lambda**

### Invoke Workflow

```powershell
$uri     = "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/workflow/submit"
$headers = @{ "x-api-key" = "<API_KEY>" }
$body    = @{ id = "sfn-101" } | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri $uri -Headers $headers -Body $body -ContentType "application/json"
```

### Expected Behavior

- First run with new ID → Inserted.
- Second run with same ID → AlreadyExists branch.

---

## EventBridge Triggers

### Option A — Scheduled Rule

Run workflow every 5 minutes:

```bash
aws events put-rule --name customer-scan-schedule   --schedule-expression "rate(5 minutes)"

aws events put-targets --rule customer-scan-schedule --targets   "Id"="sfn1","Arn"="<STATE_MACHINE_ARN>",   "RoleArn"="<ROLE_WITH_StatesStartExecution>",   "Input"='{"id":"scheduled-check"}'
```

### Option B — API-driven Event

Inside `put_customer_id` Lambda:

```python
import boto3, json

client = boto3.client("events")
client.put_events(Entries=[{
  "Source": "customer.api",
  "DetailType": "CustomerCreated",
  "Detail": json.dumps({"id": id_value})
}])
```

EventBridge rule with pattern:

```json
{ "source": ["customer.api"], "detail-type": ["CustomerCreated"] }
```

Target: Step Functions → StartExecution.

---

## Monitoring & Alarms

### CloudWatch Logs

- Each Lambda: `/aws/lambda/<function>`
- Step Functions: Execution logs + event history

### Alarms

- **Step Functions ExecutionsFailed ≥ 1** → send SNS notification
- **Lambda Errors ≥ 1** → send SNS notification
- **API Gateway 5XXErrors ≥ 1** (optional)

**SNS Topic**: `arn:aws:sns:eu-central-1:...:alerts`

- Subscribed email receives alerts.

---

## CORS

Ensure API Gateway returns CORS headers on both OPTIONS and real responses:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET,PUT,DELETE,OPTIONS
Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token
```

These are centralized via the `resp(...)` helper in backend code.

---

## Local Testing

You can run local unit tests with **pytest**:

```bash
pytest -q --disable-warnings
```

> For API tests, use cURL commands above or Postman.

---

## Troubleshooting

- **403 from API Gateway** → missing/invalid API Key, or stage not attached to Usage Plan.
- **CORS errors** → ensure OPTIONS method exists and Gateway Responses for 4XX/5XX include CORS headers.
- **Resource not found (404)** → check path (`/customers/{id}` vs `/customer`). Ensure frontend matches backend contract.
- **Validation errors** → Lambda validates `id` (must be non-empty string).

---

## Documentation & Screenshots

Additional materials are stored under the `backend/docs/` folder:

- **Architecture diagrams** (e.g. backend data flow, Lambda + DynamoDB + API Gateway)
- **Screenshots** of Step Functions executions
- **CloudWatch logs & metrics** examples
- **EventBridge rules & targets**
- **CloudWatch alarms** (OK state + notifications)
- **API test runs** (Postman / curl)

> These images support the assignment submission and illustrate the system in action.

---

## Known Limitations

- API authentication uses API Key only (no IAM/OAuth).
- Deployment is manual (no CI/CD pipeline yet).
- Workflow logic is basic (validate → log or insert).
- EventBridge Option A (schedule) included for demo; Option B (event-driven) preferred in production.

---

## Output (Submission)

- **State Machine ARN**: `arn:aws:states:eu-central-1:...:stateMachine:customers-workflow`
- **EventBridge Rule(s)**: `customer-scan-schedule` / `customer-created-to-sfn`
- **CloudFront URL (frontend)**: https://d2wjdcjivl50hy.cloudfront.net
- **API Gateway (prod stage)**: https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod
