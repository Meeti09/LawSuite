"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { DEMO_LAWYERS } from "@/lib/demo-lawyers";
import LawyerCard from "@/components/LawyerCard";
import { EmptyState, LoadingState } from "@/components/badges";
export default function Lawyers() {
  const [rows, setRows] = useState<any[]>([]); const [loading, setLoading] = useState(true);
  const [city, setCity] = useState(""); const [pa, setPa] = useState("");
  const [usingDemo, setUsingDemo] = useState(false);
  function filterDemo() {
    return DEMO_LAWYERS.filter((l) =>
      (!city || l.city.toLowerCase().includes(city.toLowerCase())) &&
      (!pa || l.practice_areas.some((x) => x.toLowerCase().includes(pa.toLowerCase()))));
  }
  async function load() {
    setLoading(true);
    try {
      const j = await api(`/api/lawyers?city=${encodeURIComponent(city)}&practice_area=${encodeURIComponent(pa)}`);
      if (j.ok && j.data.length > 0) { setRows(j.data); setUsingDemo(false); }
      else { setRows(filterDemo()); setUsingDemo(true); }
    } catch { setRows(filterDemo()); setUsingDemo(true); }
    setLoading(false);
  }
  useEffect(() => { load(); }, []);
  return (<div className="max-w-6xl mx-auto px-4 py-10">
    <h1 className="text-3xl font-extrabold text-navy">Find a verified lawyer</h1>
    <p className="text-muted text-sm">AI helps you understand. Lawyers help you act.</p>
    <div className="card mt-4 flex flex-wrap gap-2">
      <input className="input !w-auto" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} aria-label="City" />
      <input className="input !w-auto" placeholder="Practice area" value={pa} onChange={(e) => setPa(e.target.value)} aria-label="Practice area" />
      <button className="btn-primary !py-2" onClick={load}>Search</button>
    </div>
    <div className="grid md:grid-cols-2 gap-3 mt-5">{loading ? <LoadingState /> : rows.length === 0 ? <EmptyState t="No verified lawyers found" d="Try a different city or practice area." /> : rows.map((l) => <LawyerCard key={l.id} l={l} />)}</div>
    {usingDemo && !loading && <p className="text-xs text-muted mt-3">Showing pre-loaded verified profiles (demo). Connect the API for live data.</p>}
  </div>);
}
