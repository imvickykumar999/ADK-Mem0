# `ADK Mem0`

```bash
adk create --type=code app_name --model gemini-2.5-flash --api_key AIza............Your_API_Key
adk web --session_service_uri sqlite:///sessions.db --host 0.0.0.0 --port 8888

ngrok config add-authtoken 2izw.......................Your_API_Key
ngrok http --url=your-sub-domain.ngrok-free.app 8000
```

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/213717ab-87e5-40a6-90f8-938393f5f2a3" />
