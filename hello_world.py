#!/usr/bin/env python3
"""
DeerFlow Hello World - Simple Research Task Demo

This script demonstrates how to use DeerFlow with local Ollama LLM
to perform a simple research/query task.

Prerequisites:
1. Ollama running with glm-4.7-flash:latest
2. Tavily API key configured in .env
3. DeerFlow dependencies installed (uv sync)
4. DeerFlow server running (make dev)

Usage:
    python hello_world.py
"""

import os
import sys
import time

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OLLAMA_HOST = "http://localhost:11434"
DEER_FLOW_SERVER = "http://localhost:2026"


# Check prerequisites
def check_prerequisites():
    """Verify all prerequisites are met."""
    global requests
    print("🔍 Checking prerequisites...\n")

    checks_passed = True

    # Check 1: Ollama connection
    print("1. Checking Ollama connection...")
    try:
        import requests
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            print("   ✅ Ollama is running")
        else:
            print("   ❌ Ollama returned unexpected status:", response.status_code)
            checks_passed = False
    except Exception as e:
        print(f"   ❌ Cannot connect to Ollama: {e}")
        print("   💡 Solution: Run 'ollama serve' in another terminal")
        checks_passed = False

    # Check 2: Tavily API key
    print("\n2. Checking Tavily API key...")
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key and tavily_key != "your-tavily-api-key-here":
        print("   ✅ Tavily API key configured")
    else:
        print("   ❌ Tavily API key not set or invalid")
        print("   💡 Solution: Edit .env file and add your Tavily API key")
        checks_passed = False

    # Check 3: DeerFlow server
    print("\n3. Checking DeerFlow server...")
    try:
        response = requests.get(f"{DEER_FLOW_SERVER}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ DeerFlow server is running")
        else:
            print("   ⚠️  DeerFlow server status:", response.status_code)
    except Exception as e:
        print(f"   ⚠️  Cannot reach DeerFlow server: {e}")
        print("   💡 Solution: Run 'make dev' to start the server")
        print("   ℹ️  Continuing anyway (might fail later)...")

    # Check 4: Model availability
    print("\n4. Checking model availability...")
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        models = response.json().get("models", [])
        model_names = [m.get("name", "") for m in models]

        if any("glm-4.7-flash" in name for name in model_names):
            print("   ✅ GLM-4-Flash model found")
        else:
            print("   ⚠️  GLM-4-Flash not found in Ollama")
            print("   Available models:", ", ".join(model_names))
            print("   💡 Solution: Run 'ollama pull glm-4.7-flash:latest'")
    except Exception as e:
        print(f"   ⚠️  Cannot check models: {e}")

    print("\n" + "=" * 60)
    if checks_passed:
        print("✅ All critical prerequisites passed!\n")
        return True
    else:
        print("❌ Some prerequisites failed. Please fix them first.\n")
        return False


