from fastapi import Header, HTTPException


def org_id_header(x_org_id: int | None = Header(default=None)) -> int:
    if not x_org_id:
        raise HTTPException(status_code=401, detail="x-org-id header required")
    return x_org_id
