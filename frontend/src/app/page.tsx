import { KpiCard } from '@/components/KpiCard';
import { SectionCard } from '@/components/SectionCard';
import { apiGet } from '@/lib/api';

export default async function HomePage() {
  const dashboard = await apiGet('/dashboard/executive');

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <KpiCard title="Embarques activos" value={dashboard.active_shipments} />
        <KpiCard title="On-time" value={dashboard.on_time} />
        <KpiCard title="Retrasados" value={dashboard.delayed} />
        <KpiCard title="Riesgo promedio" value={`${dashboard.avg_risk}/100`} />
      </div>

      <SectionCard title="Top embarques en riesgo">
        <div className="space-y-2 text-sm">
          {(dashboard.high_risk_shipments || []).map((s: any) => (
            <div key={s.id} className="rounded border border-slate-700 p-3">
              <p className="font-semibold">#{s.id} {s.origin} → {s.destination}</p>
              <p className="text-slate-400">{s.mode} • {s.vertical} • Riesgo {s.risk_score}</p>
            </div>
          ))}
          {!dashboard.high_risk_shipments?.length && <p className="text-slate-400">Sin embarques de alto riesgo.</p>}
        </div>
      </SectionCard>
    </div>
  );
}
