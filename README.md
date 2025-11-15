🛠️ AI Warranty Checker

An intelligent warranty checking system built using LangGraph, LangChain, Streamlit, and agentic reasoning with State Graph Agent + ReAct architecture.

🚀 Overview

AI Warranty Checker is an AI-powered application designed to analyze product details, extract important warranty information, and return clear, structured responses to users.
It automates reading warranty documents, receipts, or user-provided text and determines:

Warranty validity

Duration & expiry date

Terms & conditions

Coverage & exclusions

Additional required actions

The app provides a simple, interactive UI using Streamlit, while the backend uses advanced agentic workflows for reliable reasoning.

🧠 Tech Stack
🔹 LangGraph

Used to build the agent workflow using a State Graph Agent, allowing controlled, deterministic multi-step reasoning.

🔹 LangChain

Handles:

LLM orchestration

Document parsing

Prompting

ReAct-style reasoning traces

🔹 ReAct Agent

Implements Reason + Act loops for:

Extracting warranty terms

Calling internal tools

Making logical decisions based on documents

This improves accuracy for complex or ambiguous warranty texts.

🔹 Streamlit (Frontend)

Provides a clean, fast UI for users to:

Upload receipts/invoices/warranty cards

Enter product details

View AI-generated warranty analysis

📌 Features

🔍 Automatic warranty extraction

📄 Supports PDFs, text, and image-to-text (if integrated)

⏳ Checks warranty validity & expiry

🧩 AI reasoning with multi-step ReAct agent

⚙️ Extensible LangGraph workflow

🖥️ Simple Streamlit UI
