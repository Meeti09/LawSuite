"use client";
import Link from "next/link";
import { useState } from "react";
import { Menu, X, MessageCircle } from "lucide-react";
import { WA_URL } from "@/lib/api";
const LINKS = [["Home", "/"], ["How It Works", "/how-it-works"], ["Legal Help", "/legal-help"], ["Legal Research", "/legal-research"], ["Documents", "/documents"], ["Find a Lawyer", "/lawyers"], ["For Lawyers", "/for-lawyers"]];
export default function Navbar() {
  const [open, setOpen] = useState(false);
  return (<header className="sticky top-0 z-40 bg-paper/95 backdrop-blur border-b border-line">
    <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <Link href="/" className="font-extrabold tracking-wide text-navy text-lg" aria-label="LawSuite home">LAW&nbsp;SUITE</Link>
      <nav className="hidden lg:flex gap-5 text-sm" aria-label="Primary">{LINKS.map(([l, h]) => <Link key={h} href={h} className="text-muted hover:text-ink">{l}</Link>)}</nav>
      <div className="hidden lg:flex gap-2">
        <a href={WA_URL} target="_blank" rel="noreferrer" className="btn-ghost !py-2"><MessageCircle size={16} /> Talk on WhatsApp</a>
        <Link href="/signin" className="btn-primary !py-2">Sign In</Link>
      </div>
      <button className="lg:hidden p-3" aria-label="Menu" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? <X /> : <Menu />}</button>
    </div>
    {open && <nav className="lg:hidden border-t border-line px-4 py-3 flex flex-col gap-1" aria-label="Mobile">{LINKS.map(([l, h]) => <Link key={h} href={h} className="py-3 border-b border-line last:border-0" onClick={() => setOpen(false)}>{l}</Link>)}<a href={WA_URL} className="btn-ghost mt-2">Talk on WhatsApp</a><Link href="/signin" className="btn-primary mt-2">Sign In</Link></nav>}
  </header>);
}
