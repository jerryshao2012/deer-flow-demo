# 🦌 DeerFlow Hello World Demo

A beginner-friendly introduction to using DeerFlow with local Ollama LLM. This demo shows you how to get started with DeerFlow's super agent capabilities using your local machine.

## 🎯 What You'll Learn

- Setting up DeerFlow with Local Execution mode
- Configuring Ollama as your LLM provider
- Running your first AI agent tasks
- Understanding the basic architecture

## 📋 Prerequisites

### Required Software

1. **Python 3.12+** (already set up in `.venv`)
2. **Ollama** - Install from [ollama.com](https://ollama.com)
3. **Tavily API Key** - Get free key at [tavily.com](https://app.tavily.com)

### Verify Ollama Installation

```bash
ollama --version
ollama list
```

You should see `glm-4.7-flash:latest` in your models list.

## 🚀 Quick Start

### Step 1: Clone DeerFlow Repository

```bash
cd /Users/jerryshao/Documents/projects/IBM/ai/deer-flow-demo
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
```

### Step 2: Install Dependencies

**Option A: Using uv (Recommended)**
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync
```

**Option B: Using pip**
```bash
# Install minimal dependencies for hello_world.py script
pip install -r requirements.txt

# Note: Full DeerFlow dependencies are installed via 'uv sync' in deer-flow directory
```

### Step 3: Configure for Local Execution

Copy the configuration files:

```bash
# Copy this demo's config to deer-flow directory
cp ../config.yaml .
cp ../.env.example .env
```

### Step 4: Set Your Tavily API Key

Edit the `.env` file:

```bash
# Open .env and replace with your actual key
nano .env
# or
vim .env
```

Replace `your-tavily-api-key-here` with your actual Tavily API key.

### Step 5: Start DeerFlow

#### Option A: Development Mode (Recommended for Learning)

```bash
make dev
```

This starts both backend and frontend with hot-reload.

#### Option B: Console UI Only

```bash
uv run main.py
```

### Step 6: Access the Interface

Open your browser and visit: **http://localhost:2026**

## 📖 Configuration Details

### Model Configuration (config.yaml)

```yaml
models:
  - name: ollama-glm4-flash
    display_name: GLM-4-Flash (Ollama Local)
    use: langchain_openai:ChatOpenAI
    model: glm-4.7-flash:latest
    base_url: http://localhost:11434/v1
    api_key: ollama  # Ollama doesn't need a real API key
    max_tokens: 4096
    temperature: 0.7
```

**Key Settings:**
- `base_url`: Points to your local Ollama server (default: http://localhost:11434/v1)
- `model`: Must match your Ollama model name exactly
- `use`: Uses LangChain's OpenAI-compatible interface

### Sandbox Mode: Local Execution

The config uses **Local Execution** mode, which means:
- ✅ Code runs directly on your host machine
- ✅ No Docker container overhead
- ✅ Faster execution for trusted code
- ⚠️ Less isolation than Docker mode

```yaml
sandbox:
  use: deerflow.sandbox.local_sandbox:LocalSandboxProvider
```

## 🎓 Use Case Examples

### 1. Simple Research/Query Task ⭐ (Start Here!)

**What it does:** Researches a topic and provides a comprehensive answer.

**Example Tasks:**
- "Research the latest developments in quantum computing"
- "What are the best practices for API design in 2026?"
- "Compare microservices vs monolithic architecture"

**How to try:**
1. Go to http://localhost:2026
2. Type: `"Research recent advances in renewable energy storage"`
3. Watch as DeerFlow:
   - Plans the research approach
   - Searches the web using Tavily
   - Synthesizes findings
   - Provides a structured report

**Expected Output:**
- Research plan with steps
- Search results summary
- Comprehensive answer with sources
- Follow-up suggestions

---

### 2. Code Generation Task

**What it does:** Generates working code based on your requirements.

**Example Tasks:**
- "Create a Python FastAPI endpoint for user authentication"
- "Write a React component for a todo list with drag-and-drop"
- "Generate a SQL query to analyze sales data by region"

**How to try:**
```
"Create a Python function that validates email addresses using regex. 
Include unit tests."
```

**Expected Output:**
- Working code implementation
- Code explanation
- Usage examples
- Test cases

---

### 3. Document/Report Generation

**What it does:** Creates structured documents, reports, or presentations.

**Example Tasks:**
- "Generate a product requirements document for a fitness tracking app"
- "Create a market analysis report for electric vehicles"
- "Write technical documentation for a REST API"

**How to try:**
```
"Create a comprehensive project proposal for implementing 
a company-wide knowledge base using AI."
```

**Expected Output:**
- Structured document with sections
- Executive summary
- Detailed content
- Recommendations

---

### 4. General Conversational Agent

**What it does:** Acts as an intelligent assistant for various tasks.

**Example Tasks:**
- "Help me plan my learning path for machine learning"
- "What should I consider when choosing a cloud provider?"
- "Explain blockchain technology like I'm 12"

**How to try:**
```
"I'm starting a new job as a software engineer. 
What should I prepare in my first week?"
```

**Expected Output:**
- Personalized advice
- Actionable steps
- Resources and tips
- Follow-up support

---

## 🔧 Troubleshooting

### Ollama Not Responding

**Error:** Connection refused to http://localhost:11434

**Solution:**
```bash
# Start Ollama server
ollama serve

# In another terminal, verify it's running
curl http://localhost:11434/api/tags
```

### Model Not Found

**Error:** Model 'glm-4.7-flash:latest' not found

**Solution:**
```bash
# Pull the model
ollama pull glm-4.7-flash:latest

# Verify installation
ollama list
```

### Tavily API Error

**Error:** Invalid API key or rate limit exceeded

**Solution:**
1. Check your API key in `.env` file
2. Verify at [tavily.com](https://app.tavily.com)
3. Check usage limits on free tier

### Port Already in Use

**Error:** Address already in use for port 2026

**Solution:**
```bash
# Find and kill the process
lsof -i :2026
kill -9 <PID>

# Or use a different port
export DEER_FLOW_PORT=2027
make dev
```

## 📊 Performance Tips

### For Better Results with Local Models

1. **Use Larger Models** if you have RAM:
   ```bash
   ollama pull llama3.2:latest  # 7.8GB, better reasoning
   ```

2. **Adjust Temperature** in config.yaml:
   ```yaml
   temperature: 0.5  # More focused (0.0-1.0)
   ```

3. **Increase Context Window** if needed:
   ```yaml
   max_tokens: 8192  # For longer responses
   ```

### Speed Optimization

- Local Execution is faster than Docker for simple tasks
- Keep Ollama server running in background
- Use smaller models for quick queries

## 🎯 Next Steps

After mastering the basics:

1. **Try Other Models:**
   - Edit `config.yaml` to switch models
   - Example: Change to `qwen3.5:latest` or `llama3.1:latest`

2. **Explore Advanced Features:**
   - MCP Servers integration
   - Sub-agent orchestration
   - Long-term memory

3. **Customize Workflows:**
   - Create custom skills
   - Add new tools
   - Build specialized agents

4. **Production Setup:**
   - Switch to Docker sandbox mode
   - Add authentication
   - Deploy with proper monitoring

## 📚 Resources

- **Official Docs:** [deerflow.tech](https://deerflow.tech/)
- **GitHub Repo:** [github.com/bytedance/deer-flow](https://github.com/bytedance/deer-flow)
- **Ollama Models:** [ollama.com/library](https://ollama.com/library)
- **Tavily API:** [app.tavily.com](https://app.tavily.com)

## 🤝 Community & Support

- **Issues:** Report bugs on GitHub
- **Discussions:** Join community discussions
- **Contributions:** PRs welcome!

## 📄 License

This demo follows DeerFlow's MIT License.

---

**Happy Exploring! 🦌✨**

Start with simple research queries and gradually explore more complex tasks. The local LLM might take a bit longer than cloud APIs, but you get full privacy and control!
