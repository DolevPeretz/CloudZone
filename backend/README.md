### Required Headers

- `x-api-key: NlMe8JE1ro8SBEHpi7okJ2YgnRqazFwx9knOqSlK`

---

### Endpoints

#### 1. PUT /customers/{id}

Insert a new customer ID.

**Request**

```bash
curl -X PUT \
  "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/user_abc" \
  -H "x-api-key: NlMe8JE1ro8SBEHpi7okJ2YgnRqazFwx9knOqSlK"


  curl -X GET \
  "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/user_abc" \
  -H "x-api-key: NlMe8JE1ro8SBEHpi7okJ2YgnRqazFwx9knOqSlK"

curl -X DELETE \
  "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/user_abc" \
  -H "x-api-key: NlMe8JE1ro8SBEHpi7okJ2YgnRqazFwx9knOqSlK"
```

Remove-Item backend\dist\backend_bundle.zip -ErrorAction SilentlyContinue

Compress-Archive -Path backend\app, backend\infrastructure, backend\interfaces -DestinationPath backend\dist\backend_bundle.zip -Force

aws lambda update-function-code --function-name get_customer_id --zip-file fileb://backend/dist/backend_bundle.zip
aws lambda update-function-code --function-name put_customer_id --zip-file fileb://backend/dist/backend_bundle.zip
aws lambda update-function-code --function-name delete_customer_id --zip-file fileb://backend/dist/backend_bundle.zip

curl.exe -i -X PUT "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/AB_123" `  -H "Origin: http://localhost:5173"`
-H "x-api-key: NlMe8JE1ro8SBEHpi7okJ2YgnRqazFwx9knOqSlK"

curl.exe -i -X GET "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/AB_123" `  -H "Origin: http://localhost:5173"`
-H "x-api-key: NlMe8JE1ro8SBEHpi7okJ2YgnRqazFwx9knOqSlK"

curl.exe -i -X DELETE "https://nve5ktqo18.execute-api.eu-central-1.amazonaws.com/prod/customers/AB_123" `  -H "Origin: http://localhost:5173"`
-H "x-api-key: NlMe8JE1ro8SBEHpi7okJ2YgnRqazFwx9knOqSlK"
