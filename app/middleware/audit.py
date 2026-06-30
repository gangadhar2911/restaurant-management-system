from datetime import datetime


class AuditLogger:

    def log(self, action: str, user_id: int = None, entity: str = None, entity_id: int = None):

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "user_id": user_id,
            "entity": entity,
            "entity_id": entity_id
        }

        # For now print (later store in DB audit_logs table)
        print("[AUDIT]", log_entry)