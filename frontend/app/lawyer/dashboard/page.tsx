export default function LawyerDash() {
  return (<div className="max-w-6xl mx-auto px-4 py-10"><h1 className="text-2xl font-bold text-navy">Lawyer dashboard</h1>
  <div className="grid md:grid-cols-[200px_1fr] gap-4 mt-4"><aside className="card text-sm space-y-2 h-fit"><p className="font-bold">Workspace</p>{["Dashboard", "Consultation Requests", "My Profile", "Availability", "Documents", "Messages", "Earnings", "Settings"].map((x) => <p key={x} className="text-muted">{x}</p>)}</aside>
  <div className="space-y-3"><div className="grid sm:grid-cols-4 gap-3">{[["Pending Requests", "3"], ["Upcoming", "2"], ["Active Clients", "5"], ["Completed", "12"]].map(([k, v]) => <div key={k} className="card"><p className="text-xs text-muted">{k}</p><p className="text-2xl font-bold">{v}</p></div>)}</div>
  <div className="card text-sm"><p className="font-bold">Consultation requests (demo)</p><p className="text-muted">View / Accept / Reject / Message actions are wired to POST /api/lawyers/request + admin audit in production.</p></div></div></div></div>);
}
