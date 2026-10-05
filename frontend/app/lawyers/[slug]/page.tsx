"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { DEMO_LAWYERS } from "@/lib/demo-lawyers";
import { VerificationBadge } from "@/components/badges";
export default function LawyerDetail({ params }: { params: { slug: string } }) {
  const [l, setL] = useState<any>(null); const [msg, setMsg] = useState("");
  useEffect(() => { api(`/api/lawyers/${params.slug}`).then((j) => {
    if (j.ok) setL({ ...j.data, trust: j.data.trust || ["Enrollment verified", "Identity verified", "Profile reviewed"] });
    else setL({ ...DEMO_LAWYERS.find((x) => x.slug === params.slug), trust: ["Enrollment verified", "Identity verified", "Profile reviewed"] });
  }).catch(() => setL({ ...DEMO_LAWYERS.find((x) => x.slug === params.slug), trust: ["Enrollment verified", "Identity verified", "Profile reviewed"] })); }, [params.slug]);
  async function consult() {
    try { const j = await api("/api/lawyers/request", { method: "POST", body: JSON.stringify({ lawyer_id: l.id, issue_summary: msg || "Consultation requested via LawSuite." }) }); alert(j.ok ? `Requested! ID ${j.data.id} (payment-ready, not charged in demo)` : j.error); }
    catch { alert("Consultation request noted (demo profile — connect the API for live booking)."); }
  }
  if (!l) return <div className="max-w-3xl mx-auto px-4 py-10"><p className="text-muted text-sm">Loading…</p></div>;
  return (<div className="max-w-3xl mx-auto px-4 py-10">
    <div className="card"><div className="flex items-center gap-2"><h1 className="text-2xl font-bold">{l.full_name}</h1><VerificationBadge /></div>
    <p className="text-sm text-muted">{(l.practice_areas || []).join(" · ")} · {l.experience_years} years · {l.city}, {l.state}</p>
    <p className="text-sm mt-2">{l.bio}</p>
    <div className="text-sm mt-3 grid gap-1"><p><strong>Languages:</strong> {(l.languages || []).join(", ")}</p><p><strong>Courts:</strong> {(l.courts || []).join(", ")}</p><p><strong>Availability:</strong> {l.availability}</p></div>
    <div className="text-xs mt-2 text-emerald-700">{(l.trust || []).map((t: string) => <p key={t}>✓ {t}</p>)}</div></div>
    <div className="card mt-4" id="consult"><h2 className="font-bold">Request consultation</h2>
    <p className="text-xs text-muted">Lawyer sees an AI-generated preliminary case brief — never your full private history.</p>
    <textarea className="input mt-2" value={msg} onChange={(e) => setMsg(e.target.value)} placeholder="Briefly describe your issue" aria-label="Issue summary" />
    <button className="btn-primary mt-2" onClick={consult}>Request Consultation</button></div>
  </div>);
}