def run_simple_research_task():
    """Demonstrate a simple research task using DeerFlow."""

    global requests
    print("\n" + "=" * 60)
    print("🎯 RUNNING SIMPLE RESEARCH TASK")
    print("=" * 60)

    # Define the research query
    query = "What are the latest developments in quantum computing in 2026?"

    print(f"\n📝 Research Query: {query}\n")
    print("⏳ Starting research agent...\n")

    # Method 1: Using the web UI (recommended for beginners)
    print("💡 METHOD 1: Web UI (Interactive)")
    print("-" * 60)
    print(f"1. Open your browser to: {DEER_FLOW_SERVER}")
    print("2. Paste this query into the chat input:")
    print(f'   "{query}"')
    print("3. Watch the agent work!")
    print("\nWhat you'll see:")
    print("  • Agent plans the research approach")
    print("  • Performs web searches using Tavily")
    print("  • Synthesizes information")
    print("  • Provides a comprehensive answer\n")

    # Method 2: Using API directly (for developers)
    print("\n💡 METHOD 2: Direct API Call (Programmatic)")
    print("-" * 60)

    try:
        import requests

        # DeerFlow LangGraph API endpoint
        # First, create a thread
        threads_url = f"{DEER_FLOW_SERVER}/api/langgraph/threads"

        print("Creating thread...")
        response = requests.post(threads_url, json={}, timeout=30)

        if response.status_code != 200:
            print(f"⚠️  Failed to create thread: {response.status_code}")
            print("Response:", response.text)
            print(f"\n💡 Use the Web UI instead: {DEER_FLOW_SERVER}")
            return

        thread_data = response.json()
        thread_id = thread_data.get("thread_id")

        if not thread_id:
            print("⚠️  No thread_id returned")
            print("Response:", thread_data)
            return

        print(f"   Thread created: {thread_id}")

        # Now run the agent with the thread
        runs_url = f"{DEER_FLOW_SERVER}/api/langgraph/threads/{thread_id}/runs"

        payload = {
            "assistant_id": "lead_agent",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            },
            "config": {
                "configurable": {
                    "model_name": "ollama-glm4-flash"
                }
            },
            "stream_mode": ["values"]
        }

        headers = {
            "Content-Type": "application/json"
        }

        print(f"Sending request to DeerFlow API (thread: {thread_id})...")
        start_time = time.time()

        # Note: This might timeout if server isn't running properly
        response = requests.post(runs_url, json=payload, headers=headers, timeout=120)

        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Request completed in {elapsed:.2f} seconds")
            print("\n📊 Response:")
            print("-" * 60)

            # Try to extract and display the answer
            if "output" in result:
                output = result["output"]
                if isinstance(output, dict):
                    for key, value in output.items():
                        print(f"{key}: {value}")
                else:
                    print(output)
            else:
                print("Full response:", result)

        else:
            print(f"⚠️  API returned status {response.status_code}")
            print("Response:", response.text)
            print("\n💡 This is okay! Just use the Web UI instead.")

    except requests.exceptions.ConnectionError:
        print("⚠️  Cannot connect to DeerFlow API")
        print("💡 Make sure the server is running: make dev")
        print(f"ℹ️  You can still use the Web UI at {DEER_FLOW_SERVER}")
    except Exception as e:
        print(f"⚠️  Error: {e}")
        print("💡 This is normal for a first-time setup")
        print("ℹ️  The Web UI is more user-friendly for testing")

    print("\n" + "=" * 60)


def show_next_steps():
    """Display suggested next steps for the user."""

    print("\n🎉 CONGRATULATIONS! You've set up DeerFlow Hello World!")
    print("\n" + "=" * 60)
    print("📚 NEXT STEPS TO EXPLORE")
    print("=" * 60)

    print("\n1. 🌐 Try the Web UI")
    print(f"   → Visit: {DEER_FLOW_SERVER}")
    print("   → Experiment with different queries")

    print("\n2. 📖 Read the Full Documentation")
    print("   → See README.md for all use cases")
    print("   → Learn about advanced features")

    print("\n3. 🔧 Customize Configuration")
    print("   → Edit config.yaml to try different models")
    print("   → Adjust sandbox settings")

    print("\n4. 🚀 Try Other Use Cases")
    print("   → Code generation tasks")
    print("   → Document/report creation")
    print("   → Conversational agent tasks")

    print("\n5. 🐛 Troubleshoot Issues")
    print("   → Check logs in ./logs/deerflow.log")
    print("   → See Troubleshooting section in README")

    print("\n" + "=" * 60)
    print("💬 Example Queries to Try:")
    print("=" * 60)

    queries = [
        "Research recent breakthroughs in fusion energy",
        "Create a Python script to scrape weather data",
        "Write a project proposal for a smart home system",
        "Explain neural networks in simple terms",
        "Compare TypeScript vs Python for backend development"
    ]

    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")

    print("\n" + "=" * 60)


def main():
    """Main entry point."""

    print("\n" + "=" * 60)
    print("🦌 DEERFLOW HELLO WORLD - SIMPLE RESEARCH DEMO")
    print("=" * 60)
    print("\nWelcome to DeerFlow with Local Ollama LLM!")
    print("Model: GLM-4-Flash (19GB)")
    print("Mode: Local Execution")
    print("Search: Tavily API\n")

    # Check prerequisites
    if not check_prerequisites():
        print("\n⚠️  Some checks failed.")
        print("You can continue, but the demo might not work properly.")
        choice = input("\nContinue anyway? (y/n): ").lower().strip()
        if choice != 'y':
            print("\n👋 Exiting. Please fix the issues and try again.")
            sys.exit(0)

    # Run the demo
    run_simple_research_task()

    # Show next steps
    show_next_steps()

    print("\n✨ Happy researching! See you in the next demo! ✨\n")


if __name__ == "__main__":
    main()
