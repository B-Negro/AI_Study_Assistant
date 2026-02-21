import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
from datetime import datetime,timezone
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
mongo_url = os.getenv("MONGODB_URL")

#set up MongoDB connection
client = MongoClient(mongo_url)
db = client['chat_bot']
collection = db['user']

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    question: str   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI Study Assistant. 
    1. Use the provided conversation history to maintain context.
    2. Explain concepts clearly and provide examples.
    3. If a student is stuck on a problem, give them a hint rather than the full solution first.
    4. Stay professional and academic in tone."""),
    ("placeholder", "{history}"), 
    ("user", "{question}")
])
#Initializing the "Brain"
llm= ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant")
chain = prompt | llm

def get_history(user_id):
    #fetch the conversation history for the user from MongoDB
    chats= collection.find({"user_id": user_id}).sort("timestamp", 1)
    history = []

    for chat in chats:
        history.append({"role": chat["role"], "content": chat["message"]}) 
    return history

@app.get("/") # Define a simple route to test the API
def home():
    return {"message": "Welcome to the Parasitology Chatbot API!"}
@app.post("/chat") # Define a route to handle chat interactions
def chat(request: ChatRequest):
        # Get the conversation history for the user
        history = get_history(request.user_id)
    
        # Generate a response using the chain
        response = chain.invoke({"history": history, "question": request.question})
    
        # Save the user's question and the assistant's response to MongoDB
        collection.insert_one({
            "user_id": request.user_id,
            "role": "user",
            "message": request.question,
            "timestamp": datetime.now(timezone.utc)
        })
        collection.insert_one({
            "user_id": request.user_id,
            "role": "assistant",
            "message": response.content,
            "timestamp": datetime.now(timezone.utc)
        })
    
        return {"response": response.content}
