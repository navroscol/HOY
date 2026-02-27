from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import org_id_header
from app.core.db import get_session
from app.models.entities import (
    Alert,
    Document,
    Incident,
    Quote,
    Shipment,
    ShipmentStatusHistory,
    Task,
    TrackingEvent,
)
from app.schemas.common import (
    AlertCreate,
    DocumentCreate,
    DocumentUpdate,
    IncidentCreate,
    QuoteCreate,
    ShipmentCreate,
    ShipmentStatusUpdate,
    TaskCreate,
    TaskUpdate,
    TrackingEventCreate,
)
from app.services.risk import compute_risk

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/shipments")
def create_shipment(
    payload: ShipmentCreate,
    org_id: int = Depends(org_id_header),
    session: Session = Depends(get_session),
):
    shipment = Shipment(org_id=org_id, **payload.model_dump())
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    session.add(
        ShipmentStatusHistory(
            shipment_id=shipment.id,
            from_status="none",
            to_status=shipment.status,
            changed_by="system",
        )
    )
    session.commit()
    return shipment


@router.get("/shipments")
def list_shipments(org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    return session.exec(select(Shipment).where(Shipment.org_id == org_id)).all()


@router.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: int, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    docs = session.exec(select(Document).where(Document.shipment_id == shipment_id)).all()
    events = session.exec(select(TrackingEvent).where(TrackingEvent.shipment_id == shipment_id)).all()
    shipment.risk_score = compute_risk(shipment, docs, events)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return {
        "shipment": shipment,
        "documents": docs,
        "events": events,
        "tasks": session.exec(select(Task).where(Task.shipment_id == shipment_id)).all(),
        "alerts": session.exec(select(Alert).where(Alert.shipment_id == shipment_id)).all(),
        "quotes": session.exec(select(Quote).where(Quote.shipment_id == shipment_id)).all(),
        "incidents": session.exec(select(Incident).where(Incident.shipment_id == shipment_id)).all(),
    }


@router.post("/shipments/{shipment_id}/status")
def update_status(shipment_id: int, payload: ShipmentStatusUpdate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    old = shipment.status
    shipment.status = payload.to_status
    session.add(shipment)
    session.add(ShipmentStatusHistory(shipment_id=shipment_id, from_status=old, to_status=payload.to_status, changed_by=payload.changed_by))
    session.commit()
    return shipment


@router.get("/shipments/{shipment_id}/status-history")
def status_history(shipment_id: int, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    return session.exec(select(ShipmentStatusHistory).where(ShipmentStatusHistory.shipment_id == shipment_id)).all()


@router.post("/shipments/{shipment_id}/tasks")
def create_task(shipment_id: int, payload: TaskCreate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    task = Task(shipment_id=shipment_id, **payload.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    shipment = session.get(Shipment, task.shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="task not found")
    task.status = payload.status
    session.add(task)
    session.commit()
    return task


@router.post("/shipments/{shipment_id}/documents")
def create_document(shipment_id: int, payload: DocumentCreate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    doc = Document(shipment_id=shipment_id, status="uploaded", **payload.model_dump())
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc


@router.patch("/documents/{doc_id}")
def update_document(doc_id: int, payload: DocumentUpdate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    shipment = session.get(Shipment, doc.shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="document not found")
    doc.status = payload.status
    doc.validation_errors = payload.validation_errors
    session.add(doc)
    session.commit()
    return doc


@router.post("/shipments/{shipment_id}/events")
def create_event(shipment_id: int, payload: TrackingEventCreate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    event = TrackingEvent(shipment_id=shipment_id, **payload.model_dump())
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.post("/shipments/{shipment_id}/alerts")
def create_alert(shipment_id: int, payload: AlertCreate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    alert = Alert(shipment_id=shipment_id, **payload.model_dump())
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert


@router.post("/shipments/{shipment_id}/quotes")
def create_quote(shipment_id: int, payload: QuoteCreate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    quote = Quote(shipment_id=shipment_id, **payload.model_dump())
    session.add(quote)
    session.commit()
    session.refresh(quote)
    return quote


@router.post("/shipments/{shipment_id}/incidents")
def create_incident(shipment_id: int, payload: IncidentCreate, org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment or shipment.org_id != org_id:
        raise HTTPException(status_code=404, detail="shipment not found")
    incident = Incident(shipment_id=shipment_id, **payload.model_dump())
    session.add(incident)
    session.commit()
    session.refresh(incident)
    return incident


@router.get("/dashboard/executive")
def executive_dashboard(org_id: int = Depends(org_id_header), session: Session = Depends(get_session)):
    shipments = session.exec(select(Shipment).where(Shipment.org_id == org_id)).all()
    total = len(shipments)
    delayed = len([s for s in shipments if s.status in ["in_transit", "arrival"] and s.risk_score >= 50])
    on_time = total - delayed
    high_risk = [s for s in shipments if s.risk_score >= 60]
    return {
        "active_shipments": total,
        "on_time": on_time,
        "delayed": delayed,
        "avg_risk": int(sum([s.risk_score for s in shipments]) / total) if total else 0,
        "high_risk_shipments": high_risk,
    }
