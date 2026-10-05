"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
export default function Matters() {
  const [rows, setRows] = useState<any[]>([]);
  useEffect(() => { api("/api/matters").then((j) => j.ok && setRows(j.data)); }, []);
  return (<div className="max-w-3xl mx-auto px-4 py-10"><h1 className="text-3xl font-extrabold text-navy">My matters</h1>
  <div className="space-y-2 mt-4">{rows.map((m) => (<div key={m.id} className="card text-sm"><p className="font-semibold">{m.title}</p><p className="text-muted">{m.category} · {m.status} · {m.created_at}</p></div>))}{rows.length === 0 && <p className="text-sm text-muted">No matters yet — describe a problem to create one.</p>}</div></div>);
}
