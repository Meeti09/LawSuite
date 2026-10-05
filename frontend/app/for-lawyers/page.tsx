import Link from "next/link";
export default function ForLawyers() {
  return (<div className="max-w-3xl mx-auto px-4 py-10"><h1 className="text-3xl font-extrabold text-navy">For lawyers</h1>
  <p className="text-muted mt-2">AI helps citizens understand. You help them act — with a verified profile and AI-generated preliminary briefs.</p>
  <div className="card mt-4 text-sm space-y-1"><p>· Register with Bar Council details</p><p>· Manual verification by LawSuite ops</p><p>· Receive structured consultation requests</p><p>· Payment-ready architecture (no charges in demo)</p></div>
  <div className="flex gap-2 mt-4"><Link href="/lawyer/onboarding" className="btn-primary">Register as a lawyer</Link><Link href="/lawyer/dashboard" className="btn-ghost">Lawyer dashboard</Link></div></div>);
}
