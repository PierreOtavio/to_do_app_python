from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class NewTask:
    description: str
    complete: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)