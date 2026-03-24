# 🚀 DeerFlow Hello World - Quick Reference

## One-Line Setup Commands

### Complete Automated Setup (Recommended)
```bash
./setup.sh
```

### Manual Setup
```bash
# 1. Clone DeerFlow
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow

# 2. Install dependencies
uv sync

# 3. Copy configs
cp ../config.yaml .
cp ../.env.example .env

# 4. Edit .env with your Tavily API key
nano .env

# 5. Start Ollama (in another terminal)
ollama serve

# 6. Start DeerFlow
make dev

# 7. Open browser
# http://localhost:2026
```

## Configuration Files Created

| File | Purpose |
|------|---------|
| `README.md` | Complete documentation with all use cases |
| `config.yaml` | DeerFlow configuration for Ollama + Local Execution |
| `.env.example` | Environment variables template |
| `hello_world.py` | Interactive demo script |
| `setup.sh` | Automated setup script |
| `.gitignore` | Git ignore rules |

## Quick Commands Reference

### Ollama Commands
```bash
ollama list                    # List installed models
ollama pull glm-4.7-flash      # Download GLM-4-Flash model
ollama serve                   # Start Ollama server
curl http://localhost:11434/api/tags  # Check if running
```

### DeerFlow Commands
```bash
make dev                       # Start development server
make docker-start              # Start with Docker (alternative)
uv run main.py                 # Run console UI only
```

### Testing Commands
```bash
python hello_world.py          # Run the demo script
curl http://localhost:2026/health      # Check server health
curl http://localhost:11434/api/tags   # Check Ollama
```

## Use Case Examples

### 1. Simple Research Task ⭐ START HERE
**Query:**
```
Research the latest developments in quantum computing in 2026.
Focus on practical applications and major breakthroughs.
```

**What to expect:**
- Agent creates research plan
- Searches web using Tavily
- Synthesizes findings
- Provides structured answer with sources

---

### 2. Code Generation Task
**Query:**
```
Create a Python function that validates email addresses using regex.
Include unit tests and example usage.
```

**What to expect:**
- Working Python code
- Explanation of the regex pattern
- Unit test examples
- Usage demonstration

---

### 3. Document/Report Generation
**Query:**
```
Create a comprehensive project proposal for implementing 
a company-wide knowledge base using AI. Include executive summary,
technical requirements, timeline, and budget estimates.
```

**What to expect:**
- Structured document with sections
- Executive summary
- Detailed technical specs
- Timeline and budget breakdown

---

### 4. General Conversational Agent
**Query:**
```
I'm starting a new job as a software engineer. What should I prepare 
in my first week? Give me actionable advice and resources.
```

**What to expect:**
- Personalized advice
- Actionable checklist
- Resource recommendations
- Follow-up suggestions

---

## Troubleshooting Quick Fixes

### Issue: "Connection refused to localhost:11434"
```bash
ollama serve
```

### Issue: "Model not found"
```bash
ollama pull glm-4.7-flash:latest
```

### Issue: "Port 2026 already in use"
```bash
lsof -i :2026
kill -9 <PID>
```

### Issue: "Invalid Tavily API key"
1. Check key at https://app.tavily.com
2. Edit `deer-flow/.env`
3. Restart server: `make dev`

## Performance Tips

### For Better Results
```yaml
# In config.yaml, adjust:
temperature: 0.5    # More focused (0.0-1.0)
max_tokens: 8192    # Longer responses
```

### For Faster Execution
- Keep Ollama server running
- Use smaller models for simple queries
- Local Execution is faster than Docker

### Model Switching
Edit `config.yaml` default_model:
```yaml
default_model: ollama-glm4-flash  # or uncomment other models
```

## Example Queries to Try

Copy and paste these into the Web UI:

1. **Research**: "What are the best practices for microservices architecture in 2026?"
2. **Code**: "Write a FastAPI endpoint that accepts file uploads and saves them to S3"
3. **Document**: "Create a technical specification for a real-time chat application"
4. **Conversational**: "Explain machine learning to a 10-year-old with examples"
5. **Analysis**: "Compare Rust vs Go for backend development. Pros and cons?"

## Architecture Overview

```
User Query
    ↓
DeerFlow Web UI (localhost:2026)
    ↓
LangGraph Server (localhost:2026)
    ↓
Agent Orchestrator
    ├→ Ollama LLM (localhost:11434) - GLM-4-Flash
    ├→ Tavily Search API - Web search
    ├→ Local Sandbox - Code execution
    └→ Memory System - Context tracking
    ↓
Response to User
```

## Next Steps After Hello World

1. ✅ Master simple research queries
2. 🔧 Try code generation tasks
3. 📄 Create full documents/reports
4. 🤖 Experiment with conversational tasks
5. ⚙️ Customize configuration
6. 🚀 Explore advanced features (MCP, sub-agents)

## Resources

- **Official Docs**: https://deerflow.tech/
- **GitHub**: https://github.com/bytedance/deer-flow
- **Ollama Models**: https://ollama.com/library
- **Tavily API**: https://app.tavily.com

## Support

- Check `README.md` for detailed documentation
- Review logs: `deer-flow/logs/deerflow.log`
- Join community discussions on GitHub

---

**Happy Exploring! 🦌✨**
