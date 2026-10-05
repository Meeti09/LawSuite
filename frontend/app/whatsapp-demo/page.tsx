"use client";
import { useEffect, useRef, useState } from "react";
import { MessageCircle } from "lucide-react";
import { api, WA_URL } from "@/lib/api";

type Line = { from: "you" | "bot"; text: string };

export default function WhatsDemo() {
  const [phone, setPhone] = useState("919000000000");
  const [text, setText] = useState("");
  const [log, setLog] = useState<Line[]>([
    { from: "bot", text: "Hello! I'm LawSuite. Describe your legal problem in your own words." },
  ]);
  const [sending, setSending] = useState(false);
  const [stage, setStage] = useState("START");
  const [category, setCategory] = useState("");
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
    try {
      const j = await api("/api/whatsapp/simulate", {
        method: "POST",
        body: JSON.stringify({ phone, message }),
      });
      if (j.ok) {
        setLog((l) => [...l, { from: "bot", text: j.data.reply }]);
        setStage(j.data.state || "");
        setCategory(j.data.category || "");
      } else {
        setLog((l) => [...l, { from: "bot", text: "Sorry — " + (j.error || "something went wrong.") }]);
      }
    } catch {
      setLog((l) => [...l, { from: "bot", text: "Sorry — I couldn't reach the server. Make sure the backend is running on port 8000." }]);
    } finally {
      setSending(false);
    }
  }

  function reset() {
    setPhone("919000000000");
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
