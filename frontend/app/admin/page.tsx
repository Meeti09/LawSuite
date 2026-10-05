"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
export default function Admin() {
  const [ov, setOv] = useState<any>(null); const [lawyers, setLawyers] = useState<any[]>([]); const [msg, setMsg] = useState("");
  async function load() { const a = await api("/api/admin/overview"); if (a.ok) setOv(a.data); else setMsg(a.error || "Admin login required (admin@lawsuite.in / Admin@123)");
    const b = await api("/api/admin/lawyers"); if (b.ok) setLawyers(b.data); }
  useEffect(() => { load(); }, []);
  async function verify(id: string, action: string) { const j = await api(`/api/admin/lawyers/${id}/verify`, { method: "PATCH", body: JSON.stringify({ action, notes: "Reviewed in demo" }) }); if (j.ok) load(); }
  return (<div className="max-w-6xl mx-auto px-4 py-10">
    <p className="text-xs uppercase tracking-widest text-muted">Internal operations · demo data labelled</p>
    <h1 className="text-3xl font-extrabold text-navy">Admin overview</h1>{msg && <p className="text-sm text-red-700 mt-2">{msg}</p>}
    {ov && <div className="grid sm:grid-cols-4 gap-3 mt-4">{Object.entries(ov).filter(([k]) => k !== "note").map(([k, v]) => <div key={k} className="card"><p className="text-xs text-muted">{k.replace(/_/g, " ")}</p><p className="text-2xl font-bold">{String(v)}</p></div>)}<p className="text-xs text-muted sm:col-span-4">{ov.note}</p></div>}
    <h2 className="font-bold mt-8">Lawyer verification</h2>
    <div className="space-y-2 mt-2">{lawyers.map((l) => (<div key={l.id} className="card flex flex-wrap items-center gap-2 text-sm"><span className="font-semibold">{l.full_name}</span><span className="text-muted">{l.enrollment_number} · {l.city}</span><span className="text-xs border border-line rounded-full px-2">{l.status}</span><span className="ml-auto flex gap-2"><button className="btn-primary !py-1 !px-3 text-xs" onClick={() => verify(l.id, "APPROVE")}>Approve</button><button className="btn-ghost !py-1 !px-3 text-xs" onClick={() => verify(l.id, "REJECT")}>Reject</button></span></div>))}</div>
  </div>);
}
