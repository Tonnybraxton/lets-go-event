import Link from "next/link";

export default function AccountPage() {
  return <main className="shell"><header className="page-hero"><p className="eyebrow">Customer account</p><h1>Your event plans,<br/>in one place.</h1><p className="muted">Sign-in and saved-profile management are not enabled in this local build. Ticket reservations are still protected by the event inventory service.</p></header><section className="form-card"><h2>Account access is coming soon</h2><p className="muted">For now, reserve tickets from an event page. Payment and ticket delivery will be available when the customer-account service is connected.</p><Link className="button button-violet" href="/explore">Explore events</Link></section></main>;
}
