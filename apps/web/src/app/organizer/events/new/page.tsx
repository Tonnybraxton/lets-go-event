"use client";

import { useState } from "react";
import { MapPinned, ShieldCheck } from "lucide-react";

export default function CreateEventPage() {
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setSaving(true); setMessage("");
    const form = event.currentTarget;
    const fields = Object.fromEntries(new FormData(form));
    try {
      const response = await fetch("/api/events/drafts", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(fields)});
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || "Could not create draft.");
      setMessage(`Draft created (${payload.slug}). Review and publish it in Django Admin.`); form.reset();
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not create draft."); }
    finally { setSaving(false); }
  }
  return <div className="shell"><header className="page-hero"><p className="eyebrow">Organizer studio</p><h1>Create something<br/>people remember.</h1><p className="muted">Your event is saved as a draft and appears publicly only after an operations review.</p></header><form className="form-card" onSubmit={submit}><div className="form-grid"><div className="form-group full"><label htmlFor="title">Event title</label><input id="title" name="title" placeholder="e.g. Sunday Rooftop" required minLength={5}/></div><div className="form-group full"><label htmlFor="summary">Short summary</label><textarea id="summary" name="summary" placeholder="Tell customers why this is worth leaving home for." required minLength={20}/></div><div className="form-group"><label htmlFor="category">Category</label><select id="category" name="category" defaultValue="Music"><option>Music</option><option>Nightlife</option><option>Festivals</option><option>Comedy</option><option>Food & Drink</option><option>Conferences</option></select></div><div className="form-group"><label htmlFor="startsAt">Starts</label><input id="startsAt" name="startsAt" type="datetime-local" required/></div><div className="form-group"><label htmlFor="venue">Venue name</label><input id="venue" name="venue" placeholder="KICC" required/></div><div className="form-group"><label htmlFor="city">City</label><input id="city" name="city" placeholder="Nairobi" required/></div><div className="form-group full"><label htmlFor="address">Venue address</label><input id="address" name="address" placeholder="Street, area or landmark" required/><p className="privacy-note"><MapPinned size={14}/> Exact coordinates can be added by operations before publishing.</p></div><div className="form-group"><label htmlFor="ticketName">First ticket tier</label><input id="ticketName" name="ticketName" placeholder="Early Bird" required/></div><div className="form-group"><label htmlFor="ticketPrice">Price (KES)</label><input id="ticketPrice" name="ticketPrice" type="number" min="0" placeholder="1500" required/></div><div className="form-group"><label htmlFor="quantity">Inventory</label><input id="quantity" name="quantity" type="number" min="1" max="100000" placeholder="250" required/></div></div><div style={{display:"flex",justifyContent:"space-between",alignItems:"center",gap:15,marginTop:26,flexWrap:"wrap"}}><p className="privacy-note"><ShieldCheck size={14}/> Drafts require operations approval before publication.</p><button type="submit" className="button button-violet" disabled={saving}>{saving ? "Saving…" : "Save event draft"}</button></div>{message && <p role="status" className="privacy-note" style={{marginTop:18}}>{message}</p>}</form></div>;
}
