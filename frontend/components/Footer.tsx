import Link from "next/link";
export default function Footer() {
  return (<footer className="border-t border-line mt-16 bg-white"><div className="max-w-6xl mx-auto px-4 py-10 grid gap-8 md:grid-cols-4 text-sm">
    <div><p className="font-extrabold text-navy">LAW SUITE</p><p className="text-muted mt-2">Legal help, made understandable.<br />Understand. Prepare. Connect.</p></div>
    <div><p className="font-semibold mb-2">Citizens</p><div className="flex flex-col gap-1 text-muted"><Link href="/legal-help">Describe my problem</Link><Link href="/legal-research">Legal research</Link><Link href="/documents">Documents</Link><Link href="/lawyers">Find a lawyer</Link></div></div>
    <div><p className="font-semibold mb-2">Ecosystem</p><div className="flex flex-col gap-1 text-muted"><Link href="/for-lawyers">For lawyers</Link><Link href="/lawyer/onboarding">Lawyer onboarding</Link><Link href="/admin">Admin</Link><Link href="/matters">My matters</Link></div></div>
    <div><p className="font-semibold mb-2">Trust</p><p className="text-muted">AI-generated information is for general informational purposes and is not a substitute for advice from a qualified legal professional.</p></div>
  </div></footer>);
}
