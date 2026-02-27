from datetime import datetime, timedelta

from sqlmodel import Session

from app.core.db import engine, init_db
from app.models.entities import Alert, Document, Incident, Org, Quote, Shipment, Task, TrackingEvent


def run():
    init_db()
    with Session(engine) as s:
        org = Org(name="Demo Export SAS")
        s.add(org)
        s.commit()
        s.refresh(org)

        sh1 = Shipment(
            org_id=org.id,
            mode="ocean",
            vertical="cafe",
            origin="Cartagena, CO",
            destination="Rotterdam, NL",
            incoterm="FOB",
            commodity="Cafe verde",
            weight_kg=12000,
            packages=480,
            eta_current=datetime.utcnow() + timedelta(days=18),
            status="in_transit",
            risk_score=42,
        )
        sh2 = Shipment(
            org_id=org.id,
            mode="air",
            vertical="insumos_electronicos",
            origin="Bogota, CO",
            destination="Miami, US",
            incoterm="CIP",
            commodity="Componentes de PCB",
            weight_kg=920,
            packages=36,
            eta_current=datetime.utcnow() + timedelta(days=2),
            status="pickup",
            risk_score=66,
        )
        s.add(sh1)
        s.add(sh2)
        s.commit()
        s.refresh(sh1)
        s.refresh(sh2)

        s.add(Document(shipment_id=sh2.id, doc_type="invoice", status="needs_fix", file_name="invoice_v2.pdf", validation_errors="HS code mismatch"))
        s.add(Task(shipment_id=sh2.id, title="Corregir invoice", owner="cliente", priority="high"))
        s.add(TrackingEvent(shipment_id=sh1.id, source="partner", milestone_code="DEPARTED", location="Cartagena", event_at=datetime.utcnow() - timedelta(days=4)))
        s.add(Alert(shipment_id=sh2.id, alert_type="doc_missing", severity="high", channel="email", message="Falta corrección de factura"))
        s.add(Quote(shipment_id=sh1.id, total_estimated=6400, fee_amount=350, currency="USD", assumptions="FOB + THC estimado"))
        s.add(Incident(shipment_id=sh2.id, type="docs_rejected", owner="ops", summary="Factura rechazada por inconsistencias"))
        s.commit()

        print(f"Seed ready. org_id={org.id}")


if __name__ == "__main__":
    run()
