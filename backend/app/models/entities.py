from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class ShipmentMode(str, Enum):
    air = "air"
    ocean = "ocean"


class DocStatus(str, Enum):
    missing = "missing"
    uploaded = "uploaded"
    needs_fix = "needs_fix"
    approved = "approved"


class TaskStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    done = "done"


class ShipmentStatus(str, Enum):
    draft = "draft"
    ready_for_quote = "ready_for_quote"
    booked = "booked"
    pickup = "pickup"
    origin_cleared = "origin_cleared"
    in_transit = "in_transit"
    arrival = "arrival"
    delivery = "delivery"
    closed = "closed"


class Org(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(index=True)
    name: str
    email: str
    role: str


class Shipment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(index=True)
    mode: ShipmentMode
    vertical: str
    origin: str
    destination: str
    incoterm: str
    commodity: str
    weight_kg: float
    packages: int
    eta_current: Optional[datetime] = None
    risk_score: int = 0
    status: ShipmentStatus = ShipmentStatus.draft
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ShipmentStatusHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipment_id: int = Field(index=True)
    from_status: str
    to_status: str
    changed_by: str
    changed_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipment_id: int = Field(index=True)
    title: str
    owner: str
    priority: str = "medium"
    due_at: Optional[datetime] = None
    status: TaskStatus = TaskStatus.open


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipment_id: int = Field(index=True)
    doc_type: str
    status: DocStatus = DocStatus.missing
    file_name: Optional[str] = None
    validation_errors: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TrackingEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipment_id: int = Field(index=True)
    source: str
    milestone_code: str
    location: str
    event_at: datetime
    raw_payload: Optional[str] = None


class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipment_id: int = Field(index=True)
    alert_type: str
    severity: str
    channel: str
    status: str = "sent"
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Quote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipment_id: int = Field(index=True)
    total_estimated: float
    fee_amount: float
    currency: str = "USD"
    assumptions: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Incident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipment_id: int = Field(index=True)
    type: str
    status: str = "open"
    owner: str
    summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
