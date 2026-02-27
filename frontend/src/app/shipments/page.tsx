import { SectionCard } from '@/components/SectionCard';
import { apiGet } from '@/lib/api';

export default async function ShipmentsPage() {
  const shipments = await apiGet('/shipments');

  return (
    <SectionCard title="Shipments Board">
      <div className="grid gap-3">
        {shipments.map((s: any) => (
          <a key={s.id} href={`/shipments/${s.id}`} className="rounded border border-slate-700 p-3 hover:border-cyan-400">
            <p className="font-semibold">#{s.id} {s.origin} → {s.destination}</p>
            <p className="text-sm text-slate-400">
              {s.mode} • {s.vertical} • {s.status} • Riesgo {s.risk_score}
            </p>
          </a>
        ))}
      </div>
    </SectionCard>
  );
}
