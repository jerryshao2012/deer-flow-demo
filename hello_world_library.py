#!/usr/bin/env python3
"""
DeerFlow Hello World - Library Mode Demo

This script demonstrates how to use DeerFlowClient as a library
without starting any servers. It runs the agent directly in-process.

Prerequisites:
1. Ollama running with glm-4.7-flash:latest (or other configured model)
2. Tavily API key configured in .env
3. DeerFlow dependencies installed via uv workspace

Installation:
    # Navigate to deer-flow backend directory
    cd deer-flow/backend
    
    # Install all dependencies including deerflow-harness
    uv sync
    
    # This installs the deerflow package with DeerFlowClient
    
Usage:
    # IMPORTANT: Run from the deer-flow/backend directory to ensure correct config path resolution
    cd deer-flow/backend
    
    # Then run the script:
    python ../../hello_world_library.py
    
    # Or using uv:
    uv run python ../../hello_world_library.py
    
Run diagnostics first:
    cd deer-flow/backend
    python ../../hello_world_library.py --test
    # or
    uv run python ../../hello_world_library.py --test
"""

import argparse
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import DeerFlowClient - the embedded client that runs without servers
from deerflow.client import DeerFlowClient


def run_diagnostics():
    """Run diagnostic tests to verify setup is correct."""
    print("=" * 60)
    print("🧪 DEERFLOW CLIENT DIAGNOSTICS")
    print("=" * 60)
    print()

    tests_passed = 0
    tests_total = 0
    client = None

    # Test 1: Import
    tests_total += 1
    print("📦 Testing DeerFlowClient import...")
    try:
        from deerflow.client import DeerFlowClient
        print("   ✅ Import successful!\n")
        tests_passed += 1
    except ImportError as e:
        print(f"   ❌ Import failed: {e}\n")
        print("💡 Solution:")
        print("   1. Add the local harness package:")
        print("      uv add ./deer-flow/backend/packages/harness")
        print("   2. (Optional) Navigate to deer-flow/backend and run: uv sync")
        print("   3. Try running this test again using: uv run python hello_world_library.py --test\n")
        print("📚 Installation command:")
        print("   cd deer-flow/backend && uv sync\n")
        print("⚠️  Important: deerflow-harness is not on PyPI.")
        print("   It must be installed from the local source.\n")
        return False

    # Test 2: Environment variables
    tests_total += 1
    print("🔑 Testing environment variables...")
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key and tavily_key != "your-tavily-api-key-here":
        print(f"   ✅ TAVILY_API_KEY is set (length: {len(tavily_key)})\n")
        tests_passed += 1
    else:
        print("   ❌ TAVILY_API_KEY not set or invalid\n")
        print("💡 Solution:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env and add your Tavily API key")
        print("   3. Get a free key at: https://app.tavily.com\n")

    # Test 3: Initialization
    tests_total += 1
    print("🔧 Testing DeerFlowClient initialization...")
    try:
        from deerflow.client import DeerFlowClient
        client = DeerFlowClient()
        print("   ✅ Client initialized successfully!\n")
        tests_passed += 1
    except Exception as e:
        print("   ❌ Initialization failed: {e}\n")
        print("💡 Possible issues:")
        print("   - Missing config.yaml file")
        print("   - Environment variables not set")
        print("   - Dependencies not installed")
        print("   - Script not run from deer-flow/backend directory\n")
        print("💡 Solution:")
        print("   Make sure you're running the script from the deer-flow/backend directory:")
        print("   cd deer-flow/backend && python ../../hello_world_library.py --test\n")
        return False

    # Test 4: List models
    tests_total += 1
    print("📋 Testing list_models()...")
    try:
        models = client.list_models()
        model_list = models.get("models", [])

        if model_list:
            print(f"   ✅ Found {len(model_list)} model(s):")
            for model in model_list[:3]:
                name = model.get("name", "unknown")
                display = model.get("display_name", "")
                print(f"      • {name} {display}")
            if len(model_list) > 3:
                print(f"      ... and {len(model_list) - 3} more")
            print()
            tests_passed += 1
        else:
            print("   ⚠️  No models configured\n")
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")

    # Test 5: List skills
    tests_total += 1
    print("🛠️  Testing list_skills()...")
    try:
        skills = client.list_skills(enabled_only=True)
        skill_list = skills.get("skills", [])

        if skill_list:
            print(f"   ✅ Found {len(skill_list)} enabled skill(s):")
            for skill in skill_list[:5]:
                name = skill.get("name", "unknown")
                category = skill.get("category", "")
                print(f"      • {name} ({category})")
            if len(skill_list) > 5:
                print(f"      ... and {len(skill_list) - 5} more")
            print()
            tests_passed += 1
        else:
            print("   ℹ️  No skills enabled (this is okay)\n")
            tests_passed += 1
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")

    # Test 6: Simple chat
    tests_total += 1
    print("💬 Testing simple chat (non-streaming)...")
    try:
        response = client.chat("Say 'hello' in one word")

        if response and len(response.strip()) > 0:
            print(f"   ✅ Response received: '{response.strip()}'\n")
            tests_passed += 1
        else:
            print("   ⚠️  Empty response received\n")
    except Exception as e:
        print(f"   ❌ Chat failed: {e}\n")
        print("💡 This might be due to:")
        print("   - Ollama not running")
        print("   - Model not available")
        print("   - API configuration issues\n")

    # Summary
    print("=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{tests_total}\n")

    if tests_passed == tests_total:
        print("✅ ALL TESTS PASSED!\n")
        print("🎉 Your setup is working correctly!")
        print("   You can now run: python hello_world_library.py\n")
        return True
    else:
        print("⚠️  Some tests failed.\n")
        print("   Please review the errors above and fix them.")
        print("   Critical tests: import, initialization, environment\n")
        return False


