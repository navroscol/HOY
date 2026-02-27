# Digital Freight Desk — Control Tower Logística (Aéreo + Marítimo)

## 1) Visión de producto (tech-first)

**Objetivo:** operar como una Control Tower para pymes exportadoras/importadoras en Colombia, reduciendo:
- errores documentales y rechazos,
- costos sorpresa (demoras, almacenajes, reprocesos),
- incertidumbre operativa (ETA, responsabilidades, bloqueos).

**Diferenciador:** no competir por “flete más barato”, sino por **orquestación + visibilidad + compliance + alertas + SLA**.

## 2) Alcance funcional objetivo

### A. Portal web multi-tenant
- Landing con propuesta de valor, SLA de respuesta y formulario de cotización/evaluación.
- Login por organización.
- Módulos del portal:
  - Shipments (estado, ETA, riesgo),
  - Quote/Fee (estimado, fee, extras previstos),
  - Docs Hub (checklist, plantillas, validación),
  - Tracking (timeline + mapa + alertas),
  - Tasks (cliente/equipo/partner),
  - Incidents (demoras, holds, reclamos, rechazos).

### B. Motor de workflow (Shipment OS)
Cada embarque es un objeto vivo con:
- estado actual,
- historial,
- checklist,
- tareas,
- eventos.

**Estados base:**
`Draft → Ready-for-Quote → Booked → Pickup → Origin Cleared → In Transit → Arrival → Delivery → Closed`

### C. Document Intelligence
- Repositorio por embarque con versionado.
- Validador de documentos clave (presencia + reglas).
- Reglas iniciales:
  - campos obligatorios,
  - coherencia peso/bultos/Incoterm/HS,
  - consistencia shipper/consignee,
  - alertas de documentación incompleta.
- Plantillas: invoice, packing list, carta de instrucción.

### D. Tracking + Event Broker
- Modelo unificado de eventos para aéreo y marítimo.
- MVP: ingesta manual/CSV/email partner.
- V1: 1 integración real (carrier API o agregador).
- Alertas automáticas:
  - ETA drift,
  - missing milestone,
  - cut-off cercano,
  - hold/documento faltante.

### E. Capa compliance Colombia (sin reemplazar actor regulado)
- Checklist documental de referencia DIAN/ProColombia por vertical y modo.
- Control documental y trazabilidad.
- Sin presentar declaraciones en nombre del cliente.

## 3) Arquitectura técnica recomendada

### Stack MVP
- **Frontend:** Next.js + Tailwind.
- **Auth:** Clerk/Auth0.
- **Backend API:** FastAPI (Python) o NestJS (Node).
- **DB:** Postgres (Supabase/Neon/RDS).
- **Files:** S3-compatible (R2/S3) + metadata en Postgres.
- **Jobs/colas:** Celery + Redis (Python) / BullMQ + Redis (Node).
- **Observabilidad:** Sentry + uptime monitor.

### Diseño de servicios
1. **Portal App** (UI + Auth).
2. **Core API** (shipments, tasks, docs, quotes, incidents).
3. **Workflow Engine** (state machine + reglas de transición).
4. **Document Validator** (reglas básicas y score).
5. **Event Broker** (normaliza tracking y dispara alertas).
6. **Notification Service** (email/WhatsApp).
7. **Analytics Layer** (dashboards ejecutivos y operativos).

## 4) Modelo de datos mínimo (MVP)

```sql
-- Tenancy / usuarios
orgs(id, name, plan, created_at)
users(id, org_id, role, email, phone, created_at)
partners(id, name, type, contact_email, contact_phone)

-- Operación
shipments(
  id, org_id, mode, vertical, incoterm, hs_code, commodity,
  origin, destination, shipper, consignee,
  weight_kg, packages, value_amount, value_currency,
  eta_current, risk_score, created_at
)
shipment_status_history(id, shipment_id, from_status, to_status, changed_by, changed_at)
tasks(id, shipment_id, owner_user_id, title, priority, due_at, status)

-- Documentos
documents(
  id, shipment_id, doc_type, status, file_key, version,
  validation_errors_json, uploaded_by, uploaded_at
)

-- Tracking y alertas
tracking_events(
  id, shipment_id, source, milestone_code, event_at,
  location, confidence, raw_payload_json
)
alerts(id, shipment_id, alert_type, severity, channel, status, payload_json, created_at)

-- Costos
quotes(id, shipment_id, version, assumptions, fee_amount, total_estimated, currency, valid_until)
actual_costs(id, shipment_id, category, amount, currency, evidence_doc_id, created_at)

-- Incidencias
incidents(id, shipment_id, type, status, owner_user_id, summary, created_at)
incident_actions(id, incident_id, action_type, owner_user_id, due_at, status)
```

## 5) Endpoints API (REST) sugeridos

### Auth / Tenant
- `POST /auth/login`
- `GET /me`
- `GET /orgs/:orgId/users`

### Shipments
- `POST /shipments`
- `GET /shipments`
- `GET /shipments/:id`
- `PATCH /shipments/:id`
- `POST /shipments/:id/status`
- `GET /shipments/:id/status-history`

### Tasks
- `POST /shipments/:id/tasks`
- `GET /tasks?status=&owner=&due_before=`
- `PATCH /tasks/:taskId`

### Documents
- `POST /shipments/:id/documents/presign-upload`
- `POST /shipments/:id/documents`
- `GET /shipments/:id/documents`
- `POST /documents/:docId/validate`
- `PATCH /documents/:docId/status`

### Tracking
- `POST /shipments/:id/events` (manual)
- `POST /tracking/import/csv`
- `POST /tracking/webhook/:source`
- `GET /shipments/:id/timeline`

