# 🧬 Parasitologist AI Study Assistant

A stateful, AI-powered chatbot designed to assist students in tropical medicine and parasitology. Built with **LangChain**, **Groq (Llama 3)**, and **MongoDB Atlas**, this assistant maintains long-term conversation context to support complex clinical and diagnostic learning.

## 🌟 Key Features
- **Contextual Memory:** Integrates MongoDB to store and retrieve chat history, allowing the AI to follow complex, multi-turn discussions.
- **Expert Persona:** Role-played as a Senior Research Parasitologist with 30 years of experience.
- **Educational Guardrails:** Uses the Socratic method—providing hints and technical guidance rather than just giving away answers.
- **Structured Outputs:** Automatically formats parasite taxonomy, life cycles, and diagnostic standards using Markdown.

## 🏗️ System Architecture
The bot uses a "Database-as-Memory" pattern to ensure persistence across sessions:
1. **Input:** User asks a question.
2. **Retrieval:** The system queries MongoDB for the last 10 messages based on the `user_id`.
3. **Augmentation:** History is injected into the `ChatPromptTemplate` placeholder.
4. **Inference:** Groq processes the full context (System Prompt + History + Question).
5. **Storage:** Both the question and response are saved back to MongoDB with UTC timestamps.



## 🛠️ Tech Stack
- **LLM:** Groq (Llama-3.3-70b-versatile)
- **Orchestration:** LangChain
- **Database:** MongoDB Atlas (NoSQL)
- **Deployment:** Render
- **Environment Management:** Python Dotenv

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- A MongoDB Atlas Account
- A Groq API Key

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/B-Negro/AI_Study_Assistant.git](https://github.com/B-Negro/AI_Study_Assistant.git)
cd AI_Study_Assistant

# Create and activate virtual environment
py -3.12 -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
