from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, Any
from .callbacks import decrypt_before_tool_callback, encrypt_after_tool_callback
from crypto import encrypt_data
import csv
import os

user_info = {}
file_path = os.path.join(os.getcwd(), 'info-agent/assets', 'us-500.csv')
with open(file_path, 'r') as file:
  dict_reader = csv.DictReader(file)
  for row in dict_reader:
    email = row.get('email', '').strip().lower()
    if email:
      # store the row data in user_info dictionary with email as key
      user_info[email] = row

def get_user_info(email: str) -> Dict[str, Any]:
  """
  Function to retrieve user information based on the email.
  Args:
    email (str): The email of the user whose information is to be retrieved.

  Returns:
    Dict[str, Any]: A dictionary containing user information such as name, role, and preferences
  """
  # read from us-500.csv file in assets folder and build the user map
  info = user_info.get(email.lower(), {
    "name": "Unknown",
    "role": "Unknown",
    "preferences": "No preferences available"
  })
  # encrypt email in info
  info['email'] = encrypt_data(info['email'])
  return info

root_agent = Agent(
  name="info_agent",
  description="An agent that provides information about the user who is logged in session.",
  model=LiteLlm(
    model="gpt-4.1-mini",
  ),
  instruction="""You are an information agent. Your task is to provide information about the user who is logged in session. 
  The user's email ID who is already logged in given in the below context.
  Use the tool get_user_info to fetch the user information in JSON format.
  Based on the information provided by the tool, return the corresponding value from the JSON object.
  For example, if the user asks for name and the tool returns a JSON object with the user's name, you can return the name directly.
  If the user asks for preferences, you can return the preferences in text.
  If the user asks for something that's not there in the tool response json, return 'Sorry, I don't have that information.'

  Context:
  The user is logged in with the email: {user:email}.
  """,
  tools=[get_user_info],
  before_tool_callback=decrypt_before_tool_callback,
  after_tool_callback=encrypt_after_tool_callback
)