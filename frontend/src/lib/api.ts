const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api';
const ORG_ID = process.env.NEXT_PUBLIC_ORG_ID ?? '1';

export async function apiGet(path: string) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'x-org-id': ORG_ID },
    cache: 'no-store',
  });
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json();
}
