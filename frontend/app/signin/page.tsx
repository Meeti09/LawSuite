"use client";
import { useState } from "react";
import { api } from "@/lib/api";
export default function SignIn() {
  const [email, setEmail] = useState("user@lawsuite.in"); const [pw, setPw] = useState("User@123"); const [m, setM] = useState("");
  async function go(e: React.FormEvent, admin = false) { e.preventDefault();
    const j = await api(admin ? "/api/auth/admin-login" : "/api/auth/login", { method: "POST", body: JSON.stringify({ email, password: pw }) });
    if (j.ok) { localStorage.setItem("ls_token", j.data.token); setM(`Signed in as ${j.data.name} (${j.data.role})`); } else setM(j.error || "Failed"); }
  return (<div className="max-w-md mx-auto px-4 py-10"><h1 className="text-2xl font-bold text-navy">Sign in</h1>
  <form className="card mt-4 space-y-3" onSubmit={(e) => go(e)}><label className="label">Email<input className="input" value={email} onChange={(e) => setEmail(e.target.value)} /></label>
  <label className="label">Password<input type="password" className="input" value={pw} onChange={(e) => setPw(e.target.value)} /></label>
  <div className="flex gap-2"><button className="btn-primary">Sign In</button><button type="button" className="btn-ghost" onClick={(e: any) => go(e, true)}>Admin login</button></div>{m && <p className="text-sm">{m}</p>}
  <p className="text-xs text-muted">Demo: user@lawsuite.in / User@123 · admin@lawsuite.in / Admin@123</p></form></div>);
}
