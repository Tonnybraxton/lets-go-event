import Link from "next/link";

export function BrandMark({ footer = false }: { footer?: boolean }) {
  return <Link href="/" className={`brand-mark${footer ? " brand-mark-footer" : ""}`} aria-label="Let's Go Event home">
    <svg className="brand-symbol" viewBox="0 0 44 44" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="letsgo-brand-gradient" x1="4" y1="3" x2="40" y2="42" gradientUnits="userSpaceOnUse">
          <stop stopColor="#a78bfa"/>
          <stop offset=".55" stopColor="#7c3aed"/>
          <stop offset="1" stopColor="#db2777"/>
        </linearGradient>
        <linearGradient id="letsgo-ticket-gradient" x1="11" y1="10" x2="33" y2="34" gradientUnits="userSpaceOnUse">
          <stop stopColor="#fff"/>
          <stop offset="1" stopColor="#e9ddff"/>
        </linearGradient>
      </defs>
      <rect x="1" y="1" width="42" height="42" rx="14" fill="url(#letsgo-brand-gradient)"/>
      <path d="M12 12.5h20a2 2 0 0 1 2 2v4.1a3.7 3.7 0 0 0 0 7.1v4.3a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2v-4.3a3.7 3.7 0 0 0 0-7.1v-4.1a2 2 0 0 1 2-2Z" fill="url(#letsgo-ticket-gradient)"/>
      <path d="M25 14.5v15" stroke="#9871ed" strokeWidth="1.5" strokeDasharray="2 2.5"/>
      <path d="m17.5 18.4.95 2.2 2.4.2-1.83 1.55.55 2.34-2.07-1.25-2.06 1.25.55-2.34-1.83-1.55 2.4-.2.94-2.2Z" fill="#7240db"/>
      <circle cx="28.8" cy="22.2" r="2.15" fill="#7240db"/>
      <path d="M28.8 24.8c-.95 1.25-1.6 2.3-1.6 3.15a1.6 1.6 0 0 0 3.2 0c0-.85-.65-1.9-1.6-3.15Z" fill="#7240db"/>
    </svg>
    <span className="brand-wordmark">LET&apos;S <span>GO</span></span>
    <span className="brand-footer-label">EVENTS</span>
  </Link>;
}

