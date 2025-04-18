from datetime import datetime, timedelta
import uuid

SESSION_TIMEOUT = timedelta(minutes=15)

class SessionManager:
    def __init__(self, mongo_client):
        self.db = mongo_client["your_database_name"]
        self.session_collection = self.db["active_sessions"]
        self.memory = None  # Will be linked to MemorySystem

    def create_session(self, user_id):
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()

        self.session_collection.insert_one({
            "session_id": session_id,
            "user_id": user_id,
            "start_time": now,
            "last_active_time": now,
            "status": "active"
        })
        return session_id

    def update_activity(self, session_id):
        self.session_collection.update_one(
            {"session_id": session_id, "status": "active"},
            {"$set": {"last_active_time": datetime.utcnow()}}
        )

    def check_and_expire_sessions(self):
        now = datetime.utcnow()
        expired_sessions = self.session_collection.find({
            "last_active_time": {"$lt": now - SESSION_TIMEOUT},
            "status": "active"
        })

        for session in expired_sessions:
            session_id = session["session_id"]
            self.expire_session(session_id)

    def expire_session(self, session_id):
        if self.memory:
            self.memory.stm_to_ltm(session_id)

        self.session_collection.update_one(
            {"session_id": session_id},
            {"$set": {"status": "expired"}}
        )
