"use client";
import { useState } from "react";
import { api } from "@/lib/api";
const STEPS = ["Basic details", "Professional info", "Practice areas", "Languages & location", "Verification documents", "Review & submit"];
export default function Onboarding() {
  const [s, setS] = useState(0);
  const [f, setF] = useState<any>({ full_name: "", email: "", enrollment_number: "", city: "", state: "", experience_years: 5, practice_areas: ["Property Law"], languages: ["en"], courts: ["District Court"], bio: "" });
  const [msg, setMsg] = useState("");
  const pct = Math.round(((s + 1) / STEPS.length) * 100);
  async function submit() { const j = await api("/api/lawyers/register", { method: "POST", body: JSON.stringify({ ...f, documents: [{ type: "enrollment_certificate", url: "demo://cert.pdf" }] }) }); setMsg(j.ok ? "Your profile is under review." : j.error); }
  const set = (k: string, v: any) => setF({ ...f, [k]: v });
  return (<div className="max-w-2xl mx-auto px-4 py-10"><h1 className="text-2xl font-bold text-navy">Lawyer onboarding</h1>
  <p className="text-sm text-muted">Step {s + 1} of {STEPS.length}: {STEPS[s]} · {pct}% complete</p>
  <div className="h-2 bg-white border border-line rounded-full mt-2"><div className="h-full bg-navy rounded-full" style={{ width: pct + "%" }} /></div>
  <div className="card mt-4 space-y-3">
    {s === 0 && (<><label className="label">Full name<input className="input" value={f.full_name} onChange={(e) => set("full_name", e.target.value)} /></label><label className="label">Email<input className="input" value={f.email} onChange={(e) => set("email", e.target.value)} /></label><label className="label">Phone<input className="input" value={f.phone || ""} onChange={(e) => set("phone", e.target.value)} /></label></>)}
    {s === 1 && (<><label className="label">Enrollment number<input className="input" value={f.enrollment_number} onChange={(e) => set("enrollment_number", e.target.value)} /></label><label className="label">Experience (years)<input type="number" className="input" value={f.experience_years} onChange={(e) => set("experience_years", +e.target.value)} /></label><label className="label">Bio<textarea className="input" value={f.bio} onChange={(e) => set("bio", e.target.value)} /></label></>)}
    {s === 2 && (<label className="label">Practice areas (comma separated)<input className="input" value={f.practice_areas.join(", ")} onChange={(e) => set("practice_areas", e.target.value.split(",").map((x) => x.trim()))} /></label>)}
    {s === 3 && (<><label className="label">City<input className="input" value={f.city} onChange={(e) => set("city", e.target.value)} /></label><label className="label">State<input className="input" value={f.state} onChange={(e) => set("state", e.target.value)} /></label><label className="label">Languages (comma separated codes)<input className="input" value={f.languages.join(",")} onChange={(e) => set("languages", e.target.value.split(","))} /></label></>)}
    {s === 4 && <p className="text-sm text-muted">Demo mode: an enrollment certificate placeholder will be attached. File validation + secure storage abstraction live server-side.</p>}
    {s === 5 && <p className="text-sm">Review and submit. Status will be <strong>PENDING VERIFICATION</strong> until an admin approves.</p>}
    <div className="flex gap-2">{s > 0 && <button className="btn-ghost" onClick={() => setS(s - 1)}>Back</button>}{s < 5 ? <button className="btn-primary" onClick={() => setS(s + 1)}>Continue</button> : <button className="btn-primary" onClick={submit}>Submit for review</button>}</div>
    {msg && <p className="text-sm font-semibold">{msg}</p>}
  </div></div>);
}
