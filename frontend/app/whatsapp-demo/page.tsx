"use client";
import { useEffect, useRef, useState } from "react";
import { MessageCircle } from "lucide-react";
import { api, WA_URL } from "@/lib/api";

type Line = { from: "you" | "bot"; text: string };

// TEMPORARY offline mock (for Vercel demo without backend).
// Mirrors backend DemoLLMProvider + state machine so a few questions get answers.
const STATES = ["START", "LANGUAGE_SELECTION", "ISSUE_DESCRIPTION", "FOLLOW_UP", "LEGAL_CLASSIFICATION", "GUIDANCE", "DOCUMENT_OPTION", "LAWYER_OPTION", "COMPLETED"];
const CATEGORY_KEYWORDS: Record<string, string[]> = {
  "Property Law": ["rent", "deposit", "landlord", "tenant", "property", "evict", "lease", "flat", "house"],
  "Employment Law": ["salary", "employer", "job", "fired", "terminat", "offer letter", "pf", "gratuity", "workplace"],
  "Consumer Law": ["refund", "consumer", "product", "defect", "warranty", "seller", "flipkart", "amazon", "shop"],
  "Family Law": ["divorce", "marriage", "custody", "maintenance", "dowry", "alimony"],
  "Criminal Law": ["fir", "police", "arrest", "theft", "fraud", "cheat", "threat"],
  "Cyber Law": ["otp", "upi", "phishing", "hack", "online fraud", "whatsapp scam"],
  "Women & Child Rights": ["harassment", "posh", "domestic violence", "pocso", "dowry"],
  "Banking & Finance": ["loan", "emi", "bank", "cheque bounce", "138"],
  "Tax Law": ["gst", "income tax", "notice", "tds"],
};
const FOLLOW_UPS: Record<string, string[]> = {
  "Property Law": ["Which state is the property located in?", "Do you have a written rental agreement?", "When did you vacate / when was rent due?"],
  "Employment Law": ["Which state do you work in?", "Do you have a written employment agreement or offer letter?", "How long has the salary been unpaid?"],
  "Consumer Law": ["What did you purchase and when?", "Do you have the bill / invoice?", "Have you contacted the seller in writing?"],
  "Family Law": ["Which city/state are you in?", "Is there a written agreement or court case already?", "Are there children involved?"],
  "Criminal Law": ["Which city/state did this happen in?", "Have you approached the police yet?", "Do you have any written evidence (messages, receipts)?"],
  "Cyber Law": ["What amount is involved, if any?", "Do you have transaction IDs / screenshots?", "Have you reported on cybercrime.gov.in or 1930?"],
};
const DISCLAIMER = "AI-generated information is for general informational purposes and is not a substitute for advice from a qualified legal professional.";
function detectCategory(text: string): string {
  const t = text.toLowerCase();
  let best = "General", score = 0;
  for (const [cat, kws] of Object.entries(CATEGORY_KEYWORDS)) {
    const s = kws.filter((k) => t.includes(k)).length;
    if (s > score) { best = cat; score = s; }
  }
  return best;
}
function nextState(current: string): string {
  const i = STATES.indexOf(current);
  return STATES[Math.min((i < 0 ? 0 : i) + 1, STATES.length - 1)];
}

