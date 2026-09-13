import { BadgeCheck, CalendarDays, Clock3, MapPin, Share2 } from "lucide-react";
import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { TicketPanel } from "@/components/ticket-panel";
import { EventMap } from "@/components/event-map";
import { events, getEvent } from "@/lib/data";

export function generateStaticParams() {
  return events.map((event) => ({ slug: event.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const event = await getEvent((await params).slug);
  return event ? { title: event.title, description: event.summary } : {};
}

export default async function EventPage({ params }: { params: Promise<{ slug: string }> }) {
  const event = await getEvent((await params).slug);
  if (!event) notFound();
  const start = new Date(event.startAt);
  const scheduleLabel = event.dateConfirmed === false
    ? "Date needs organizer confirmation"
    : event.timeConfirmed === false
      ? `${start.toLocaleDateString("en-KE", {dateStyle:"medium"})} · time to be confirmed`
      : start.toLocaleString("en-KE", {dateStyle:"medium", timeStyle:"short"});

  return <>
    <section className="event-detail-hero">
      <Image src={event.image} alt={`${event.title} event artwork`} fill priority sizes="100vw" />
      <div className="detail-title">
        <p className="eyebrow">{event.category} · {event.county ?? event.city}</p>
        <h1>{event.title}</h1>
        <div className="hero-meta">
          <span><CalendarDays size={17}/>{start.toLocaleDateString("en-KE", {weekday:"long", day:"numeric", month:"long"})}</span>
          <span><Clock3 size={17}/>{event.dateConfirmed === false ? "Confirm date at source" : event.timeConfirmed === false ? "Time to be confirmed" : start.toLocaleTimeString("en-KE", {hour:"numeric", minute:"2-digit"})}</span>
          <span><MapPin size={17}/>{event.venue}</span>
        </div>
      </div>
    </section>
    <div className="shell detail-grid">
      <article className="prose">
        <p className="eyebrow">The experience</p>
        <h2>{event.summary}</h2>
        <p>{event.description}</p>
        {event.isExternalListing && <div className="info-item">
          <small>Original ticket source</small>
          <strong>{event.sourceName}</strong>
          <p className="muted" style={{marginBottom:0}}>Confirm final details, availability and policies on the original listing before booking.</p>
        </div>}
        <div className="info-list">
          <div className="info-item"><small>Hosted by</small><strong>{event.organizer} {event.organizerVerified && <BadgeCheck size={16} color="#8b5cf6" style={{display:"inline"}}/>}</strong></div>
          <div className="info-item"><small>Venue</small><strong>{event.venue}, {event.area}</strong></div>
          <div className="info-item"><small>Date & time</small><strong>{scheduleLabel}</strong></div>
          <div className="info-item"><small>Share</small><strong><Share2 size={16} style={{display:"inline"}}/> Send to your people</strong></div>
        </div>
        <h2>Good to know</h2>
        <p>{event.isExternalListing ? "This event uses an external ticket source. The original source controls ticket availability, checkout and final event details." : "Doors open one hour before start. A valid secure digital ticket is required at entry."}</p>
        <h2>Location</h2>
        <div className="info-item">
          <small>Selected event venue—not your live position</small>
          <strong>{event.address}, {event.area}, {event.city}{event.county ? `, ${event.county} County` : ""}</strong>
          {event.locationApproximate && <p className="muted" style={{marginBottom:0}}>The source did not publish an exact venue pin, so this marker is approximate.</p>}
        </div>
        <EventMap events={[event]} mode="venue" compact title={`${event.venue}, ${event.city}`}/>
      </article>
      <TicketPanel tiers={event.ticketTiers} externalUrl={event.isExternalListing ? event.sourceUrl : undefined} priceAvailable={event.priceAvailable}/>
    </div>
  </>;
}
