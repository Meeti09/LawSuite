"use client";
import Link from "next/link";
import { VerificationBadge } from "./badges";
export default function LawyerCard({ l }: { l: any }) {
  return (<article className="card flex gap-4">
    <div className="w-14 h-14 rounded-full bg-navy text-white flex items-center justify-center font-bold shrink-0" aria-hidden>{(l.full_name || "L")[0]}</div>
    <div className="flex-1"><div className="flex items-center gap-2 flex-wrap"><h3 className="font-semibold">{l.full_name}</h3><VerificationBadge /></div>
    <p className="text-xs text-muted mt-0.5">{(l.practice_areas || []).join(" · ")} · {l.experience_years}y · {l.city}</p>
    <p className="text-sm text-muted mt-1 line-clamp-2">{l.bio}</p>
    <div className="flex gap-2 mt-3"><Link href={`/lawyers/${l.slug}`} className="btn-ghost !py-2 !px-4 text-xs">View Profile</Link>
    <Link href={`/lawyers/${l.slug}#consult`} className="btn-primary !py-2 !px-4 text-xs">Request Consultation</Link></div></div>
  </article>);
}
