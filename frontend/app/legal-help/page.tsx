"use client";
import { useState } from "react";
import { api, LANGUAGES } from "@/lib/api";
import Link from "next/link";

export default function LegalHelp() {
  const [msg, setMsg] = useState("");
  const [lang, setLang] = useState("en");
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState<any>(null);
  const [err, setErr] = useState("");
  async function send(e?: React.FormEvent) {
    e?.preventDefault(); if (!msg.trim()) return;
    setLoading(true); setErr("");
    try { const j = await api("/api/legal-help/chat", { method: "POST", body: JSON.stringify({ message: msg, language: lang }) });
      if (!j.ok) throw new Error(j.error || "Failed"); setRes(j.data);
    } catch (e: any) { setErr(e.message); } finally { setLoading(false); }
  }
  return (<div className="max-w-3xl mx-auto px-4 py-10">
    <h1 className="text-3xl font-extrabold text-navy">Tell us what happened.</h1>
    <p className="text-muted mt-1 text-sm">Progress: Understanding your situation → Identifying legal area → Finding relevant information → Preparing your next step.</p>
    <form onSubmit={send} className="card mt-5 space-y-3">
      <label className="label" htmlFor="what">What happened?</label>
      <textarea id="what" className="input min-h-[110px]" value={msg} onChange={(e) => setMsg(e.target.value)} placeholder="Example: My employer hasn't paid my salary for three months." />
      <div className="flex flex-wrap gap-3 items-center">
        <label className="text-sm">Language <select className="input !w-auto" value={lang} onChange={(e) => setLang(e.target.value)} aria-label="Language">{LANGUAGES.map((l) => <option key={l.code} value={l.code}>{l.label}</option>)}</select></label>
        <button className="btn-primary" disabled={loading}>{loading ? "Understanding…" : "Get guidance"}</button>
      </div>
      {err && <p role="alert" className="text-sm text-red-700">{err}</p>}
    </form>
    {res && (<div className="space-y-3 mt-5">
      <div className="card"><p className="text-xs uppercase tracking-widest text-muted">Stage · {res.stage}</p><p className="mt-2 whitespace-pre-line text-[15px]">{res.reply}</p></div>
      <div className="card"><h2 className="font-bold">Legal area &amp; next steps</h2><p className="text-sm mt-1"><strong>Area:</strong> {res.brief?.category}</p>
        <ul className="text-sm mt-2 list-disc ml-5 space-y-1">{(res.brief?.next_steps || []).map((s: string) => <li key={s}>{s}</li>)}</ul>
        {res.brief?.high_risk_note && <p className="text-sm mt-2 font-semibold text-amber-800">{res.brief.high_risk_note}</p>}
        <p className="text-xs text-muted mt-2">{res.brief?.disclaimer}</p>
        <div className="flex flex-wrap gap-2 mt-3"><Link href="/documents" className="btn-ghost !py-2 text-xs">Prepare a document</Link><Link href="/lawyers" className="btn-primary !py-2 text-xs">Find a lawyer</Link></div></div>
      {res.grounding?.citations?.length > 0 && (<div className="card"><h2 className="font-bold">Sources</h2>{res.grounding.citations.map((c: any) => (<p key={c.id} className="text-sm mt-1">{c.title} — {c.act} {c.section}</p>))}</div>)}
    </div>)}
  </div>);
}
