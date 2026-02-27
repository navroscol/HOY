from app.models.entities import Document, Shipment, TrackingEvent


def compute_risk(shipment: Shipment, documents: list[Document], events: list[TrackingEvent]) -> int:
    risk = 0
    if any(doc.status in ["missing", "needs_fix"] for doc in documents):
        risk += 35
    if shipment.mode == "ocean":
        risk += 10
    if len(events) < 2:
        risk += 20
    if shipment.weight_kg <= 0 or shipment.packages <= 0:
        risk += 30
    return min(100, risk)
