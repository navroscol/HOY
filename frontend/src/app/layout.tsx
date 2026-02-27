import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <main className="mx-auto min-h-screen max-w-6xl p-6">
          <header className="mb-6 flex items-end justify-between">
            <div>
              <h1 className="text-2xl font-bold">Digital Freight Desk</h1>
              <p className="text-sm text-slate-400">Control Tower — Aéreo y Marítimo</p>
            </div>
            <nav className="flex gap-4 text-sm text-slate-300">
              <a href="/">Dashboard</a>
              <a href="/shipments">Shipments</a>
              <a href="/ops">Ops</a>
            </nav>
          </header>
          {children}
        </main>
      </body>
    </html>
  );
}
