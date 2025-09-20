# Customer IDs Backend (AWS Lambda + API Gateway + DynamoDB)

Serverless backend providing a secure **REST API** to manage customer IDs, plus an **event‑driven workflow** with **Step Functions + EventBridge**, monitored by **CloudWatch**.

---

## Tech Stack

- **Python 3.11** (AWS Lambda)
- **API Gateway** (REST, API Key)
- **DynamoDB** (`customer_ids`, PK: `id`)
- **Step Functions + EventBridge** (orchestration & triggers)
- **CloudWatch** (logs, metrics, alarms)
- **pytest** (unit tests)

---

## Project Structure

```
backend/
  app/
    config.py        # settings & env
    logging.py       # structured logging
    errors.py        # domain exceptions
    http.py          # response helpers (CORS included)
    dynamodb_repo.py # DynamoDB repository
    validation.py    # input validation
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
    screenshots/   # CloudWatch, SFN, EventBridge, alarms
    diagrams/      # architecture
```

---

## DynamoDB

Create the table:

```bash
aws dynamodb create-table   --table-name customer_ids   --attribute-definitions AttributeName=id,AttributeType=S   --key-schema AttributeName=id,KeyType=HASH   --billing-mode PAY_PER_REQUEST   --region eu-central-1
```

Check status:

```bash
aws dynamodb describe-table   --table-name customer_ids   --region eu-central-1   --query "Table.TableStatus"
```

Sample ops:

```bash
aws dynamodb put-item    --table-name customer_ids --item file://item.json --region eu-central-1
aws dynamodb get-item    --table-name customer_ids --key '{"id":{"S":"user_123"}}' --region eu-central-1
aws dynamodb delete-item --table-name customer_ids --key '{"id":{"S":"user_123"}}' --region eu-central-1
```

--

**Table Name:** `customer_ids`  
**Partition Key:** `id (String)`

### CLI Commands

- Create table: [Paste command + output]
- Describe table: [Paste output]
- Example put/get/delete: [Paste outputs]

---

## Lambda Functions

List of functions:

- `put_customer_id` – insert ID
- `get_customer_id` – check ID
- `delete_customer_id` – delete ID
- `validate_exists` – helper for workflow
- `log_event` – log branch
- `insert_id` – insert branch

### Deployment

- Packaging: [Paste command/output]
- Update function code: [Paste command/output]

---

---

## API Contract

**Endpoints**

- `PUT    /customers/{id}` – insert new ID
- `GET    /customers/{id}` – check existence
- `DELETE /customers/{id}` – delete ID

**Headers**

- `x-api-key` (required)
- `Content-Type: application/json` (for PUT with body)

**Examples**

```bash
# PUT create
curl -X PUT "https://<api-id>.execute-api.eu-central-1.amazonaws.com/prod/customers/user_test"   -H "x-api-key: <API_KEY>"

# GET exists
curl -X GET "https://<api-id>.execute-api.eu-central-1.amazonaws.com/prod/customers/user_test"   -H "x-api-key: <API_KEY>"

# DELETE
curl -X DELETE "https://<api-id>.execute-api.eu-central-1.amazonaws.com/prod/customers/user_test"   -H "x-api-key: <API_KEY>"
```

---

## Lambda Deployment

Package:

```bash
zip -r backend/dist/backend_bundle.zip backend/app backend/lambdas
```

Update functions:

```bash
REGION=eu-central-1
ZIP=backend/dist/backend_bundle.zip
for f in put_customer_id get_customer_id delete_customer_id validate_exists log_event insert_id; do
  aws lambda update-function-code --function-name "$f" --zip-file "fileb://$ZIP" --region "$REGION"
done
```

---

## Mission 3 – Event‑Driven Workflow

### Architecture

📸 See `docs/diagrams/mission3-architecture.png` (./docs/mission3-architecture.png)
Flow: **API Gateway → EventBridge → Step Functions → (ValidateExists → Choice → [LogEvent | InsertId]) → DynamoDB → CloudWatch → SNS**

### State Machine (ASL)

File: `backend/stepfunctions/customers-workflow.asl.json` (example):

### Flow

`ValidateExists → Choice → [LogEvent | InsertId]`

### Executions

- Example input (new ID) → Insert path.
- Example input (existing ID) → LogEvent path.
- Example invalid input → Failure.

📸 See `docs/diagrams/WORKFLOW INSERT ID.png` (./docs/WORKFLOW INSERT ID.png)
📸 See `docs/diagrams/WORKFLOW EDITOR.png` (./docs/WORKFLOW EDITOR.png)
📸 See `docs/diagrams/WORKFLOW FAILED.png` (./docs/WORKFLOW FAILED.png)

