import { SectionCard } from '@/components/SectionCard';
import { apiGet } from '@/lib/api';

export default async function OpsTodayPage() {
  const data = await apiGet('/ops/today');

  return (
    <div className="space-y-4">
      <SectionCard title="Atenciones hoy — Embarques en riesgo">
        {data.at_risk.map((s: any) => (
          <p key={s.id} className="mb-2 text-sm">#{s.id} {s.origin} → {s.destination} ({s.risk_score})</p>
        ))}
        {!data.at_risk.length && <p className="text-sm text-slate-400">Sin embarques críticos.</p>}
      </SectionCard>

      <SectionCard title="Tareas abiertas">
        {data.open_tasks.map((t: any) => (
          <p key={t.id} className="mb-2 text-sm">• {t.title} — {t.owner} ({t.status})</p>
        ))}
        {!data.open_tasks.length && <p className="text-sm text-slate-400">Sin tareas abiertas.</p>}
      </SectionCard>

      <SectionCard title="Incidentes abiertos">
        {data.open_incidents.map((i: any) => (
          <p key={i.id} className="mb-2 text-sm">• {i.type} — {i.summary}</p>
        ))}
        {!data.open_incidents.length && <p className="text-sm text-slate-400">Sin incidentes abiertos.</p>}
      </SectionCard>
    </div>
  );
}
