#!/usr/bin/env python3
"""Task 3: Multiple MCP Servers - Orchestrating calculator and weather servers"""

import os
import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from dotenv import load_dotenv

load_dotenv()


model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


client = MultiServerMCPClient(
    {
        "calculator": {
            "command": "python",
            "args": ["./mcp_servers/calc_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "command": "python",
            "args": ["./mcp_servers/weather_server.py"],
            "transport": "stdio",
        }
    }
)

def print_header():
    print("""
╔══════════════════════════════════════════════╗
║           MCP AGENT CLI TOOL                 ║
╚══════════════════════════════════════════════╝
Type 'exit' or 'quit' to end the session.""")

async def run_multi_server_agent():
    """Create and run agent with multiple MCP servers"""
    print("\n🔄 Initializing MCP Agent...")
    
    try:
        print("🔧 Loading tools from MCP servers...")
        tools = await client.get_tools()
        agent = create_react_agent(model, tools)
        print("✅ Agent initialized successfully!")
        
        print("\n" + "="*60)
        print("🧪 Running test queries...")
        print("="*60)
        
        # Run test queries
        queries = [
            ("Calculator MCP", "What is 42 plus 58?"),
            ("Weather MCP", "What's the weather in London?"),
            ("Complex Math", "What's (3 + 5) x 12?"),
            ("Weather in Multiple Cities", "Compare the weather in New York and Tokyo"),
            ("Mixed Query", "If it's 20°C in Paris and temperature rises by 5 degrees, what will it be?")
        ]

        for test_name, query in queries:
            print(f"\n🔍 [{test_name}] Processing: {query}")
            print("-" * 80)
            response = await agent.ainvoke({"messages": query})
            print(f"\n📋 Result:")
            print("-" * 80)
            print(response['messages'][-1].content)
            print("=" * 80)
            
    except Exception as e:
        print(f"\n❌ Error initializing agent: {str(e)}")
        return

async def run_interactive_mode():
    """Run agent in interactive mode"""
    try:
        print("\n🔧 Loading tools from MCP servers...")
        tools = await client.get_tools()
        agent = create_react_agent(model, tools)
        print("✅ Agent ready! Type your query or 'exit' to quit.")
        
        while True:
            try:
                user_input = input("\n🔎 Your query: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Thank you for using MCP Agent. Goodbye!")
                    break
                    
                if not user_input:
                    print("⚠️  Please enter a valid query.")
                    continue
                    
                print("\n" + "="*60)
                print(f"🔍 Processing: {user_input}")
                print("="*60)
                
                response = await agent.ainvoke({"messages": user_input})
                
                print("\n📋 Result:")
                print("-"*60)
                print(response['messages'][-1].content)
                print("="*60)
                
            except KeyboardInterrupt:
                print("\n👋 Operation cancelled by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                
    except Exception as e:
        print(f"\n❌ Error initializing agent: {str(e)}")

if __name__ == "__main__":
    import sys
    
    print_header()
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Run test queries
        asyncio.run(run_multi_server_agent())
    else:
        # Run in interactive mode
        try:
            asyncio.run(run_interactive_mode())
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user. Goodbye!")
        except Exception as e:
            print(f"\n❌ Fatal error: {str(e)}")