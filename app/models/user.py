from dataclass import dataclass
from datetime import datetime

@dataclass
class User:
    uid:str
    nome:str
    email:str
    created_at: datetime = field(defaul_facture=datatime.utcnow)