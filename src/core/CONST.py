from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).replace(tzinfo=None)