def check_prerequisites():
    """Verify prerequisites are met."""
    print("🔍 Checking prerequisites...\n")

    checks_passed = True

    # Check 1: Tavily API key
    print("1. Checking Tavily API key...")
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key and tavily_key != "your-tavily-api-key-here":
        print("   ✅ Tavily API key configured")
    else:
        print("   ❌ Tavily API key not set or invalid")
        print("   💡 Solution: Edit .env file and add your Tavily API key")
        checks_passed = False

    # Check 2: Try importing deerflow
    print("\n2. Checking DeerFlow library...")
    try:
        from deerflow.client import DeerFlowClient
        print("   ✅ DeerFlow library available")
    except ImportError as e:
        print("   ❌ Cannot import DeerFlow: {e}")
        print("   💡 Solution: Add the local harness package:")
        print("      uv add ./deer-flow/backend/packages/harness")
        print("   📚 Installation steps:")
        print("      1. uv add ./deer-flow/backend/packages/harness")
        print("      2. (Optional) cd deer-flow/backend && uv sync")
        print("      3. This installs deerflow-harness package")
        checks_passed = False

    print("\n" + "=" * 60)
    if checks_passed:
        print("✅ All critical prerequisites passed!\n")
        return True
    else:
        print("❌ Some prerequisites failed. Please fix them first.\n")
        return False


def run_simple_research_task():
    """Demonstrate a simple research task using DeerFlowClient."""

    print("\n" + "=" * 60)
    print("🎯 RUNNING SIMPLE RESEARCH TASK (Library Mode)")
    print("=" * 60)

    # Define the research query
    query = "What are the latest developments in quantum computing in 2026?"

    print(f"\n📝 Research Query: {query}\n")
    print("⏳ Starting research agent (no server required)...\n")

    # Initialize the client
    # This runs the agent directly in-process, no servers needed!
    client = DeerFlowClient()

    print("💡 Using DeerFlowClient in library mode")
    print("-" * 60)
    print("The agent will run locally with these capabilities:")
    print("  • Web search via Tavily API")
    print("  • Local LLM (Ollama with GLM-4-Flash)")
    print("  • No Gateway or LangGraph Server processes\n")

    # Method 1: Simple chat (non-streaming)
    print("\n💡 METHOD 1: Simple Chat (Non-streaming)")
    print("-" * 60)
    try:
        print("Sending query to agent...")
        response = client.chat(query)

        print("\n✅ Response received!")
        print("\n📊 Answer:")
        print("-" * 60)
        print(response)
        print("-" * 60)

    except Exception as e:
        print(f"⚠️  Error during chat: {e}")
        print("💡 This might be due to model configuration or API issues")

    # Method 2: Streaming (recommended for better UX)
    print("\n\n💡 METHOD 2: Streaming (Recommended)")
    print("-" * 60)
    try:
        print("Streaming response from agent...\n")

        for event in client.stream(query):
            if event.type == "messages-tuple" and event.data.get("type") == "ai":
                content = event.data.get("content", "")
                if content:
                    print(content, end="", flush=True)
            elif event.type == "end":
                usage = event.data.get("usage", {})
                print("\n\n" + "-" * 60)
                print(f"✅ Stream completed!")
                print(f"📊 Token usage:")
                print(f"   Input tokens: {usage.get('input_tokens', 0)}")
                print(f"   Output tokens: {usage.get('output_tokens', 0)}")
                print(f"   Total tokens: {usage.get('total_tokens', 0)}")

    except Exception as e:
        print(f"\n⚠️  Error during streaming: {e}")
        print("💡 You can try the non-streaming method instead")

    print("\n" + "=" * 60)