### Alerts
- `GET /alerts`
- `POST /alerts/:id/ack`
- `POST /alerts/:id/resolve`

### Quotes / Costs
- `POST /shipments/:id/quotes`
- `GET /shipments/:id/quotes`
- `POST /shipments/:id/actual-costs`
- `GET /shipments/:id/cost-summary`

### Incidents
- `POST /shipments/:id/incidents`
- `GET /incidents`
- `PATCH /incidents/:id`
- `POST /incidents/:id/actions`

## 6) Wireframes textuales por pantalla

### 6.1 Executive Dashboard
- KPI row: activos | on-time % | delayed % | riesgo promedio | SLA respuesta.
- Gráficos:
  - estimado vs real (mensual),
  - causas top de incidencias,
  - ETA drift por ruta.
- Tabla “Top embarques en riesgo”.

### 6.2 Shipments Board (operación)
- Vista kanban por estado.
- Filtros: modo, vertical, ruta, partner, incoterm, prioridad.
- Panel lateral “Atenciones hoy”: tareas vencidas + alertas P1 + eventos faltantes.

### 6.3 Documents Hub
- Checklist por embarque (Missing / Uploaded / Needs Fix / Approved).
- Botones: subir, validar, aprobar, comentar.
- Bloque de “Errores detectados” por documento.
- Acción: “Generar paquete de embarque (ZIP/PDF)”.

### 6.4 Tracking Timeline
- Línea de tiempo de milestones normalizados.
- Header con ETA actual y variación.
- Alertas activas.
- Mapa opcional (fase posterior).

### 6.5 Incidents & Claims
- Lista de incidentes por estado/severidad.
- Dentro del incidente:
  - resumen,
  - evidencia,
  - playbook sugerido,
  - tareas relacionadas,
  - post-mortem exportable.

## 7) Playbooks por vertical (enfoque inicial)

### Tech / Gadgets / Insumos electrónicos
- Alertas por descripciones genéricas.
- Revisión de consistencia HS/descripción/valor.
- Flags por posibles cargas sensibles (baterías, RF, componentes críticos).

### Autopartes
- Validación estricta de HS + uso/material.
- Alertas por discrepancias de unidad/peso.
- Checklist reforzada en documentación técnica.

### Instrumentos musicales
- Validación de materiales y embalaje.
- Riesgo por daño: checklist de evidencia fotográfica.
- Revisión de descripción detallada por pieza.

### Café y cacao
- Coherencia lote/peso neto-bruto.
- Checklist de origen/calidad según operación.
- Alertas por discrepancias entre invoice, packing y certificados.

## 8) Automatizaciones clave (1 persona operando)

1. **Doc-chaser automático**
   - Trigger: documento faltante + cut-off cercano.
   - Acción: notificación + tarea + escalamiento.

2. **ETA drift watchdog**
   - Trigger: variación ETA > umbral.
   - Acción: alerta al cliente + tarea interna de mitigación.

3. **Cost-surprise guard**
   - Trigger: evento de hold/demora/riesgo portuario.
   - Acción: incidente + bandera de sobrecosto + playbook.

4. **SLA bot**
   - Mide tiempo alerta→primera respuesta y muestra en dashboards.

## 9) Backlog Jira (sin fechas)

## EPIC 0 — Plataforma base
- Multi-tenant + aislamiento por `org_id`.
- RBAC y permisos en API/UI.
- MFA admin + auditoría de acceso.
- Audit logs de cambios operativos.

## EPIC 1 — Shipment OS
- CRUD de embarques air/ocean.
- State machine con transiciones válidas.
- Task engine con vencimientos y prioridades.
- Portal/Inbox para partners.

## EPIC 2 — Docs Hub
- Repositorio documental versionado.
- Checklists por vertical y modo.
- Estados doc + comentarios de corrección.
- Validaciones automáticas básicas.

## EPIC 3 — Quote Engine
- Cotización con supuestos y fee.
- Comparador estimado vs real.
- Requote por cambios críticos.

## EPIC 4 — Tracking
- Modelo estándar de eventos.
- Ingesta manual + CSV + email parser.
- Alertas ETA drift y missing milestones.
- Conector API inicial (1 fuente).

## EPIC 5 — Risk Engine
- Score 0–100 con razones explicables.
- Cola “Atenciones hoy” para operación.

## EPIC 6 — Incidentes y playbooks
- Registro de incidentes y evidencias.
- Playbooks por vertical.
- Post-mortem PDF 1 página.

## EPIC 7 — Notificaciones y SLA
- Motor multicanal (email/WhatsApp).
- Tracking de entrega/ack.
- Dashboard SLA (promedios y percentiles).

## EPIC 8 — Dashboards
- Ejecutivo cliente.
- Operativo interno.
- Scorecard de partners.

## EPIC 9 — Observabilidad y confiabilidad
- Error tracking + alertas.
- Integrations health.
- Backups + restore probado.

## 10) Dependencias y secuencia de implementación (sin fechas)

1. **Base técnica**: EPIC 0.
2. **Operación núcleo**: EPIC 1 + EPIC 2 (imprescindible para vender).
3. **Valor financiero**: EPIC 3.
4. **Visibilidad real**: EPIC 4.
5. **Escalabilidad operativa**: EPIC 5 + EPIC 7.
6. **Resiliencia operacional**: EPIC 6.
7. **Retención y expansión**: EPIC 8 + EPIC 9.

## 11) Definición de “listo para vender”

Se considera vendible cuando existe:
- Portal cliente con login multi-tenant,
- Shipments + tareas + docs checklist,
- Timeline de tracking (manual/CSV) con alertas,
- Cotización con fee y vista estimado,
- SLA de respuesta visible,
- Auditoría básica de acciones.

