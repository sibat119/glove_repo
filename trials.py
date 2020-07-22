import dialogflow_v2 as dialogflow

client = dialogflow.IntentsClient()
parent = client.project_agent_path('[project]')

intent = {
    "display_name": "test",
    "webhook_state": True,
    "training_phrases": [{"parts": [{"text": "school", "entity_type": "@school"}], "type": "EXAMPLE"}],
    "parameters": [{"display_name": "school", "entity_type_display_name": "@school", "value": "$school"}]
}

response = client.create_intent(parent, intent)


'''
curl \
https://api.dialogflow.com/v1/query?v=20150910 \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer YOUR_CLIENT_ACCESS_TOKEN' \
-d '{
  "contexts": [
    "shop"
  ],
  "lang": "en",
  "query": "I need apples",
  "sessionId": "12345",
  "timezone": "America/New_York"
}'


curl \
-H "Authorization: Bearer YOUR_CLIENT_ACCESS_TOKEN" \
"https://api.dialogflow.com/v1/query?v=20150910&contexts=shop&lang=en&query=apple&sessionId=12345&timezone=America/New_York"
   
'''