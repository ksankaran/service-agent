from typing import Any, Dict, Optional
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from crypto import decrypt_data, encrypt_data
import re

def decrypt_before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict[str, Any]]:
  """
  Callback to decrypt sensitive data before tool execution.
  
  Args:
    tool (BaseTool): The tool being executed.
    args (Dict[str, Any]): Arguments passed to the tool.
    context (ToolContext): Context of the tool execution.
      
  Returns:
    Optional[Dict[str, Any]]: Decrypted arguments or None if no decryption is needed.
  """
  agent_name = tool_context.agent_name
  tool_name = tool.name
  print(f"Decrypting data for agent: {agent_name}, tool: {tool_name}")
  print(f"Arguments before decryption: {args}")

  if args.get('email'):
    print(f"Decrypting email: {args['email']}")
    args['email'] = decrypt_data(args['email'])
  return None

def encrypt_after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict[str, Any]]:
  """
  Callback to encrypt sensitive data after tool execution.
  
  Args:
    tool (BaseTool): The tool being executed.
    args (Dict[str, Any]): Arguments passed to the tool.
    context (ToolContext): Context of the tool execution.
      
  Returns:
    Optional[Dict[str, Any]]: Encrypted arguments or None if no encryption is needed.
  """
  agent_name = tool_context.agent_name
  tool_name = tool.name
  print(f"Encrypting data for agent: {agent_name}, tool: {tool_name}")
  print(f"Arguments before encryption: {args}")

  # check if email is in unencrypted format as well
  # check for email regex and use re library to validate
  if args.get('email') and re.match(r"[^@]+@[^@]+\.[^@]+", args['email']):
    print(f"Encrypting email: {args['email']}")
    args['email'] = encrypt_data(args['email'])
  return None