# ✅ DeerFlow Hello World Setup Checklist

Use this checklist to ensure everything is properly configured before running the demo.

## Pre-Setup Checklist

### 1. System Requirements
- [ ] macOS/Linux/Windows with WSL
- [ ] Python 3.12+ installed (`python3 --version`)
- [ ] Git installed (`git --version`)
- [ ] At least 25GB free disk space (for model + DeerFlow)
- [ ] 16GB+ RAM recommended (GLM-4-Flash is 19GB)

### 2. Ollama Installation
- [ ] Ollama installed (`ollama --version`)
- [ ] Ollama service can start (`ollama serve`)
- [ ] GLM-4-Flash model downloaded (`ollama pull glm-4.7-flash:latest`)
- [ ] Model verified (`ollama list` shows glm-4.7-flash)

### 3. API Keys
- [ ] Tavily API key obtained from https://app.tavily.com
- [ ] API key saved in `.env` file
- [ ] API key tested (free tier has 100 searches/month)

## Setup Process

### Option A: Automated Setup (Recommended)
```bash
./setup.sh
```

Checklist:
- [ ] Script executed successfully
- [ ] Ollama detected
- [ ] Model downloaded (if needed)
- [ ] DeerFlow cloned
- [ ] Dependencies installed
- [ ] Configuration files copied
- [ ] Tavily API key configured
- [ ] Ollama server started

### Option B: Manual Setup
```bash
# Step-by-step manual setup
cd /Users/jerryshao/Documents/projects/IBM/ai/deer-flow-demo

# 1. Clone repository
[ ] git clone https://github.com/bytedance/deer-flow.git

# 2. Navigate to deer-flow
[ ] cd deer-flow

# 3. Install uv (if not installed)
[ ] curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Sync dependencies
[ ] uv sync

# 5. Copy config files
[ ] cp ../config.yaml .
[ ] cp ../.env.example .env

# 6. Edit .env with Tavily API key
[ ] nano .env  # Replace placeholder with actual key

# 7. Start Ollama (separate terminal)
[ ] ollama serve

# 8. Start DeerFlow
[ ] make dev
```

## Verification Steps

### 1. Check Ollama
```bash
ollama list
```
Expected output includes: `glm-4.7-flash:latest`

### 2. Check Ollama Server
```bash
curl http://localhost:11434/api/tags
```
Expected: JSON response with model list

### 3. Check DeerFlow Server
```bash
curl http://localhost:2024/health
```
Expected: `{"status": "ok"}` or similar

### 4. Check Web UI
Open browser: http://localhost:2026
Expected: DeerFlow web interface loads

### 5. Run Demo Script
```bash
cd ..
python hello_world.py
```
Expected: All prerequisites pass

## First Test Tasks

### Test 1: Simple Query ⭐ START HERE
**Action:** Go to http://localhost:2026 and enter:
```
What is quantum computing? Explain in simple terms.
```

**Expected Result:**
- [ ] Agent responds within 30-60 seconds
- [ ] Answer is coherent and relevant
- [ ] No errors in console

### Test 2: Research Task
**Action:** Enter:
```
Research recent developments in renewable energy storage.
```

**Expected Result:**
- [ ] Agent creates research plan
- [ ] Performs web search (uses Tavily API)
- [ ] Provides structured answer with sources
- [ ] Search count visible in logs

### Test 3: Code Generation
**Action:** Enter:
```
Write a Python function to calculate fibonacci numbers. Include examples.
```

**Expected Result:**
- [ ] Working Python code generated
- [ ] Code explanation provided
- [ ] Example usage shown

## Common Issues & Solutions

### Issue: Model Not Found
```bash
# Solution:
ollama pull glm-4.7-flash:latest
```

### Issue: Connection Refused to Ollama
```bash
# Solution:
ollama serve
# Keep this running in background
```

### Issue: Tavily API Error
- [ ] Check API key in `.env` file
- [ ] Verify at https://app.tavily.com
- [ ] Check usage limits (free tier: 100/month)

### Issue: Port Already in Use
```bash
# Find process using port 2026
lsof -i :2026
# Kill it
kill -9 <PID>
```

### Issue: Out of Memory
- [ ] Close other applications
- [ ] Consider using smaller model (qwen3.5:latest = 6.6GB)
- [ ] Add swap space (Linux/Mac)

## Success Criteria

You've successfully set up DeerFlow Hello World when:

- [x] Ollama running with GLM-4-Flash model
- [x] DeerFlow server accessible at http://localhost:2026
- [x] Can perform simple Q&A tasks
- [x] Can perform research tasks (with Tavily)
- [x] Can generate code
- [x] No critical errors in logs

## Performance Benchmarks

### Expected Response Times (Local LLM)

| Task Type | Expected Time | Notes |
|-----------|--------------|-------|
| Simple Q&A | 10-30 seconds | Depends on query length |
| Research Task | 30-90 seconds | Includes web search time |
| Code Generation | 20-60 seconds | Depends on complexity |
| Document Creation | 60-120 seconds | Long-form content |

**Note:** Local LLM is slower than cloud APIs but provides privacy and no usage limits!

## Next Steps After Setup

Once everything is working:

1. [ ] Read full README.md documentation
2. [ ] Try all 4 use case examples
3. [ ] Experiment with different queries
4. [ ] Customize config.yaml settings
5. [ ] Explore advanced features
6. [ ] Share feedback/issues on GitHub

## Files Created

Reference guide for what each file does:

| File | Purpose | Edit? |
|------|---------|-------|
| `README.md` | Main documentation | Read only |
| `config.yaml` | DeerFlow configuration | ✅ Customize |
| `.env.example` | Environment template | Read only |
| `.env` | Actual environment (created from example) | ✅ Add API keys |
| `hello_world.py` | Demo script | Optional |
| `setup.sh` | Automated setup | Optional |
| `QUICK_REFERENCE.md` | Quick command reference | Read only |
| `.gitignore` | Git ignore rules | Optional |

## Tips for Best Results

### DO ✅
- Keep Ollama server running in background
- Start with simple queries to test
- Monitor logs for debugging
- Use Tavily for up-to-date information
- Be patient with local LLM (slower than cloud)

### DON'T ❌
- Don't skip the Tavily API key setup
- Don't expect GPT-4 speed from local model
- Don't run multiple heavy models simultaneously
- Don't ignore error messages in logs
- Don't forget to save your API keys securely

## Getting Help

If you're stuck:

1. Check `README.md` troubleshooting section
2. Review `QUICK_REFERENCE.md` for common commands
3. Check logs: `deer-flow/logs/deerflow.log`
4. Visit official docs: https://deerflow.tech/
5. Join GitHub discussions: https://github.com/bytedance/deer-flow/discussions

---

## Completion Certificate

When all boxes are checked, you've successfully completed the DeerFlow Hello World setup! 🎉

**Date Completed:** _______________

**Notes:**
_________________________________
_________________________________
_________________________________

**Next Goal:** Try your first research task!

---

**Congratulations! You're ready to explore DeerFlow with local Ollama LLM! 🦌✨**
