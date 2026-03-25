# 🦌 DeerFlow Hello World Demo - Complete Guide

A comprehensive introduction to using DeerFlow with local Ollama LLM. Learn to build AI agents that can research, code, and assist autonomously using either **Server Mode** (full platform) or **Library Mode** (Python library).

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Choosing Your Path](#choosing-your-path)
3. [Library Mode (DeerFlowClient)](#library-mode-deerflowclient)
4. [Server Mode (Full Platform)](#server-mode-full-platform)
5. [Configuration](#configuration)
6. [Use Cases & Examples](#use-cases--examples)
7. [Architecture Overview](#architecture-overview)
8. [Troubleshooting](#troubleshooting)
9. [Performance Tips](#performance-tips)

---

## 🚀 Quick Start

### ⚡ Fastest Path (Library Mode - Recommended for Beginners)

**No servers required!** Get results in under 5 minutes:

**Option A: Manual setup**
```bash
# 1. Install dependencies
cd deer-flow/backend
uv sync

# 2. Configure environment
cp ../../.env.example .env
# Edit .env and add your TAVILY_API_KEY from https://app.tavily.com

# 3. Test setup (optional)
python ../../hello_world_library.py
```

**→ See [Library Mode Section](#library-mode-deerflowclient) for complete guide**

---

### 🖥️ Full Platform (Server Mode)

Complete experience with Web UI and REST API:

**⚠️ Note:** The `setup.sh` and `start.sh` scripts are **only for Server Mode**. They set up and manage the full server infrastructure (Gateway + LangGraph + Web UI). Do NOT use these scripts for Library Mode.

**Option A: Using the setup script (Recommended for first-time setup)**
```bash
# Run the automated setup (checks deps, clones repo, installs everything)
./setup.sh

# After setup completes, start servers
./start.sh

# Open browser
open http://localhost:2026
```

**Option B: Manual setup (if you already have deer-flow cloned)**
```bash
# 1. Setup
cd deer-flow
uv sync
cp ../config.yaml .
cp ../.env.example .env
# Edit .env with TAVILY_API_KEY

# 2. Start servers
make dev

# 3. Open browser
open http://localhost:2026
```

**→ See [Server Mode Section](#server-mode-full-platform) for complete guide**

---

## 📋 Choosing Your Path

### Library Mode (`DeerFlowClient`)

**Best for:**
- ✅ Python scripts & applications
- ✅ Data analysis pipelines
- ✅ Rapid prototyping
- ✅ Personal projects
- ✅ Batch processing
- ✅ Embedded AI features

**Characteristics:**
- Single Python process
- Direct function calls
- No network overhead
- Standard debugging
- Lightweight (~100MB RAM)

**Example Use Case:**
```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()
response = client.chat("Research quantum computing advances")
print(response)
```

---

### Server Mode (Full Platform)

**Best for:**
- ✅ Interactive Web UI
- ✅ REST API access
- ✅ Multi-user scenarios
- ✅ Team collaboration
- ✅ Production deployments
- ✅ Language-agnostic integration

**Characteristics:**
- Multiple processes (Gateway + LangGraph)
- HTTP API calls
- Web interface included
- Concurrent users supported
- Heavier (~500MB+ RAM)

**Example Access:**
- Browser: http://localhost:2026
- REST API: `POST /api/langgraph/threads/{id}/runs`

---

## 📚 Library Mode (DeerFlowClient)

### Installation

**Using uv (Recommended)**

```bash
# Add the local harness package to your project
uv add ./deer-flow/backend/packages/harness

# (Optional) If you want to sync existing backend dependencies
cd deer-flow/backend && uv sync
```

This installs the `deerflow-harness` package which includes `DeerFlowClient`.

**Alternative: Manual Editable Install**

If you are not using `uv`, ensure you are in the correct Python environment:

```bash
pip install -e ./deer-flow/backend/packages/harness
```

**⚠️ Important:** The package is NOT on PyPI. You cannot use `pip install deerflow-harness`.

### Configuration

1. **Copy environment file:**
   ```bash
   cp ../../.env.example .env
   ```

2. **Add Tavily API key:**
   ```bash
   nano .env  # Replace with your actual key from https://app.tavily.com
   ```

3. **Start Ollama (optional but recommended):**
   ```bash
   ollama serve
   ollama pull glm-4.7-flash:latest
   ```

### Basic Usage

#### Simple Chat (Non-streaming)

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()
response = client.chat("What is quantum computing?")
print(response)
```

#### Running Diagnostics

Test your setup and configuration with the built-in diagnostics:

```bash
# Run diagnostics using uv (recommended)
uv run python hello_world_library.py --test

# Or using your local python environment
python hello_world_library.py --test
```

This will verify:
- Ollama server connection
- Model availability
- Tavily API key configuration
- Dependencies status

#### Streaming Response (Recommended for long outputs)

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()

for event in client.stream("Explain neural networks"):
    if event.type == "messages-tuple" and event.data.get("type") == "ai":
        content = event.data.get("content", "")
        if content:
            print(content, end="", flush=True)
```

#### Multi-turn Conversations

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()
thread_id = "my-conversation-1"

# First message
response1 = client.chat("What is machine learning?", thread_id=thread_id)
print(response1)

# Follow-up (maintains context)
response2 = client.chat("How does it differ from AI?", thread_id=thread_id)
print(response2)
```

### Advanced Features

#### List Available Models

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()
models = client.list_models()

for model in models.get("models", []):
    print(f"{model['name']} - {model.get('display_name', '')}")
```

#### List Enabled Skills

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()
skills = client.list_skills(enabled_only=True)

for skill in skills.get("skills", []):
    print(f"{skill['name']} ({skill['category']})")
    print(f"  └─ {skill['description'][:60]}...")
```

#### File Uploads

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()
thread_id = "analysis-1"

result = client.upload_files(
    thread_id=thread_id,
    files=["document.pdf", "data.xlsx"]
)
print(result)
```

#### Memory Management

```python
from deerflow.client import DeerFlowClient

client = DeerFlowClient()

# Get memory status
status = client.get_memory_status()
print(status)

# Reload memory from disk
memory = client.reload_memory()
```

### Integration Examples

#### Data Analysis Pipeline

```python
from deerflow.client import DeerFlowClient

def analyze_data(data):
    client = DeerFlowClient()
    return client.chat(f"Analyze this data: {data}")

results = [analyze_data(d) for d in dataset]
```

#### Customer Support Bot

```python
class SupportBot:
    def __init__(self):
        self.client = DeerFlowClient()
    
    def respond(self, query):
        return self.client.chat(query, thread_id="support-1")

bot = SupportBot()
response = bot.respond("How do I reset my password?")
```

#### Content Generation

```python
def generate_article(topic):
    client = DeerFlowClient()
    outline = client.chat(f"Create outline for {topic}")
    content = client.chat(f"Write article based on: {outline}")
    return content

article = generate_article("renewable energy trends")
```

---

## 🖥️ Server Mode (Full Platform)

### Installation

```bash
# Navigate to deer-flow directory
cd deer-flow

# Install dependencies
uv sync

# Copy configuration files
cp ../config.yaml .
cp ../.env.example .env

# Edit .env with your Tavily API key
nano .env
```

### Starting the Servers

```bash
# Development mode (hot-reload enabled)
make dev

# Wait ~30 seconds for startup
# Then open: http://localhost:2026
```

### Using the Web UI

1. **Open browser:** http://localhost:2026
2. **Type your query:** e.g., "Research latest AI developments"
3. **Watch agent work:** Plans, searches, synthesizes, responds
4. **Multi-turn chat:** Conversation history maintained

### REST API Usage

#### Create Thread

```python
import requests

response = requests.post(
    "http://localhost:2026/api/langgraph/threads",
    json={}
)
thread_id = response.json()["thread_id"]
```

#### Send Message

```python
response = requests.post(
    f"http://localhost:2026/api/langgraph/threads/{thread_id}/runs",
    json={
        "assistant_id": "lead_agent",
        "input": {
            "messages": [
                {"role": "user", "content": "Research quantum computing"}
            ]
        }
    }
)
result = response.json()
```

#### Stream Response

```python
import requests
import json

response = requests.post(
    f"http://localhost:2026/api/langgraph/threads/{thread_id}/runs/stream",
    json={
        "assistant_id": "lead_agent",
        "input": {"messages": [{"role": "user", "content": "Hello!"}]}
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        event = json.loads(line)
        print(event)
```

---

## ⚙️ Configuration

### Model Configuration (config.yaml)

```yaml
models:
  - name: ollama-glm4-flash
    display_name: GLM-4-Flash (Ollama Local)
    use: langchain_openai:ChatOpenAI
    model: glm-4.7-flash:latest
    base_url: http://localhost:11434/v1
    api_key: ollama
    max_tokens: 4096
    temperature: 0.7
```

**Key Settings:**
- `base_url`: Ollama server URL (default: http://localhost:11434/v1)
- `model`: Must match Ollama model name exactly
- `use`: LangChain's OpenAI-compatible interface
- `temperature`: 0.0 (focused) to 1.0 (creative)
- `max_tokens`: Context window size

### Sandbox Settings

```yaml
sandbox:
  use: deerflow.sandbox.local_sandbox:LocalSandboxProvider
```

**Local Execution Mode:**
- ✅ Code runs on host machine
- ✅ No Docker overhead
- ✅ Faster execution
- ⚠️ Less isolation than Docker

### Environment Variables (.env)

```env
TAVILY_API_KEY=your-actual-api-key-here
# Get free key at: https://app.tavily.com
```

---

## 🎯 Use Cases & Examples

### 1. Research Task ⭐ (Start Here!)

**Goal:** Get comprehensive answers with web search

**Example Query:**
```
"Research recent advances in quantum computing and their practical applications."
```

**What Agent Does:**
1. Creates research plan
2. Searches web using Tavily
3. Synthesizes findings
4. Provides structured report with sources

**Expected Output:**
- Research approach outline
- Search results summary
- Comprehensive answer
- Citations and references

---

### 2. Code Generation

**Goal:** Generate working code with explanations

**Example Query:**
```
"Create a Python FastAPI endpoint for user authentication with JWT tokens. Include error handling and unit tests."
```

**What Agent Does:**
1. Analyzes requirements
2. Writes complete implementation
3. Adds explanations
4. Includes test cases

**Expected Output:**
- Working code
- Usage examples
- Test suite
- Documentation

---

### 3. Document Generation

**Goal:** Create structured documents and reports

**Example Query:**
```
"Generate a product requirements document for a fitness tracking mobile app with AI coaching features."
```

**What Agent Does:**
1. Structures document
2. Generates executive summary
3. Fills detailed sections
4. Adds recommendations

**Expected Output:**
- PRD structure
- Executive summary
- Feature specifications
- Technical requirements

---

### 4. Conversational Assistant

**Goal:** Interactive Q&A and guidance

**Example Query:**
```
"I'm starting a data science role next month. What should I prepare in my first week?"
```

**What Agent Does:**
1. Understands context
2. Provides personalized advice
3. Suggests actionable steps
4. Offers follow-up support

**Expected Output:**
- Tailored recommendations
- Priority checklist
- Resource suggestions
- Next steps

---

## 🏗️ Architecture Overview

### Library Mode Flow

```
Your Python Script
    ↓
DeerFlowClient (imported)
    ↓
Agent Creation (lazy init)
    ├─ Load config.yaml
    ├─ Load extensions_config.json
    └─ Initialize tools
    ↓
Agent Execution
    ├─ Process message
    ├─ Plan approach
    ├─ Call tools (Tavily, code, etc.)
    └─ Generate response
    ↓
External Services
    ├─ Ollama (LLM)
    ├─ Tavily API (search)
    └─ Local filesystem
    ↓
Return Response
```

### Server Mode Flow

```
Browser / HTTP Client
    ↓ (HTTP)
Gateway API (port 2026)
    ↓ (HTTP)
LangGraph Server
    ↓
Agent Execution
    ↓
External Services
    ├─ Ollama (LLM)
    ├─ Tavily API (search)
    └─ Local filesystem
```

### Key Components

**DeerFlowClient:**
- Configuration loader
- Agent lifecycle manager
- Message serializer
- Event streamer
- File manager

**Tools Available:**
- Search: `tavily_search`, `tavily_answer`, `duckduckgo_search`
- Code: `python_repl`, `sandbox_execution`
- Analysis: `data_analysis`, `chart_visualization`
- Documents: `file_upload`, `artifact_generation`
- Skills: Custom extensions (skill-creator, frontend-design, etc.)
- MCP: Optional server integrations

---

## 🔧 Troubleshooting

### Library Mode Issues

**Problem: Cannot import `DeerFlowClient`**

```bash
# Solution: Reinstall dependencies
cd deer-flow/backend
uv sync
```

**Problem: Tavily API error**

```bash
# Check .env file
cat .env | grep TAVILY

# Should show real key, not placeholder
```

**Problem: Ollama connection failed**

```bash
# Start Ollama in another terminal
ollama serve

# Verify running
curl http://localhost:11434/api/tags
```

**Problem: Model not found**

```bash
# Pull required model
ollama pull glm-4.7-flash:latest

# Or update config.yaml to use different model
```

---

### Server Mode Issues

**Problem: Server won't start**

```bash
# Check logs
cat deer-flow/logs/deerflow.log

# Look for errors
```

**Problem: Web UI not loading**

- Wait 30 seconds for startup
- Refresh browser
- Check console for errors

**Problem: API returns 500**

- Verify all services running
- Check Gateway logs
- Ensure Ollama accessible

---

### Common Issues (Both Modes)

**Port Already in Use**

```bash
# Find process using port 2026
lsof -i :2026

# Kill it
kill -9 <PID>

# Or use different port
export DEER_FLOW_PORT=2027
make dev
```

**Out of Memory**

- Close other applications
- Use smaller model: `ollama pull qwen3.5:latest` (6.6GB)
- Add swap space (Linux/Mac)

**Slow Performance**

- Local LLM is slower than cloud APIs (30-90s vs 2-5s)
- This is normal for privacy-focused local execution
- Consider using larger models if you have RAM

---

## ⚡ Performance Tips

### For Better Results

1. **Use Larger Models** (if you have RAM):
   ```bash
   ollama pull deepseek-v3:latest  # Powerful reasoning and coding capabilities
   ```

2. **Adjust Temperature** in config.yaml:
   ```yaml
   temperature: 0.5  # More focused (0.0-1.0)
   ```

3. **Increase Context Window**:
   ```yaml
   max_tokens: 8192  # For longer responses
   ```

### Speed Optimization

- Keep Ollama server running in background
- Use smaller models for quick queries
- Enable thinking mode for complex tasks
- Reuse client instances in Library Mode

### Expected Response Times

| Task Type | Time | Notes |
|-----------|------|-------|
| Simple Q&A | 10-30s | Query length dependent |
| Research | 30-90s | Includes web search |
| Code Gen | 20-60s | Complexity dependent |
| Documents | 60-120s | Long-form content |

**Note:** Local LLM provides privacy but is slower than cloud APIs.

---

## 📊 Comparison Summary

| Feature | Library Mode | Server Mode |
|---------|-------------|-------------|
| **Setup Time** | 5 minutes | 15 minutes |
| **Processes** | 1 (your script) | 3+ servers |
| **Web UI** | ❌ No | ✅ Yes |
| **REST API** | ❌ No | ✅ Yes |
| **Python Integration** | ✅ Direct import | ❌ HTTP calls |
| **Performance** | ⚡ Fastest | 🐢 Network latency |
| **Resource Usage** | 💚 Light (~100MB) | 🔴 Heavy (~500MB+) |
| **Debugging** | 🔍 Easy | 🔍 Harder |
| **Multi-user** | ❌ Single | ✅ Multiple |
| **Best For** | Scripts & Apps | Platforms & Teams |

---

## 🎓 Learning Path

### Day 1: Library Mode Basics (30 min)

1. Run `hello_world_library.py` ✅
2. Try simple chat examples
3. Read this README

### Day 2: Advanced Library Mode (1 hour)

1. Experiment with streaming
2. Test multi-turn conversations
3. Try file uploads
4. Explore skills

### Day 3: Server Mode (1 hour)

1. Set up full system
2. Try Web UI
3. Explore REST API
4. Test multi-user features

### Day 4+: Build Something! (2+ hours)

1. Create custom script using DeerFlowClient
2. Integrate into existing project
3. Share with team!

---

## 📚 Resources

### Official Documentation

- **DeerFlow Docs:** https://deerflow.tech/
- **GitHub Repo:** https://github.com/bytedance/deer-flow
- **Ollama Models:** https://ollama.com/library
- **Tavily API:** https://app.tavily.com

### Community

- **Issues:** Report bugs on GitHub
- **Discussions:** Join community discussions
- **Contributions:** PRs welcome!

### Troubleshooting Installation Issues

If you encounter import errors or dependency issues:

```bash
# Navigate to backend directory
cd deer-flow/backend

# Reinstall dependencies
uv sync

# Then try starting again
cd .. && ./start.sh
```

---

## 🎉 Next Steps

### After Mastering Basics

1. **Explore Advanced Features:**
   - MCP Servers integration
   - Sub-agent orchestration
   - Long-term memory

2. **Customize Workflows:**
   - Create custom skills
   - Add new tools
   - Build specialized agents

3. **Production Setup:**
   - Switch to Docker sandbox mode
   - Add authentication
   - Deploy with monitoring

---

**Happy Exploring! 🦌✨**

Start with Library Mode for quick wins, then explore Server Mode when you need the full platform. Both modes give you powerful AI agent capabilities running locally on your machine!

---

## 🛠️ Setup Scripts Reference (Server Mode Only)

**⚠️ Important:** The following scripts (`setup.sh` and `start.sh`) are **only for Server Mode** (full platform with Web UI and REST API). They set up and manage multiple server processes.

**For Library Mode:** Do NOT use these scripts. Instead, follow the manual setup steps in the [Library Mode section](#library-mode-deerflowclient).

### When to Use These Scripts

✅ **Use `setup.sh` and `start.sh` if you want:**
- Web UI interface at http://localhost:2026
- REST API access for multi-user applications
- Full platform experience with Gateway + LangGraph servers
- Team collaboration features

❌ **Do NOT use these scripts if you want:**
- Simple Python library integration (use Library Mode instead)
- Single-script applications
- Lightweight setup without server overhead

### `setup.sh` - Automated Initial Setup (Server Mode)
**Use this for first-time setup** - Automatically:
- ✅ Checks Ollama and Nginx installation
- ✅ Validates required Python/Node.js versions  
- ✅ Clones the DeerFlow repository
- ✅ Installs all dependencies (uv, pnpm/npm)
- ✅ Copies configuration files
- ✅ Configures Tavily API key interactively
- ✅ Starts Ollama server

```bash
./setup.sh
```

**Time**: ~5-10 minutes (includes downloading models)

---

### `start.sh` - Quick Start Script
**Use this to restart after initial setup** - Validates prerequisites and starts servers:
- ✅ Checks if Ollama is running (starts it if not)
- ✅ Validates GLM-4-Flash model is available
- ✅ Verifies configuration files exist
- ✅ Runs `make dev` to start all services

```bash
./start.sh
```

**Time**: ~30 seconds (if already set up)

---

### Troubleshooting Installation Issues

If you encounter import errors or dependency issues:

```bash
# Navigate to backend directory
cd deer-flow/backend

# Reinstall dependencies
uv sync

# Then try starting again
cd .. && ./start.sh
```
