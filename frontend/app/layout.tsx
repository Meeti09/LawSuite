import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
export const metadata: Metadata = { title: "LawSuite — Legal help, made understandable", description: "Understand your situation, prepare what you need, and connect with a verified lawyer when you need one.", openGraph: { title: "LawSuite", description: "Legal help, made understandable.", type: "website" } };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body className="bg-paper text-ink font-sans antialiased"><a href="#main" className="sr-only focus:not-sr-only">Skip to content</a><Navbar /><main id="main" className="min-h-[70vh]">{children}</main><Footer /></body></html>);
}
