import os
from cryptography.fernet import Fernet

encryption_key = os.getenv("ENCRYPTION_KEY")

def decrypt_data(encrypted_data: str) -> str:
  """
  Decrypts the given encrypted data using a symmetric key.
  
  Args:
      encrypted_data (str): The encrypted data to decrypt.
      
  Returns:
      str: The decrypted data.
  """
  # Replace 'your_symmetric_key' with your actual symmetric key
  if not encryption_key:
    raise ValueError("Encryption key is not set in the environment variables.")
  
  fernet = Fernet(encryption_key)
  decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
  return decrypted_data

def encrypt_data(data: str) -> str:
  """
  Encrypts the given data using a symmetric key.
  
  Args:
      data (str): The data to encrypt.
      
  Returns:
      str: The encrypted data.
  """
  if not encryption_key:
    raise ValueError("Encryption key is not set in the environment variables.")
  
  fernet = Fernet(encryption_key)
  encrypted_data = fernet.encrypt(data.encode()).decode()
  return encrypted_data
