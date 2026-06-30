# run_webhook.py
import uvicorn
from sync.webhook import app

if __name__ == "__main__":
    uvicorn.run("sync.webhook:app", host="0.0.0.0", port=8002, reload=True)