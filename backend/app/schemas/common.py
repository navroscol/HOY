from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.entities import DocStatus, ShipmentMode, ShipmentStatus, TaskStatus


class ShipmentCreate(BaseModel):
    mode: ShipmentMode
    vertical: str
    origin: str
    destination: str
    incoterm: str
    commodity: str
    weight_kg: float
    packages: int
    eta_current: Optional[datetime] = None


class ShipmentStatusUpdate(BaseModel):
    to_status: ShipmentStatus
    changed_by: str = "system"


class TaskCreate(BaseModel):
    title: str
    owner: str
    priority: str = "medium"
    due_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    status: TaskStatus


class DocumentCreate(BaseModel):
    doc_type: str
    file_name: Optional[str] = None


class DocumentUpdate(BaseModel):
    status: DocStatus
    validation_errors: Optional[str] = None


class TrackingEventCreate(BaseModel):
    source: str
    milestone_code: str
    location: str
    event_at: datetime
    raw_payload: Optional[str] = None


class AlertCreate(BaseModel):
    alert_type: str
    severity: str
    channel: str
    message: str


class QuoteCreate(BaseModel):
    total_estimated: float
    fee_amount: float
    currency: str = "USD"
    assumptions: str


class IncidentCreate(BaseModel):
    type: str
    owner: str
    summary: str