def show_configuration_info():
    """Display configuration information."""

    print("\n" + "=" * 60)
    print("📋 CONFIGURATION INFO")
    print("=" * 60)

    client = DeerFlowClient()

    # List available models
    print("\n📦 Available Models:")
    models = client.list_models()
    for model in models.get("models", []):
        name = model.get("name", "unknown")
        display = model.get("display_name", "")
        supports_thinking = model.get("supports_thinking", False)
        print(f"  • {name} {display}")
        if supports_thinking:
            print(f"    └─ Supports thinking mode ✅")

    # List enabled skills
    print("\n🛠️  Enabled Skills:")
    skills = client.list_skills(enabled_only=True)
    for skill in skills.get("skills", []):
        name = skill.get("name", "unknown")
        description = skill.get("description", "")[:60]
        category = skill.get("category", "")
        print(f"  • {name} ({category})")
        print(f"    └─ {description}...")

    print("\n" + "=" * 60)


def show_next_steps():
    """Display suggested next steps for the user."""

    print("\n🎉 CONGRATULATIONS! You've used DeerFlow as a library!")
    print("\n" + "=" * 60)
    print("📚 NEXT STEPS TO EXPLORE")
    print("=" * 60)

    print("\n1. 🔄 Try Multi-turn Conversations")
    print("   → Use thread_id to maintain conversation context")
    print("   → Example: client.chat('follow-up question', thread_id='my-thread')")

    print("\n2. 📖 Explore Advanced Features")
    print("   → File uploads: client.upload_files(thread_id, ['file.pdf'])")
    print("   → Artifacts: client.get_artifact(thread_id, 'path/to/file.txt')")
    print("   → Memory: client.get_memory_status()")

    print("\n3. 🔧 Customize Configuration")
    print("   → Edit config.yaml to change models")
    print("   → Enable/disable skills in extensions_config.json")

    print("\n4. 🚀 Try Different Use Cases")
    print("   → Code generation tasks")
    print("   → Document/report creation")
    print("   → Data analysis with sandbox")

    print("\n5. 📝 Check Documentation")
    print("   → See deer-flow/backend/docs/README.md")
    print("   → Review client.py docstrings for API details")

    print("\n" + "=" * 60)
    print("💬 Example Code Snippets:")
    print("=" * 60)

    examples = [
        "# Simple one-shot",
        "client = DeerFlowClient()",
        "response = client.chat('hello')",
        "",
        "# Streaming with thread context",
        "for event in client.stream('query', thread_id='conv-1'):",
        "    print(event.data)",
        "",
        "# With custom model",
        "response = client.chat('query', model_name='ollama-glm4-flash')",
        "",
        "# Enable plan mode",
        "response = client.chat('complex task', plan_mode=True)",
    ]

    for line in examples:
        print(line)

    print("\n" + "=" * 60)


def main():
    """Main entry point."""

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='DeerFlow Hello World Demo')
    parser.add_argument('--test', action='store_true', help='Run diagnostics only')
    args = parser.parse_args()

    # If --test flag is provided, run diagnostics only
    if args.test:
        success = run_diagnostics()
        sys.exit(0 if success else 1)

    print("\n" + "=" * 60)
    print("🦌 DEERFLOW HELLO WORLD - LIBRARY MODE DEMO")
    print("=" * 60)
    print("\nWelcome to DeerFlow Client Library!")
    print("Mode: Embedded (No Servers Required)")
    print("Model: Configured in config.yaml")
    print("Search: Tavily API\n")
    print("💡 IMPORTANT: This script should be run from the deer-flow/backend directory")
    print("   to ensure correct configuration path resolution.\n")

    # Check prerequisites
    if not check_prerequisites():
        print("\n⚠️  Some checks failed.")
        print("You can continue, but the demo might not work properly.")
        choice = input("\nContinue anyway? (y/n): ").lower().strip()
        if choice != 'y':
            print("\n👋 Exiting. Please fix the issues and try again.")
            sys.exit(0)

    # Show configuration info
    show_configuration_info()

    # Run the demo
    run_simple_research_task()

    # Show next steps
    show_next_steps()

    print("\n✨ Happy researching with DeerFlow Client! ✨\n")


if __name__ == "__main__":
    main()
