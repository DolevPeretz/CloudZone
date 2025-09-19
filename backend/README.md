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
- CloudWatch (logs & metrics)
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

  tests/
    test_get_customer_id.py
    test_put_customer_id.py
    test_delete_customer_id.py
    test_validate_exists.py
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

### Invoke Workflow

```powershell
$uri     = "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/workflow/submit"
$headers = @{ "x-api-key" = "<API_KEY>" }
$body    = @{ id = "sfn-101" } | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri $uri -Headers $headers -Body $body -ContentType "application/json"
```

### Expected Behavior

- If ID exists → Step Function routes to **log event Lambda**
- If ID does not exist → Step Function routes to **insert Lambda**

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

## Known Limitations

- API authentication uses API Key only (no IAM/OAuth).
- Deployment is manual (no CI/CD pipeline yet).
- Workflow logic is basic (validate → log or insert).
