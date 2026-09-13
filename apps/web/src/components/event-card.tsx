"use client";

import type { EventListing, NearbyEvent } from "@letsgo/types";
import { BadgeCheck, Heart, MapPin } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { formatMoney } from "@/lib/data";

export function EventCard({ event }: { event: EventListing | NearbyEvent }) {
  const [saved, setSaved] = useState(false);
  useEffect(() => {
    // localStorage is the browser-backed source of truth for saved events.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setSaved(JSON.parse(window.localStorage.getItem("letsgo.savedEvents") ?? "[]").includes(event.slug));
  }, [event.slug]);
  function toggleSaved() {
    const savedEvents = new Set<string>(JSON.parse(window.localStorage.getItem("letsgo.savedEvents") ?? "[]"));
    if (saved) savedEvents.delete(event.slug);
    else savedEvents.add(event.slug);
    window.localStorage.setItem("letsgo.savedEvents", JSON.stringify([...savedEvents]));
    setSaved(!saved);
  }
  const date = new Date(event.startAt);
  const distance = "distanceLabel" in event ? event.distanceLabel : `${event.area}, ${event.city}`;
  return <article className="event-card" style={{position:"relative"}}>
    <Link href={`/events/${event.slug}`} aria-label={`Open ${event.title}`}>
      <div className="card-image"><Image src={event.image} alt="" fill sizes="(max-width: 620px) 100vw, (max-width: 900px) 50vw, 33vw"/><div className="card-overlay"/>{event.hotRank && <span className="badge badge-hot">Top 10 · #{event.hotRank}</span>}{!event.hotRank && event.sellingFast && <span className="badge badge-hot">Selling fast</span>}<span className="date-chip"><span>{date.toLocaleDateString("en-KE", {month:"short"}).toUpperCase()}</span><strong>{date.getDate()}</strong></span></div>
      <div className="card-body"><span className="card-kicker">{event.category}{event.county ? ` · ${event.county}` : ""}</span><h3>{event.title}</h3><div className="card-detail"><MapPin size={14}/>{distance}{event.locationApproximate ? " · approximate pin" : ""}</div><div className="card-detail"><BadgeCheck size={14} color="#8b5cf6"/>{event.organizer}</div><div className="card-footer"><div><small>{event.priceAvailable === false ? "Tickets" : "From"}</small><strong>{event.priceAvailable === false ? "See source" : event.priceFromMinor === 0 ? "Free" : formatMoney(event.priceFromMinor, event.currency)}</strong></div><span className="muted" style={{fontSize:12}}>{date.toLocaleDateString("en-KE", event.timeConfirmed === false ? {weekday:"short", day:"numeric", month:"short"} : {weekday:"short", hour:"numeric", minute:"2-digit"})}</span></div></div>
    </Link>
    <button className="favorite" aria-label={`${saved ? "Remove" : "Save"} ${event.title}`} aria-pressed={saved} type="button" onClick={toggleSaved}><Heart size={17} fill={saved ? "currentColor" : "none"}/></button>
  </article>;
}
