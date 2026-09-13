"use client";

import type { TicketTier } from "@letsgo/types";
import { LockKeyhole } from "lucide-react";
import { useMemo, useState } from "react";
import { formatMoney } from "@/lib/data";

export function TicketPanel({ tiers, externalUrl, priceAvailable = true }: { tiers: TicketTier[]; externalUrl?: string | undefined; priceAvailable?: boolean | undefined }) {
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);
  const total = useMemo(() => tiers.reduce((sum, tier) => sum + tier.priceMinor * (quantities[tier.id] ?? 0), 0), [quantities, tiers]);

  if (externalUrl || priceAvailable === false) return <aside className="ticket-panel"><span className="eyebrow">External listing</span><h2>Tickets at the source</h2><p className="muted">Availability and checkout are managed by the original event source.</p>{externalUrl ? <a className="button button-violet" style={{width:"100%",display:"block",textAlign:"center"}} href={externalUrl} target="_blank" rel="noopener noreferrer">View original listing</a> : <p className="trust">Source ticket details are coming soon.</p>}</aside>;

  async function reserveTickets() {
    setSaving(true); setMessage("");
    try {
      const response = await fetch("/api/orders", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({items: tiers.filter((tier) => quantities[tier.id]).map((tier) => ({tierId:tier.id, quantity:quantities[tier.id]}))}) });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "Could not reserve tickets.");
      setMessage(`${payload.reference}: reserved until ${new Date(payload.expiresAt).toLocaleTimeString("en-KE", {hour:"numeric", minute:"2-digit"})}. Payment will be enabled once your M-Pesa details are added.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not reserve tickets."); }
    finally { setSaving(false); }
  }

  return <aside className="ticket-panel"><span className="eyebrow">Verified inventory</span><h2>Choose tickets</h2><p className="muted" style={{fontSize:13}}>Your selection is held for 10 minutes when you reserve it.</p>
    {tiers.map((tier) => { const quantity = quantities[tier.id] ?? 0; const maximum = Math.min(6, tier.remaining); return <div className="ticket-option" key={tier.id}><div><strong>{tier.name}</strong><small className="muted" style={{display:"block",marginTop:4}}>{tier.description} · {tier.remaining} left</small><span style={{display:"block",marginTop:8}}>{formatMoney(tier.priceMinor,tier.currency)}</span></div><div style={{display:"flex",alignItems:"center",gap:6}}><button type="button" aria-label={`Decrease ${tier.name} quantity`} disabled={quantity === 0} onClick={() => setQuantities({...quantities,[tier.id]:quantity - 1})}>−</button><input aria-label={`${tier.name} quantity`} type="number" min="0" max={maximum} value={quantity} onChange={(event) => setQuantities({...quantities,[tier.id]:Math.max(0,Math.min(maximum,Number(event.target.value) || 0))})}/><button type="button" aria-label={`Increase ${tier.name} quantity`} disabled={quantity === maximum} onClick={() => setQuantities({...quantities,[tier.id]:quantity + 1})}>+</button></div></div>; })}
    <div className="ticket-total"><span>Total</span><strong>{formatMoney(total,tiers[0]?.currency)}</strong></div><button className="button button-violet" style={{width:"100%"}} disabled={total === 0 || saving} onClick={reserveTickets}>{saving ? "Reserving…" : "Reserve tickets"}</button>{message && <p className="trust" role="status">{message}</p>}<p className="trust"><LockKeyhole size={13}/> Payment details are not configured yet.</p></aside>;
}
