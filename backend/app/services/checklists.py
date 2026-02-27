from app.models.entities import ShipmentMode

_BASE_DOCS = ["invoice", "packing_list", "transport_doc"]

_VERTICAL_EXTRA = {
    "cafe": ["coo", "quality_cert"],
    "cacao": ["coo", "quality_cert"],
    "autopartes": ["technical_sheet"],
    "insumos_electronicos": ["technical_sheet", "compliance_cert"],
    "tech_gadgets": ["technical_sheet", "compliance_cert"],
    "instrumentos_musicales": ["material_declaration"],
}

_MODE_EXTRA = {
    ShipmentMode.air: ["awb"],
    ShipmentMode.ocean: ["bl"],
}


def required_documents(vertical: str, mode: ShipmentMode | str) -> list[str]:
    docs = list(_BASE_DOCS)
    docs.extend(_VERTICAL_EXTRA.get(vertical, []))
    docs.extend(_MODE_EXTRA.get(mode, []))
    return sorted(set(docs))