### EventBridge Triggers

**Option A – Schedule**

```bash
aws events put-rule   --name customer-scan-schedule   --schedule-expression "rate(5 minutes)"

aws events put-targets   --rule customer-scan-schedule   --targets "Id"="sfn1","Arn"="<STATE_MACHINE_ARN>","RoleArn"="<EVENTBRIDGE_TO_SFN_ROLE_ARN>","Input"='{"id":"scheduled-check"}'
```

**Option B – API‑Driven (preferred)**
Lambda (`put_customer_id`) publishes an event:

```python
import boto3, json
events = boto3.client("events")
events.put_events(Entries=[{
  "Source": "customer.api",
  "DetailType": "CustomerCreated",
  "Detail": json.dumps({"id": id_value})
}])
```

Rule pattern:

```json
{ "source": ["customer.api"], "detail-type": ["CustomerCreated"] }
```

Target: Step Functions (StartExecution).

### IAM (Minimal Snippets)

**SFN execution role → invoke Lambdas**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": [
        "arn:aws:lambda:eu-central-1:<ACCOUNT_ID>:function:validate_exists",
        "arn:aws:lambda:eu-central-1:<ACCOUNT_ID>:function:log_event",
        "arn:aws:lambda:eu-central-1:<ACCOUNT_ID>:function:insert_id"
      ]
    }
  ]
}
```

**EventBridge role → start SFN**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "states:StartExecution",
      "Resource": "arn:aws:states:eu-central-1:<ACCOUNT_ID>:stateMachine:customers-workflow"
    }
  ]
}
```

---

## Monitoring & Alarms

**Metrics**

- Step Functions: `ExecutionsFailed`, `ExecutionsTimedOut`, `ExecutionsThrottled`
- Lambda: `Errors`, `Throttles`

**Alarm (example)**

```bash
aws cloudwatch put-metric-alarm   --alarm-name StepFunctionExecutionFailures   --metric-name ExecutionsFailed   --namespace AWS/States   --dimensions Name=StateMachineArn,Value=<STATE_MACHINE_ARN>   --statistic Sum --period 60 --evaluation-periods 1 --threshold 1   --comparison-operator GreaterThanOrEqualToThreshold   --alarm-actions <SNS_TOPIC_ARN>
```

**EMAIL**

- Topic: `arn:aws:sns:eu-central-1:<ACCOUNT_ID>:alerts` (confirm email subscription)
  📸 See `docs/diagrams/EMAIL.png` (./docs/EMAIL.png)
  📸 See `docs/diagrams/Alarms.png` (./docs/Alarms.png)

---

## Testing & Validation

**Manual execution**

```bash
aws stepfunctions start-execution   --state-machine-arn "<STATE_MACHINE_ARN>"   --input '{"id":"demo-123"}'
```

Results:

- First run → Insert branch
- Second run (same id) → LogEvent branch
- Invalid input → Failed execution → Alarm → Email

**End‑to‑End via API**

```bash
curl -X PUT "https://<api-id>.execute-api.eu-central-1.amazonaws.com/prod/customers/demo-123"   -H "x-api-key: <API_KEY>"
```

---

## Screenshots (Proof)

Stored in `backend/docs/screenshots/`:

- `workflow-insert.png`, `workflow-exists.png`
- `eventbridge-rule.png`
- `cloudwatch-logs.png`
- `alarm-in-alarm.png`, `alarm-ok.png`
- `sns-email.png`

---

## Outputs

- **State Machine ARN:** `arn:aws:states:eu-central-1:<ACCOUNT_ID>:stateMachine:customers-workflow`
- **EventBridge Rules:** `customer-scan-schedule`, `customer-created-to-sfn`
- **CloudFront URL (frontend):** `https://<cloudfront-domain>`
- **API Gateway (prod):** `https://<api-id>.execute-api.eu-central-1.amazonaws.com/prod`

---

## Troubleshooting (Quick)

- **403** → missing/invalid `x-api-key` or Usage Plan not attached
- **CORS** → ensure OPTIONS + Gateway Responses (4XX/5XX) include CORS headers
- **404** → path mismatch (`/customers/{id}`)
- **Validation** → `id` must be non-empty string

---

## Known Limitations

- API Key auth only (no IAM/OAuth)
- Manual deployment (no CI/CD)
- Simple workflow logic for demo
