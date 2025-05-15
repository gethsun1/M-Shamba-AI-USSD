from django.conf import settings
from django_redis import get_redis_connection
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class USSDSessionManager:
    def __init__(self):
        self.redis = get_redis_connection("default")
        self.session_timeout = 300  # 5 minutes

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session data with error handling and logging."""
        try:
            data = self.redis.get(f"ussd:session:{session_id}")
            if data:
                return json.loads(data)
            return {"level": 0, "data": {}, "retries": 0}
        except Exception as e:
            logger.error(f"Session retrieval error: {e}")
            return {"level": 0, "data": {}, "retries": 0}

    def save_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Save session data with error handling."""
        try:
            self.redis.setex(
                f"ussd:session:{session_id}",
                self.session_timeout,
                json.dumps(data)
            )
            return True
        except Exception as e:
            logger.error(f"Session save error: {e}")
            return False

    def increment_retry(self, session_id: str) -> int:
        """Track retry attempts for error recovery."""
        session = self.get_session(session_id)
        session["retries"] = session.get("retries", 0) + 1
        self.save_session(session_id, session)
        return session["retries"]

    def clear_session(self, session_id: str) -> None:
        """Clear session data."""
        try:
            self.redis.delete(f"ussd:session:{session_id}")
        except Exception as e:
            logger.error(f"Session clear error: {e}")

    def is_session_valid(self, session_id: str) -> bool:
        """Validate session existence and integrity."""
        try:
            return bool(self.redis.exists(f"ussd:session:{session_id}"))
        except Exception:
            return False 