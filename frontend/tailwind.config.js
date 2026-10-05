/** @type {import('tailwindcss').Config} */
module.exports = { content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
theme: { extend: { colors: { ink: "#16202E", navy: "#1E2A44", muted: "#4A5B7A", accent: "#B98A2F", paper: "#FAF8F4", line: "#E6E1D8" },
borderRadius: { card: "12px" }, fontFamily: { sans: ["Inter", "system-ui", "sans-serif"] } } }, plugins: [] };
