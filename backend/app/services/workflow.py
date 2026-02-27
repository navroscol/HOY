from app.models.entities import ShipmentStatus

_ALLOWED: dict[ShipmentStatus, set[ShipmentStatus]] = {
    ShipmentStatus.draft: {ShipmentStatus.ready_for_quote},
    ShipmentStatus.ready_for_quote: {ShipmentStatus.booked, ShipmentStatus.draft},
    ShipmentStatus.booked: {ShipmentStatus.pickup},
    ShipmentStatus.pickup: {ShipmentStatus.origin_cleared},
    ShipmentStatus.origin_cleared: {ShipmentStatus.in_transit},
    ShipmentStatus.in_transit: {ShipmentStatus.arrival},
    ShipmentStatus.arrival: {ShipmentStatus.delivery},
    ShipmentStatus.delivery: {ShipmentStatus.closed},
    ShipmentStatus.closed: set(),
}


def can_transition(from_status: ShipmentStatus, to_status: ShipmentStatus) -> bool:
    return to_status in _ALLOWED.get(from_status, set())
