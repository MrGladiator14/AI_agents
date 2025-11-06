#!/usr/bin/env python3
"""Task 7: Research Agent - Complete assistant with calculator + web search"""

import os
import time
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        print("Warning: DuckDuckGo search not available. Install with: pip install duckduckgo-search")
        class DDGS:
            def text(self, query, max_results=2):
                return []


class State(TypedDict):
    query: str
    query_type: str
    result: str

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    # api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)

ddgs = DDGS()

def classify_query(state: State):
    """Classifies query as math or search"""
    print("\n🔍 Analyzing query type...")
    time.sleep(0.5)

    query_lower = state["query"].lower()
    math_indicators = ["+", "-", "*", "/", "plus", "minus", "times", "divided",
                       "calculate", "sum", "multiply", "add", "subtract"]
    is_math = any(indicator in query_lower for indicator in math_indicators)
    query_type = "math" if is_math else "search"

    print(f"✅ Query classified as: {query_type.upper()}")
    return {"query_type": query_type}

def router(state: State):
    """Routes to appropriate tool"""
    if state["query_type"] == "math":
        print("➡️  Routing to calculator tool...")
        return "calculator_tool"
    print("➡️  Routing to search tool...")
    return "search_tool"

def calculator_tool(state: State):
    """Calculator for math queries"""
    print(f"🧮 Calculating: {state['query']}")
    time.sleep(0.5)

    response = llm.invoke(f"Calculate and return ONLY the answer: {state['query']}")
    answer = response.content.strip()
    
    print("✅ Calculation complete!")
    return {"result": f"\n📊 Calculation result: {answer}"}

def search_tool(state: State):
    """Web search for information queries"""
    print(f"🌐 Searching for: {state['query']}")
    time.sleep(0.5)

    try:
        results = ddgs.text(state["query"], max_results=2)

        if results:
            search_text = "\n".join([f"- {r.get('title', '')}: {r.get('body', '')[:100]}..."
                                     for r in results])
            time.sleep(1)
            print("✅ Search complete!")
            return {"result": f"\n🔍 Search results:\n{'-'*50}\n{search_text}\n{'-'*50}"}
        else:
            if "langgraph" in state["query"].lower():
                simulated = "LangGraph is a framework for building stateful, multi-step AI workflows using graphs."
                return {"result": f"\nℹ️  {simulated}"}
            return {"result": "\n❌ No search results found"}
    except Exception as e:
        print(f"⚠️  Search error: {str(e)}")
        if "langgraph" in state["query"].lower():
            return {"result": "\nℹ️  LangGraph is a framework for building stateful AI agents with graphs."}
        return {"result": f"\n⚠️  Search unavailable, but I can tell you: {state['query']} is an interesting topic!"}


workflow = StateGraph(State)

workflow.add_node("classify", classify_query)
workflow.add_node("calculator_tool", calculator_tool)
workflow.add_node("search_tool", search_tool)

workflow.set_entry_point("classify")
workflow.add_conditional_edges(
    "classify",
    router,
    {
        "calculator_tool": "calculator_tool",
        "search_tool": "search_tool"
    }
)

workflow.add_edge("calculator_tool", END)
workflow.add_edge("search_tool", END)

app = workflow.compile()

def run_cli():
    print("""
╔══════════════════════════════════════════════╗
║           RESEARCH AGENT CLI TOOL            ║
╚══════════════════════════════════════════════╝
Type 'exit' or 'quit' to end the session.""")

    while True:
        try:
            user_input = input("\n🔎 Enter your query: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Thank you for using Research Agent. Goodbye!")
                break
                
            if not user_input:
                print("⚠️  Please enter a valid query.")
                continue
                
            print("\n" + "="*60)
            print(f"🔍 Processing: {user_input}")
            print("="*60)
            
            result = app.invoke({
                "query": user_input,
                "query_type": "",
                "result": ""
            })
            
            print("\n" + "="*60)
            print("📋 RESULT:")
            print("-"*60)
            print(result['result'])
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    run_cli()
