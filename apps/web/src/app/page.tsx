import { ArrowRight, CalendarDays, MapPin, Sparkles } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { EventCard } from "@/components/event-card";
import { LocationSearch } from "@/components/location-search";
import { getAvailableEvents, getNearbyEvents, locations } from "@/lib/data";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const catalogue = await getAvailableEvents();
  const featured = catalogue.find((event) => event.featured) ?? catalogue[0]!;
  const featuredStart = new Date(featured.startAt);
  const featuredDate = featuredStart.toLocaleDateString("en-KE", {
    weekday: "short",
    day: "numeric",
    month: "short",
    timeZone: featured.timezone,
  });
  const featuredTime = featuredStart.toLocaleTimeString("en-KE", {
    hour: "numeric",
    minute: "2-digit",
    timeZone: featured.timezone,
  });
  const featuredLocation = [featured.venue, featured.area].filter(Boolean).join(", ");
  const featuredTrust = featured.sourceName
    ? `Tickets via ${featured.sourceName}`
    : featured.organizerVerified
      ? "Verified organizer"
      : `Hosted by ${featured.organizer}`;

  const westlands = locations[0]!;
  const nearby = (await getNearbyEvents(westlands, 25)).slice(0, 6);
  const curated = catalogue.filter((event) => event.slug !== featured.slug).slice(0, 3);

  return <>
    <section className="hero">
      <div className="hero-image">
        <Image
          src={featured.image}
          alt={`${featured.title} event cover`}
          fill
          priority
          sizes="100vw"
        />
      </div>
      <div className="shell hero-content">
        <p className="eyebrow">{`Featured · ${featured.city} · ${featuredDate}`}</p>
        <h1>{featured.title}</h1>
        <p className="hero-copy">{featured.summary}</p>
        <div className="hero-meta">
          <span><CalendarDays size={17}/>{featuredDate}, {featuredTime}</span>
          <span><MapPin size={17}/>{featuredLocation}</span>
          <span><Sparkles size={17}/>{featuredTrust}</span>
        </div>
        <div className="hero-actions">
          <Link className="button button-primary" href={`/events/${featured.slug}`}>
            Explore {featured.title} <ArrowRight size={17}/>
          </Link>
          <Link className="button button-ghost" href="/organizer/events/new">
            Create an event
          </Link>
        </div>
      </div>
    </section>
    <div className="shell"><LocationSearch locations={locations}/></div>
    <section className="section shell">
      <div className="section-heading">
        <div><p className="eyebrow">Around your chosen place</p><h2>Happening near Westlands</h2></div>
        <p>Selected-location discovery, with clear distance labels and no automatic GPS request.</p>
      </div>
      <div className="event-grid">{nearby.map((event) => <EventCard key={event.id} event={event}/>)}</div>
    </section>
    <section className="section shell">
      <div className="section-heading">
        <div><p className="eyebrow">Choose a feeling</p><h2>What kind of night is it?</h2></div>
        <Link className="button button-ghost" href="/explore">See every experience <ArrowRight size={16}/></Link>
      </div>
      <div className="mood-grid">
        <Link className="mood" href="/explore?mood=Dance%20all%20night"><strong>Dance all night</strong></Link>
        <Link className="mood" href="/explore?mood=Date%20night"><strong>Date night</strong></Link>
        <Link className="mood" href="/explore?mood=Chill%20weekend"><strong>Chill weekend</strong></Link>
        <Link className="mood" href="/explore?mood=Laugh%20out%20loud"><strong>Laugh out loud</strong></Link>
      </div>
    </section>
    <section className="section shell">
      <div className="section-heading">
        <div><p className="eyebrow">Freshly curated</p><h2>Worth leaving home for</h2></div>
        <p>Published experiences managed through the event operations catalogue.</p>
      </div>
      <div className="event-grid">{curated.map((event) => <EventCard key={event.id} event={event}/>)}</div>
    </section>
  </>;
}