export default function WhatsDemo() {
  const [phone, setPhone] = useState("919000000000");
  const [text, setText] = useState("");
  const [log, setLog] = useState<Line[]>([
    { from: "bot", text: "Hello! I'm LawSuite. Describe your legal problem in your own words." },
  ]);
  const [sending, setSending] = useState(false);
  const [stage, setStage] = useState("START");
  const [category, setCategory] = useState("");
  const [offline, setOffline] = useState(false);
  const turnsRef = useRef<string[]>([]);
  const tokenRef = useRef("");
  const boxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    boxRef.current?.scrollTo({ top: boxRef.current.scrollHeight, behavior: "smooth" });
  }, [log, sending]);

  async function send(e?: React.FormEvent) {
    e?.preventDefault();
    const message = text.trim();
    if (!message || sending) return;
    setText("");
    setSending(true);
    setLog((l) => [...l, { from: "you", text: message }]);
    // Try live backend first; fall back to temporary offline mock on Vercel.
    try {
      const j = await api("/api/whatsapp/simulate", {
        method: "POST",
        body: JSON.stringify({ phone, message }),
      });
      if (j.ok) {
        setOffline(false);
        turnsRef.current = [...turnsRef.current, message];
        setLog((l) => [...l, { from: "bot", text: j.data.reply }]);
        setStage(j.data.state || "");
        setCategory(j.data.category || "");
        setSending(false);
        return;
      }
    } catch { /* fall through to offline mock */ }
    // --- Offline mock reply (temporary) ---
    const turns = [...turnsRef.current, message];
    turnsRef.current = turns;
    const trivial = message.toLowerCase().trim().replace(/[ !.,]+$/g, "");
    if (!tokenRef.current) tokenRef.current = "mock-" + Math.random().toString(16).slice(2, 10);
    let reply: string;
    let cat = "";
    if (turns.length === 1 && ["hi", "hello", "hey", "yo", "hii", "start", "namaste", "namaskar", "sat sri akal"].includes(trivial)) {
      reply = "Hello! I'm LawSuite. Describe your legal problem in your own words.\n\nTry: My landlord isn't returning my deposit";
      setStage((s) => nextState(s === "START" ? "START" : s));
    } else {
      cat = detectCategory(turns.join(" "));
      const answered = turns.length;
      const qs = FOLLOW_UPS[cat] || ["Which state/city did this happen in?", "Do you have any documents related to this?"];
      const risk = /arrest|fir|domestic violence|dowry|evict|deadline|notice|lawsuit|court|police|custody/.test(turns.join(" ").toLowerCase());
      let out = `Based on the information provided, this looks like it may relate to **${cat}**. `;
      if (risk) out += "This situation may require professional legal assistance. Consider connecting with a qualified lawyer. ";
      if (answered < 3) {
        out += `\n\nTo help you better: ${qs[Math.min(answered - 1, qs.length - 1)]}`;
      } else {
        out += `\n\n**What we understood (preliminary):** your description has been noted.`
          + `\n**Possible next steps:** 1) Preserve records & messages 2) Review any written agreement 3) Send a written request 4) Consider professional legal advice. ${DISCLAIMER}`
          + `\n\nContinue on web with this token: /legal-help?handoff=${tokenRef.current}`;
      }
      if (/lawyer/.test(message.toLowerCase())) {
        out += `\n\nI can connect you with a verified lawyer — see /lawyers or continue with token /legal-help?handoff=${tokenRef.current}`;
      }
      reply = out;
      setStage((s) => nextState(s));
      setCategory(cat);
    }
    setOffline(true);
    // Simulate typing delay so it feels like a chat
    await new Promise((r) => setTimeout(r, 500));
    setLog((l) => [...l, { from: "bot", text: reply }]);
    setSending(false);
  }

  function reset() {
    setPhone("919000000000");
    turnsRef.current = [];
    tokenRef.current = "";
    setOffline(false);
    setLog([{ from: "bot", text: "Hello! I'm LawSuite. Describe your legal problem in your own words." }]);
    setStage("START");
    setCategory("");
  }

  return (<div className="max-w-2xl mx-auto px-4 py-10">
    <p className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-[#128C4B]">
      <span className="w-7 h-7 rounded-full bg-[#25D366] text-white inline-flex items-center justify-center" aria-hidden><MessageCircle size={15} strokeWidth={2.5} /></span>
      WhatsApp Assistant · Mock demo
    </p>
    <h1 className="text-3xl font-extrabold text-navy mt-2">WhatsApp mock conversation</h1>
    <p className="text-sm text-muted">Same state machine as production (START → … → COMPLETED). <a className="underline" href={WA_URL} target="_blank" rel="noreferrer">Open real WhatsApp →</a></p>
    {offline && <p className="text-xs mt-2 inline-block bg-amber-100 border border-amber-300 rounded px-2 py-1">Temporary offline demo — answering without backend</p>}
    <div className="flex flex-wrap gap-2 mt-3">
      {["My landlord isn't returning my deposit", "My salary hasn't been paid for 2 months", "I got cheated in an online UPI fraud"].map((q) => (
        <button key={q} type="button" className="btn-ghost !py-1 text-xs" disabled={sending} onClick={() => { setText(q); }}>{q}</button>
      ))}
    </div>
    <div className="card mt-4 flex flex-wrap items-end gap-2">
      <label className="label !mb-0 flex-1 min-w-[200px]">Phone<input className="input mt-1" value={phone} onChange={(e) => setPhone(e.target.value)} /></label>
      <button type="button" className="btn-ghost !py-2 text-xs" onClick={reset}>Restart chat</button>
    </div>
    {(stage !== "START" || category) && (
      <p className="text-xs text-muted mt-3" aria-live="polite">
        Stage: <strong>{stage.replace(/_/g, " ")}</strong>{category && <> · Area: <strong>{category}</strong></>}
      </p>
    )}
    <div ref={boxRef} className="card mt-2 space-y-2 max-h-[420px] overflow-y-auto !bg-[#EFEBE3]" aria-live="polite">
      {log.map((m, i) => (
        <div key={i} className={m.from === "you" ? "flex justify-end" : "flex justify-start"}>
          <p className={`max-w-[85%] rounded-xl px-3 py-2 text-sm whitespace-pre-line ${m.from === "you" ? "bg-[#D9FDD3] text-ink" : "bg-white text-ink border border-line"}`}>{m.text}</p>
        </div>
      ))}
      {sending && <p className="text-xs text-muted">LawSuite is typing…</p>}
    </div>
    <form onSubmit={send} className="flex gap-2 mt-3">
      <input className="input" value={text} onChange={(e) => setText(e.target.value)} placeholder="Try: My landlord isn't returning my deposit" aria-label="Message" disabled={sending} />
      <button className="btn-primary shrink-0" disabled={sending || !text.trim()}>{sending ? "…" : "Send"}</button>
    </form>
  </div>);
}
