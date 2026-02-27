# Digital Freight Desk — MVP ejecutable

MVP completo (portal + API) para una Control Tower logística de pymes exportadoras/importadoras en Colombia.

## Qué incluye

- **Backend FastAPI multi-tenant por `x-org-id`**
  - Shipments + state machine + historial
  - Tasks
  - Documents Hub (estados + errores)
  - Tracking timeline
  - Alerts
  - Quotes
  - Incidents
  - Dashboard ejecutivo
- **Frontend Next.js**
  - Dashboard ejecutivo
  - Shipments board
  - Shipment detail con docs/timeline/tasks/quotes/incidents
- **Seed de datos demo** para mostrar flujo end-to-end.

## Ejecutar con Docker

```bash
docker compose up --build
```

API: `http://localhost:8000/api/health`
Portal: `http://localhost:3000`

## Seed de datos demo

En otra terminal:

```bash
docker compose exec api python scripts/seed.py
```

Esto crea una organización demo con `org_id=1`.

## Ejecutar backend local (sin Docker)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Ejecutar frontend local (sin Docker)

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000/api NEXT_PUBLIC_ORG_ID=1 npm run dev
```

## Tests backend

```bash
cd backend
pytest
```

## Endpoints principales

- `POST /api/shipments`
- `GET /api/shipments`
- `GET /api/shipments/{id}`
- `POST /api/shipments/{id}/status`
- `POST /api/shipments/{id}/documents`
- `POST /api/shipments/{id}/events`
- `POST /api/shipments/{id}/quotes`
- `POST /api/shipments/{id}/incidents`
- `GET /api/dashboard/executive`
- `GET /api/tasks?status=&owner=`
- `GET /api/ops/today`

> Header requerido en endpoints de negocio: `x-org-id`.
