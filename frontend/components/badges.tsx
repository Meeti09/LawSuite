import { BadgeCheck } from "lucide-react";
export function VerificationBadge() { return (<span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-full px-2 py-0.5"><BadgeCheck size={13} /> Verified</span>); }
export function StatusBadge({ s }: { s: string }) { return (<span className="inline-flex items-center text-xs font-semibold border border-line rounded-full px-2 py-0.5 bg-paper">{s}</span>); }
export function EmptyState({ t, d }: { t: string; d?: string }) { return (<div className="card text-center py-10"><p className="font-semibold">{t}</p>{d && <p className="text-muted text-sm mt-1">{d}</p>}</div>); }
export function LoadingState({ t = "Loading…" }: { t?: string }) { return (<div className="card" role="status" aria-live="polite"><p className="text-muted text-sm">{t}</p></div>); }
export function ErrorState({ t }: { t: string }) { return (<div className="card border-red-200" role="alert"><p className="text-sm text-red-700">{t}</p></div>); }
