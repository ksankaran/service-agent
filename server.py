import os
import uvicorn
import httpx
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.adk.cli.fast_api import get_fast_api_app
from crypto import encrypt_data

import logging
logging.basicConfig(level=logging.DEBUG)

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_ORIGINS = ["http://localhost:8080", "http://localhost", "*"]
SERVE_WEB_INTERFACE = True

app: FastAPI = get_fast_api_app(
  agents_dir=AGENT_DIR,
  allow_origins=ALLOWED_ORIGINS,
  web=SERVE_WEB_INTERFACE,
)

# uncomment this middleware if you want to enforce token checks
# @app.middleware("http")
# async def check_token_in_header(request, call_next):
#   token = request.headers.get("Authorization")
#   if not token or not token.startswith("Bearer "):
#     return {"error": "Unauthorized access. Please provide a valid token."}
  
#   # Proceed with the request if the token is valid
#   response = await call_next(request)
#   return response

@app.post("/apps/{app_name}/sessions")
async def create_session(app_name: str):
  """
  Endpoint to create a session for the specified app.
  """
  # ideally, this email would come from a secure source or user token
  payload = {
    "user:email": encrypt_data("josephine_darakjy@darakjy.org")
  }
  async with httpx.AsyncClient() as client:
    response = await client.post(
      f"http://localhost:8000/apps/{app_name}/users/velu/sessions/my_test_session",
      json=payload
    )
    response_data = response.json()
    return JSONResponse(content=response_data, status_code=response.status_code)

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8000)
