#!/usr/bin/env python3
"""
Quick test to verify DeerFlowClient is working correctly.

This script performs basic sanity checks without running a full research task.
Run this first to ensure your setup is correct before running hello_world_library.py

Usage:
    python test_deerflow_client.py
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_import():
    """Test if DeerFlowClient can be imported."""
    print("📦 Testing DeerFlowClient import...")
    try:
        from deerflow.client import DeerFlowClient
        print("   ✅ Import successful!")
        return True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        print("\n💡 Solution:")
        print("   1. Navigate to deer-flow/backend directory")
        print("   2. Run: uv sync")
        print("      This installs deerflow-harness package locally")
        print("   3. Try running this test again")
        print("\n📚 Installation command:")
        print("   cd deer-flow/backend && uv sync")
        print("\n⚠️  Important: deerflow-harness is not on PyPI.")
        print("   It must be installed from the local source.")
        return False


def test_initialization():
    """Test if DeerFlowClient can be initialized."""
    print("\n🔧 Testing DeerFlowClient initialization...")
    try:
        from deerflow.client import DeerFlowClient
        client = DeerFlowClient()
        print("   ✅ Client initialized successfully!")
        return client
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        print("\n💡 Possible issues:")
        print("   - Missing config.yaml file")
        print("   - Environment variables not set")
        print("   - Dependencies not installed")
        return None


def test_list_models(client):
    """Test listing available models."""
    print("\n📋 Testing list_models()...")
    try:
        models = client.list_models()
        model_list = models.get("models", [])
        
        if model_list:
            print(f"   ✅ Found {len(model_list)} model(s):")
            for model in model_list[:3]:  # Show first 3
                name = model.get("name", "unknown")
                display = model.get("display_name", "")
                print(f"      • {name} {display}")
            if len(model_list) > 3:
                print(f"      ... and {len(model_list) - 3} more")
            return True
        else:
            print("   ⚠️  No models configured")
            return False
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False


def test_list_skills(client):
    """Test listing enabled skills."""
    print("\n🛠️  Testing list_skills()...")
    try:
        skills = client.list_skills(enabled_only=True)
        skill_list = skills.get("skills", [])
        
        if skill_list:
            print(f"   ✅ Found {len(skill_list)} enabled skill(s):")
            for skill in skill_list[:5]:  # Show first 5
                name = skill.get("name", "unknown")
                category = skill.get("category", "")
                print(f"      • {name} ({category})")
            if len(skill_list) > 5:
                print(f"      ... and {len(skill_list) - 5} more")
            return True
        else:
            print("   ℹ️  No skills enabled (this is okay)")
            return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False


def test_env_vars():
    """Test if required environment variables are set."""
    print("\n🔑 Testing environment variables...")
    
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key and tavily_key != "your-tavily-api-key-here":
        print(f"   ✅ TAVILY_API_KEY is set (length: {len(tavily_key)})")
        return True
    else:
        print("   ❌ TAVILY_API_KEY not set or invalid")
        print("\n💡 Solution:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env and add your Tavily API key")
        print("   3. Get a free key at: https://app.tavily.com")
        return False


def test_simple_chat(client):
    """Test a very simple chat query."""
    print("\n💬 Testing simple chat (non-streaming)...")
    try:
        response = client.chat("Say 'hello' in one word")
        
        if response and len(response.strip()) > 0:
            print(f"   ✅ Response received: '{response.strip()}'")
            return True
        else:
            print("   ⚠️  Empty response received")
            return False
    except Exception as e:
        print(f"   ❌ Chat failed: {e}")
        print("\n💡 This might be due to:")
        print("   - Ollama not running")
        print("   - Model not available")
        print("   - API configuration issues")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 DEERFLOW CLIENT TEST SUITE")
    print("=" * 60)
    print()
    
    # Track overall success
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Import
    tests_total += 1
    if test_import():
        tests_passed += 1
    
    # Test 2: Environment variables
    tests_total += 1
    if test_env_vars():
        tests_passed += 1
    
    # Test 3: Initialization
    tests_total += 1
    client = test_initialization()
    if client:
        tests_passed += 1
        
        # Test 4: List models
        tests_total += 1
        if test_list_models(client):
            tests_passed += 1
        
        # Test 5: List skills
        tests_total += 1
        if test_list_skills(client):
            tests_passed += 1
        
        # Test 6: Simple chat
        tests_total += 1
        if test_simple_chat(client):
            tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n✅ ALL TESTS PASSED!")
        print("\n🎉 Your setup is working correctly!")
        print("   You can now run: python hello_world_library.py")
    else:
        print("\n⚠️  Some tests failed.")
        print("   Please review the errors above and fix them.")
        print("   Critical tests: import, initialization, environment")
    
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if tests_passed == tests_total else 1)


if __name__ == "__main__":
    main()
