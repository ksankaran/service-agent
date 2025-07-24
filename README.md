# Service Agent: Secure AI Agents with Google ADK

A demonstration project showing how to build secure AI agents that handle sensitive data using encryption strategies and Google's Agent Development Kit (ADK) lifecycle callbacks.

## 🔒 Security-First Approach

This project demonstrates a practical implementation of data protection in AI agents by:

- **Encrypting sensitive data at session creation** to minimize exposure
- **Using ADK lifecycle callbacks** to decrypt data only when tools need raw access
- **Re-encrypting data immediately** after processing to maintain security
- **Isolating LLMs from sensitive information** while preserving functionality

The key insight: LLMs work with encrypted identifiers while tools handle decryption/encryption through strategic callback placement.

## 🏗️ Architecture

```
Session Creation → Encrypt user identifiers
       ↓
Agent Context → LLM processes encrypted data  
       ↓
Tool Execution → before_tool_callback decrypts arguments
       ↓
Data Processing → Tools work with raw data
       ↓  
Response → after_tool_callback re-encrypts sensitive fields
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ksankaran/service-agent.git
   cd service-agent
   ```

2. **Create virtual environment**
   ```bash
   uv venv
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up encryption key**
   
   Generate a 32-byte encryption key at [https://generate-random.org/encryption-key-generator](https://generate-random.org/encryption-key-generator) and set it as an environment variable:
   
   ```bash
   export ENCRYPTION_KEY="your-32-byte-key-here"
   ```

5. **Run the server**
   ```bash
   uv run server.py
   ```

## 📁 Project Structure

```
service-agent/
├── info-agent/
│   ├── agent.py          # Main agent implementation with callbacks
│   ├── callbacks.py      # Encryption/decryption callback functions
│   └── assets/
│       └── us-500.csv    # Sample user data for testing
├── crypto.py            # Encryption utilities
├── server.py            # Server implementation
└── README.md
```

## 🔧 Key Components

### Agent Implementation

The core agent uses Google ADK with encryption callbacks:

```python
root_agent = Agent(
  name="info_agent",
  model=LiteLlm(model="gpt-4.1-mini"),
  tools=[get_user_info],
  before_tool_callback=decrypt_before_tool_callback,
  after_tool_callback=encrypt_after_tool_callback
)
```

### Lifecycle Callbacks

- **`before_tool_callback`**: Decrypts sensitive arguments before tool execution
- **`after_tool_callback`**: Re-encrypts sensitive data in tool responses

### Data Flow

1. **Session starts** with encrypted user identifiers
2. **LLM receives** encrypted data in context (never sees raw sensitive info)
3. **Tool calls** trigger automatic decryption via callbacks
4. **Tools process** raw data securely
5. **Responses** get encrypted before returning to LLM

## 🛡️ Security Benefits

- **Zero Trust LLM**: Language models never access plaintext sensitive data
- **Minimal Exposure**: Data decrypted only during tool execution
- **Compliance Ready**: Encrypted data at rest and in transit
- **Audit Trail**: All encryption/decryption events can be logged
- **Provider Isolation**: External LLM services only see encrypted tokens

## 🧪 Testing

The project includes sample data (US-500 dataset) for testing the encryption flow. When you run the server:

1. User sessions are created with encrypted email identifiers
2. The agent can retrieve user information using encrypted context
3. Tools decrypt data only when needed for database lookups
4. All sensitive information remains encrypted in logs and LLM interactions

## 📖 Learn More

This project was built to demonstrate the security patterns described in the blog post: "Securing Sensitive Data in AI Agents: Encryption Strategies with Google's Agent ADK"

For detailed implementation insights and security considerations, check out the full blog post and explore the callback implementations in the codebase.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report issues or security concerns
- Suggest improvements to the encryption patterns
- Add support for additional callback types
- Enhance the demo with more realistic scenarios

## 📄 License

This project is open source and available under the MIT License.