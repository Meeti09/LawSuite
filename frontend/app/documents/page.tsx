"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
export default function Documents() {
  const [types, setTypes] = useState<any[]>([]); const [t, setT] = useState("legal_notice");
  const [fields, setFields] = useState<Record<string, string>>({}); const [out, setOut] = useState<any>(null);
  useEffect(() => { api("/api/documents/types").then((j) => j.ok && setTypes(j.data)); }, []);
  const cur = types.find((x) => x.key === t);
  async function gen() { const j = await api("/api/documents/generate", { method: "POST", body: JSON.stringify({ doc_type: t, fields }) }); if (j.ok) setOut(j.data); }
  return (<div className="max-w-3xl mx-auto px-4 py-10">
    <h1 className="text-3xl font-extrabold text-navy">Document assistant</h1>
    <p className="text-muted text-sm">Choose → answer guided questions → review → download.</p>
    <div className="card mt-4 space-y-3">
      <label className="label">Choose document<select className="input" value={t} onChange={(e) => setT(e.target.value)}>{types.map((x) => <option key={x.key} value={x.key}>{x.title}</option>)}</select></label>
      {(cur?.fields || []).map((f: string) => (<div key={f}><label className="label" htmlFor={f}>{f.replace(/_/g, " ")}</label><input id={f} className="input" value={fields[f] || ""} onChange={(e) => setFields({ ...fields, [f]: e.target.value })} /></div>))}
      <button className="btn-primary" onClick={gen}>Generate draft</button>
    </div>
    {out && <div className="card mt-4"><h2 className="font-bold">{out.title}</h2><pre className="whitespace-pre-wrap text-sm mt-2">{out.content}</pre><p className="text-xs text-muted mt-2">{out.disclaimer}</p><button className="btn-ghost mt-2 !py-2 text-xs" onClick={() => window.print()}>Download / Print (PDF)</button></div>}
  </div>);
}
