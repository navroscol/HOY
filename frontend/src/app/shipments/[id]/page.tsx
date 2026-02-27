import { SectionCard } from '@/components/SectionCard';
import { apiGet } from '@/lib/api';

export default async function ShipmentDetailPage({ params }: { params: { id: string } }) {
  const data = await apiGet(`/shipments/${params.id}`);
  const s = data.shipment;

  return (
    <div className="space-y-4">
      <SectionCard title={`Shipment #${s.id}`}>
        <p>{s.origin} → {s.destination} | {s.mode} | {s.status}</p>
        <p className="text-sm text-slate-400">Vertical: {s.vertical} • Riesgo: {s.risk_score}</p>
      </SectionCard>

      <div className="grid gap-4 md:grid-cols-2">
        <SectionCard title="Documents Hub">
          {data.documents.map((d: any) => (
            <div key={d.id} className="mb-2 rounded border border-slate-700 p-2 text-sm">
              {d.doc_type} — <span className="text-cyan-300">{d.status}</span>
              {d.validation_errors && <p className="text-amber-300">{d.validation_errors}</p>}
            </div>
          ))}
          {!data.documents.length && <p className="text-sm text-slate-400">Sin documentos aún.</p>}
        </SectionCard>

        <SectionCard title="Tracking Timeline">
          {data.events.map((e: any) => (
            <div key={e.id} className="mb-2 rounded border border-slate-700 p-2 text-sm">
              <p className="font-semibold">{e.milestone_code} — {e.location}</p>
              <p className="text-slate-400">{new Date(e.event_at).toLocaleString()}</p>
            </div>
          ))}
          {!data.events.length && <p className="text-sm text-slate-400">Sin eventos aún.</p>}
        </SectionCard>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <SectionCard title="Tasks">
          {data.tasks.map((t: any) => (
            <p key={t.id} className="mb-2 text-sm">• {t.title} ({t.status})</p>
          ))}
          {!data.tasks.length && <p className="text-sm text-slate-400">Sin tareas.</p>}
        </SectionCard>

        <SectionCard title="Quotes">
          {data.quotes.map((q: any) => (
            <p key={q.id} className="mb-2 text-sm">USD {q.total_estimated} (fee {q.fee_amount})</p>
          ))}
          {!data.quotes.length && <p className="text-sm text-slate-400">Sin cotización.</p>}
        </SectionCard>

        <SectionCard title="Incidents">
          {data.incidents.map((i: any) => (
            <p key={i.id} className="mb-2 text-sm">{i.type} — {i.status}</p>
          ))}
          {!data.incidents.length && <p className="text-sm text-slate-400">Sin incidentes.</p>}
        </SectionCard>
      </div>
    </div>
  );
}
