import Link from "next/link";

export default function TicketsPage() {
  return <main className="shell"><header className="page-hero"><p className="eyebrow">Your tickets</p><h1>Tickets will appear<br/>here after payment.</h1><p className="muted">This local build supports inventory reservations. Customer ticket delivery is enabled once payment and account services are connected.</p></header><section className="form-card"><h2>No delivered tickets yet</h2><p className="muted">Choose an event to reserve available tickets for ten minutes.</p><Link className="button button-violet" href="/explore">Browse events</Link></section></main>;
}
