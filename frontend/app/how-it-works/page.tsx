export default function HowItWorks() {
  return (<div className="max-w-3xl mx-auto px-4 py-10"><h1 className="text-3xl font-extrabold text-navy">How it works</h1>
  <div className="space-y-3 mt-4">{[["01 — Tell us what happened.", "Use simple words on the website or WhatsApp, in your language."], ["02 — Understand your situation.", "LawSuite identifies the legal area and explains it plainly, with sources."], ["03 — Prepare your next step.", "Checklists and document drafts, marked for professional review."], ["04 — Connect with a lawyer if needed.", "Verified lawyers receive an AI-generated preliminary brief."]].map(([t, d]) => (<div key={t} className="card"><p className="font-bold">{t}</p><p className="text-sm text-muted">{d}</p></div>))}</div></div>);
}
