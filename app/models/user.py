from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    uid: str
    nome: str
    email: str
    created_at: datetime = field(default_factory=datetime.utcnow)
