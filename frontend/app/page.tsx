import Link from "next/link";
import { MessageCircle, Scale, FileText, ArrowRight } from "lucide-react";
import { WA_URL } from "@/lib/api";
import { QRCodeSVG } from "qrcode.react";

const ISSUES = ["I received a legal notice", "My employer has an issue with me", "My landlord isn't returning my deposit", "I have a consumer complaint", "I have a family dispute", "I need a legal document", "I need to find a lawyer", "I don't know where to start"];

export default function Home() {
  return (<div>
    <section className="max-w-6xl mx-auto px-4 pt-14 pb-10 grid lg:grid-cols-2 gap-10 items-center">
      <div>
        <p className="text-xs font-semibold tracking-widest text-accent uppercase">LawSuite · India</p>
        <h1 className="text-4xl md:text-5xl font-extrabold text-navy mt-3 leading-tight">Legal help,<br />made understandable.</h1>
        <p className="text-muted mt-4 text-lg">Understand your situation, prepare what you need, and connect with a verified lawyer when you need one.</p>
        <div className="flex flex-wrap gap-3 mt-6">
          <Link href="/legal-help" className="btn-primary">Describe My Legal Problem <ArrowRight size={16} /></Link>
          <a href={WA_URL} target="_blank" rel="noreferrer" className="btn-ghost"><MessageCircle size={16} /> Talk on WhatsApp</a>
          <Link href="/lawyers" className="btn-ghost">Find a Lawyer</Link>
        </div>
        <p className="text-xs text-muted mt-3">Available in multiple Indian languages. One problem. One clear next step.</p>
      </div>
      <div className="card" aria-label="How LawSuite works">
        <p className="text-xs font-semibold uppercase tracking-widest text-muted">Start anywhere</p>
        <ol className="mt-3 space-y-0 text-sm">
          {[["Your Problem", "Describe it in simple words — website or WhatsApp."], ["LawSuite understands", "Guided questions, legal area, simple explanation."], ["Your Next Step", "Checklist, document draft, or a verified lawyer."]].map(([t, d], i) => (
            <li key={t} className="flex gap-3 py-3 border-b border-line last:border-0"><span className="w-7 h-7 rounded-full bg-navy text-white text-xs flex items-center justify-center shrink-0">{i + 1}</span><span><strong>{t}</strong><br /><span className="text-muted">{d}</span></span></li>))}
        </ol>
        <div className="flex gap-4 mt-2 text-xs text-muted"><span className="inline-flex items-center gap-1"><Scale size={13} /> AI + Research</span><span className="inline-flex items-center gap-1"><MessageCircle size={13} /> WhatsApp</span><span className="inline-flex items-center gap-1"><FileText size={13} /> Lawyers</span></div>
      </div>
    </section>
    <section className="max-w-6xl mx-auto px-4 py-8" aria-label="Quick legal help">
      <h2 className="text-2xl font-bold text-navy">What do you need help with?</h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3 mt-4">{ISSUES.map((t) => (<Link key={t} href={`/legal-help?q=${encodeURIComponent(t)}`} className="card hover:border-navy text-sm font-medium">{t}</Link>))}</div>
    </section>
    <section className="max-w-6xl mx-auto px-4 py-8" aria-label="How it works">
      <h2 className="text-2xl font-bold text-navy">How it works</h2>
      <div className="grid md:grid-cols-4 gap-3 mt-4">{[["01", "Tell us what happened.", "Simple words, any of 8 languages."], ["02", "Understand your situation.", "Legal area explained plainly."], ["03", "Prepare your next step.", "Checklist or document draft."], ["04", "Connect with a lawyer if needed.", "Verified profiles, AI case brief."]].map(([n, t, d]) => (<div key={n} className="card"><p className="text-accent font-bold text-sm">{n}</p><p className="font-semibold mt-1">{t}</p><p className="text-sm text-muted">{d}</p></div>))}</div>
      <Link href="/how-it-works" className="text-sm font-semibold text-navy mt-3 inline-block">Learn more →</Link>
    </section>
    <section className="bg-white border-y border-line mt-4" aria-label="WhatsApp">
      <div className="max-w-6xl mx-auto px-4 py-10 grid md:grid-cols-2 gap-8 items-center">
        <div>
        <p className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-[#128C4B]"><span className="w-7 h-7 rounded-full bg-[#25D366] text-white inline-flex items-center justify-center" aria-hidden><MessageCircle size={15} strokeWidth={2.5} /></span> WhatsApp Assistant</p>
        <h2 className="text-2xl font-bold text-navy mt-2">Legal guidance is now a WhatsApp away.</h2>
        <p className="text-muted mt-2">No app to download. No complicated forms. Just send a message.</p>
        <ul className="text-sm mt-3 space-y-1 text-muted"><li>· Multilingual guided conversations</li><li>· Legal issue classification</li><li>· Document assistance &amp; lawyer handoff</li></ul>
        <div className="flex gap-3 mt-4"><a href={WA_URL} target="_blank" rel="noreferrer" className="btn-primary !bg-[#128C4B] hover:!bg-[#0E6F3B]"><MessageCircle size={16} /> Start on WhatsApp</a><Link href="/whatsapp-demo" className="btn-ghost">Try mock demo</Link></div></div>
        <div className="card !border-[#25D366]/50 flex items-center gap-5"><span className="bg-[#EAFBF1] rounded-xl p-2"><QRCodeSVG value={WA_URL} size={140} aria-label="WhatsApp QR code" /></span><div className="text-sm"><p className="font-semibold inline-flex items-center gap-1.5"><span className="w-5 h-5 rounded-full bg-[#25D366] text-white inline-flex items-center justify-center" aria-hidden><MessageCircle size={12} strokeWidth={2.5} /></span> Scan to chat</p><p className="text-muted break-all">{process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || "919876543210"}</p><p className="text-xs text-muted mt-1">Powered by wa.me deep link until Cloud API is configured.</p></div></div>
      </div>
    </section>
  </div>);
}
