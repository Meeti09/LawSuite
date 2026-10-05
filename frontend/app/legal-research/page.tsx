"use client";
import { useState } from "react";
import { api } from "@/lib/api";
export default function Research() {
  const [q, setQ] = useState(""); const [r, setR] = useState<any>(null); const [loading, setLoading] = useState(false);
  async function go(e: React.FormEvent) { e.preventDefault(); setLoading(true);
    const j = await api("/api/legal-research/search", { method: "POST", body: JSON.stringify({ query: q }) });
    setR(j.data); setLoading(false); }
  return (<div className="max-w-3xl mx-auto px-4 py-10">
    <h1 className="text-3xl font-extrabold text-navy">Legal research</h1>
    <p className="text-muted text-sm">Grounded answers with citations. We never fabricate sources.</p>
    <form onSubmit={go} className="card mt-4 flex gap-2"><input className="input" value={q} onChange={(e) => setQ(e.target.value)} placeholder="What are you looking for? e.g. cheque bounce notice" aria-label="Search" /><button className="btn-primary" disabled={loading}>{loading ? "…" : "Search"}</button></form>
    {r && <div className="card mt-4"><p className="whitespace-pre-line text-[15px]">{r.answer}</p>{(r.citations || []).map((c: any) => (<div key={c.id} className="border-t border-line mt-2 pt-2 text-sm"><strong>{c.title}</strong><br /><span className="text-muted">{c.act} · {c.section} · {c.source_name}</span></div>))}</div>}
  </div>);
}
