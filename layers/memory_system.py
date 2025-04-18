import pymongo
import sqlite3
import google.generativeai as genai
import json
from config import MONGO_URI, MONGO_DB_NAME, MONGO_STM_COLLECTION, MONGO_LTM_COLLECTION, SQLITE_DB_PATH, GENAI_MODEL_NAME, GENAI_MAX_TOKENS, GENAI_TEMPERATURE
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

class MemorySystem:
    def __init__(self):
        # Connect to MongoDB
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.stm_collection = self.db[MONGO_STM_COLLECTION]
        self.ltm_collection = self.db[MONGO_LTM_COLLECTION]
        self.factual_memory_collection = self.db["factual_memory"]

        # Connect to SQLite for feedback storage
        self.sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        self.sqlite_cursor = self.sqlite_conn.cursor()

        # Ensure feedback table exists
        self.sqlite_cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                user_id TEXT,
                feedback TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.sqlite_conn.commit()
#done #factual memory storing from analysis
#done #redine get stm memory to get only the last 10 entries and it ill not remove the stm till the session is ot completed and get updated with secondary nlu all after 

#repair stm_to_ltm function logic to get limited patterns of the user only and extract in the factual memory collection and only create when session in end and only use updated stm from nlu secondary's origin for summary 
#redifine get Ltm context
#for understanding the context model should use only limited memory if it is not required to analysis full
#redifine get Ltm context 
#search for factual memory
#and this is for nlu secondary (it will consist control of all memory and other layers also except nlu primary for better simulate of automate system for extract what ever is needed on that particular time.).
    def store_in_stm(self, user_id, user_input, analysis):
        """
        Stores user input and analysis in STM. If more than 5 entries exist, removes the oldest one.
        Returns the ID of the inserted STM entry.
        """
        # Fetch current STM records
        stm_entries = list(self.stm_collection.find({"user_id": user_id}))

        # Insert new STM entry (includes user input and analysis)
        inserted_entry = self.stm_collection.insert_one({
            "user_id": user_id,
            "user_input": user_input,
            "analysis": analysis,
            "timestamp": datetime.utcnow()
        })    
        
        # If STM exceeds 10 entries, remove the oldest
        if len(stm_entries) >= 10:
            oldest_entry = stm_entries[0]  # First inserted entry
            self.stm_collection.delete_one({"_id": oldest_entry["_id"]})

        return str(inserted_entry.inserted_id)  # Return ID of the inserted STM record
    
    def update_stm_with_output(self, stm_id, chatbot_output):
        """
        Updates the specified STM entry with the chatbot's generated output.
        """
        result = self.stm_collection.update_one(
            {"_id": ObjectId(stm_id)},  # Find document by ID
            {"$set": {"chatbot_output": chatbot_output}}  # Update with chatbot's response
        )
        
        if result.modified_count > 0:
            return f"Updated STM entry {stm_id} with chatbot output."
        else:
            return f"Failed to update STM entry {stm_id}."
    
    def generate_summary(self, user_id):
        """
        Generates a summary of the last 5 STM entries using Gemini AI and formats it for LTM.
        """
        # Fetch last 5 STM entries
        stm_entries = list(self.stm_collection.find({"user_id": user_id}))[-5:]

        if not stm_entries:
            return None  # No entries to summarize

        # Extract analysis texts
        analysis_texts = [entry["analysis"] for entry in stm_entries]

        # Define system prompt for Gemini AI
        system_prompt = f"""
        You are an AI chatbot memory summarizer. Your job is to process multiple short-term memory (STM) entries 
        and create a structured summary that can be stored in long-term memory (LTM).

        Instructions:
        - Analyze the last 5 user interactions.
        - Identify recurring topics, intents, and emotions.
        - Extract key insights and relationships between past statements.
        - Format the summary as structured JSON.

        Example Format:
        {{
            "summary": "...",
            "key_topics": [...],
            "dominant_emotion": "...",
            "patterns_detected": [...],
            "user_preferences": "...",
            "important_statements": [...]
        }}

        STM Entries:
        {analysis_texts}
        """

        try:
            model = genai.GenerativeModel(GENAI_MODEL_NAME)
            response = model.generate_content(system_prompt, generation_config=genai.GenerationConfig(
                max_output_tokens=GENAI_MAX_TOKENS,
                temperature=GENAI_TEMPERATURE,
            ))

            extracted_text = response.text.strip() if hasattr(response, "text") else ""
            extracted_text = extracted_text.replace("```json", "").replace("```", "").strip()

            try:
                summary_json = json.loads(extracted_text)
                return summary_json  # Return structured summary
            except json.JSONDecodeError:
                return {"error": f"Invalid JSON: {extracted_text}"}

        except Exception as e:
            return {"error": f"Summary Generation Error: {e}"}

    def transfer_stm_to_ltm(self, user_id):
        """
        Generates a summary of STM and stores it in LTM.
        """
        summary = self.generate_summary(user_id)

        if summary and "error" not in summary:
            self.ltm_collection.insert_one({"user_id": user_id, "ltm_summary": summary})
            return "Summary added to LTM."
        return "No STM data to summarize."
    
    def get_ltm_context(self, user_id):
        """
        Retrieves LTM context for a given user.
        """
        ltm_entries = list(self.ltm_collection.find({"user_id": user_id}))
        if not ltm_entries:
            return None  # No LTM data found
        
        # Extract only the latest stored LTM summary
        latest_ltm_summary = ltm_entries[-1].get("ltm_summary", {})
        return latest_ltm_summary
    
    def get_stm_memory(self, user_id):
        """
        Retrieves all STM memory entries for a given user.
        """
        stm_entries = list(self.stm_collection.find({"user_id": user_id}))
        return stm_entries if stm_entries else None

memory_system = MemorySystem()
