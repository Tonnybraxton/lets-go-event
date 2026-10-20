import { ArrowRight, ArrowUpRight, CalendarDays, MapPin, Sparkles } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { EventCard } from "@/components/event-card";
import { LocationSearch } from "@/components/location-search";
import { getAvailableEvents, getHotCounties, getNearbyEvents, locations } from "@/lib/data";

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
  const hotCounties = getHotCounties(catalogue).slice(0, 10);

  return <>
    <section className="hero">
      <div className="hero-image">
        <Image
          src={featured.image}
          alt={`${featured.title} event poster`}
          fill
          unoptimized
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
    <section className="section shell county-discovery-section" aria-labelledby="county-discovery-title">
      <div className="county-discovery">
        <div className="county-discovery-heading">
          <div>
            <p className="eyebrow">Explore by county</p>
            <h2 id="county-discovery-title">Pick a place. Find your people.</h2>
            <p>Browse upcoming events across Kenya, then check dates and tickets with the original organiser.</p>
          </div>
          <Link className="button button-ghost" href="/explore">Explore all Kenya <ArrowRight size={16}/></Link>
        </div>
        <div className="county-discovery-grid">
          {hotCounties.map((item, index) => <Link key={item.county} className="county-feature-card" href={`/explore?county=${encodeURIComponent(item.county)}`}>
            <span className="county-feature-top"><span>{String(index + 1).padStart(2, "0")} · COUNTY</span><ArrowUpRight size={18}/></span>
            <strong>{item.county}</strong>
            <span className="county-feature-meta">{item.eventCount} upcoming {item.eventCount === 1 ? "event" : "events"} · Next {new Date(item.nextStartAt).toLocaleDateString("en-KE", { weekday: "short", day: "numeric", month: "short", timeZone: "Africa/Nairobi" })}</span>
          </Link>)}
        </div>
      </div>
    </section>
    <section className="section shell">
      <div className="section-heading">
        <div><p className="eyebrow">Coming up next</p><h2>More plans across Kenya</h2></div>
        <p>Current listings with dates and ticket details linked to their original sources.</p>
      </div>
      <div className="event-grid">{curated.map((event) => <EventCard key={event.id} event={event}/>)}</div>
    </section>
  </>;
}

