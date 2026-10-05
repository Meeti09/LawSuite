export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export const WA_NUMBER = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || "919876543210";
export const WA_URL = process.env.NEXT_PUBLIC_WHATSAPP_URL || `https://wa.me/${WA_NUMBER}?text=Hi%20LawSuite%2C%20I%20need%20legal%20help`;
export async function api(path: string, opts: RequestInit = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("ls_token") : null;
  const r = await fetch(`${API}${path}`, { ...opts, headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(opts.headers || {}) } });
  const j = await r.json().catch(() => ({ ok: false, error: "Bad response" }));
  if (!r.ok && j.ok !== false) return { ok: false, error: `HTTP ${r.status}` };
  return j;
}
export const LANGUAGES = [{ code: "en", label: "English" }, { code: "hi", label: "हिन्दी" }, { code: "mr", label: "मराठी" }, { code: "gu", label: "ગુજરાતી" }, { code: "ta", label: "தமிழ்" }, { code: "te", label: "తెలుగు" }, { code: "bn", label: "বাংলা" }, { code: "kn", label: "ಕನ್ನಡ" }];
