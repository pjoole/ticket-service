from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class Ticket:
    event_name: str
    event_timestamp: str
    event_place: str
    seat: str
    owner: str
    id: str = uuid.uuid4().hex