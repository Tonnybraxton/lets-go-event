import { Flame, Grid3X3, ListFilter, Map, MapPinned } from "lucide-react";
import Link from "next/link";
import { EventCard } from "@/components/event-card";
import { EventMap } from "@/components/event-map";
import {
  getAvailableEvents,
  getHotCounties,
  getLocation,
  getTopKenyaEvents,
  nearbyEvents,
} from "@/lib/data";

type SearchParams = Record<string, string | string[] | undefined>;

export const dynamic = "force-dynamic";

export default async function ExplorePage({ searchParams }: { searchParams: Promise<SearchParams> }) {
  const params = await searchParams;
  const locationId = typeof params.location === "string" ? params.location : undefined;
  const parsedRadius = typeof params.radius === "string" ? Number(params.radius) : 25;
  const radius = [5, 10, 25, 50, 100].includes(parsedRadius) ? parsedRadius : 25;
  const view = params.view === "map" ? "map" : "grid";
  const category = typeof params.category === "string" ? params.category : undefined;
  const mood = typeof params.mood === "string" ? params.mood : undefined;
  const searchQuery = typeof params.q === "string" ? params.q.trim() : "";
  const county = typeof params.county === "string" ? params.county : undefined;
  const date = typeof params.date === "string" && ["today", "weekend", "week"].includes(params.date)
    ? params.date as "today" | "weekend" | "week"
    : undefined;
  const catalogue = await getAvailableEvents();
  const national = getTopKenyaEvents(catalogue);
  const location = locationId ? getLocation(locationId) : undefined;
  const baseResults = location ? nearbyEvents(location, radius, catalogue) : national;
  const now = Date.now();
  const nairobiDate = (value: Date) => new Intl.DateTimeFormat("en-CA", { timeZone: "Africa/Nairobi", year: "numeric", month: "2-digit", day: "2-digit" }).format(value);
  const weekday = new Intl.DateTimeFormat("en-US", { timeZone: "Africa/Nairobi", weekday: "short" }).format(new Date(now));
  const weekdayNumber = ({ Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 } as Record<string, number>)[weekday] ?? 0;
  const saturdayOffset = (6 - weekdayNumber + 7) % 7;
  const weekendStart = nairobiDate(new Date(now + saturdayOffset * 86_400_000));
  const weekendEnd = nairobiDate(new Date(now + (saturdayOffset + 1) * 86_400_000));
  const today = nairobiDate(new Date(now));
  const results = baseResults.filter((event) =>
    (!category || event.category.toLowerCase() === category.toLowerCase())
    && (!mood || event.mood.toLowerCase().includes(mood.toLowerCase()))
    && (!searchQuery || [event.title, event.summary, event.category, event.mood, event.city, event.county].filter(Boolean).join(" ").toLowerCase().includes(searchQuery.toLowerCase()))
    && (!county || event.county?.toLowerCase() === county.toLowerCase()),
  ).filter((event) => {
    if (!date) return true;
    const eventDate = nairobiDate(new Date(event.startAt));
    if (date === "today") return eventDate === today;
    if (date === "weekend") return eventDate >= weekendStart && eventDate <= weekendEnd;
    return Date.parse(event.startAt) <= now + 7 * 86_400_000;
  });
  const hotCounties = getHotCounties(catalogue);
  const guideLocation = location?.label.split(",")[0] ?? county;

  const exploreHref = (updates: {
    view?: "grid" | "map";
    radius?: number;
    category?: string | null;
    mood?: string | null;
    query?: string | null;
    county?: string | null;
    location?: string | null;
    date?: string | null;
  }) => {
    const params = new URLSearchParams();
    const nextLocation = updates.location === undefined ? locationId : updates.location;
    const nextCategory = updates.category === undefined ? category : updates.category;
    const nextMood = updates.mood === undefined ? mood : updates.mood;
    const nextQuery = updates.query === undefined ? searchQuery : updates.query;
    const nextCounty = updates.county === undefined ? county : updates.county;
    const nextDate = updates.date === undefined ? date : updates.date;
    const nextRadius = updates.radius ?? radius;
    params.set("view", updates.view ?? view);
    if (nextLocation) {
      params.set("location", nextLocation);
      params.set("radius", String(nextRadius));
    }
    if (nextCategory) params.set("category", nextCategory);
    if (nextMood) params.set("mood", nextMood);
    if (nextQuery) params.set("q", nextQuery);
    if (nextCounty) params.set("county", nextCounty);
    if (nextDate) params.set("date", nextDate);
    return `/explore?${params.toString()}`;
  };

  return <div className="shell">
    <header className="page-hero">
      <p className="eyebrow">{location ? "Local discovery" : guideLocation ? `${guideLocation} events guide` : "Kenya events guide"}</p>
      <h1>{location ? <>Events around<br/>{location.label.split(",")[0]}</> : guideLocation ? <>What’s on in<br/>{guideLocation}</> : <>What’s on across<br/>Kenya</>}</h1>
      <p className="muted">
        {results.length} {searchQuery ? `matching “${searchQuery}”` : category ? category.toLowerCase() : mood ? mood.toLowerCase() : "upcoming"} {results.length === 1 ? "event" : "events"}
        {location ? ` within ${radius} km of your selected place.` : " found in current public event listings. Check the source link for the latest availability and details."}
      </p>
    </header>

    <section className="hot-counties" aria-labelledby="hot-counties-heading">
      <div className="hot-counties-heading">
        <div><p className="eyebrow"><Flame size={13}/> Where it’s happening</p><h2 id="hot-counties-heading">Event hotspots</h2></div>
        <p>Browse locations represented by the current upcoming listings.</p>
      </div>
      <div className="county-grid">
        {hotCounties.map((item, index) => <Link
          key={item.county}
          className={`county-card ${county === item.county ? "active" : ""}`}
          href={exploreHref({ county: county === item.county ? null : item.county, location: null })}
        >
          <span>#{index + 1}</span>
          <strong>{item.county}</strong>
          <small>{item.eventCount} {item.eventCount === 1 ? "event" : "events"}</small>
        </Link>)}
      </div>
    </section>

    <div className="filter-bar" aria-label="Explore view and discovery filters">
      <Link className={`filter-chip ${view === "grid" ? "active" : ""}`} href={exploreHref({view:"grid"})} aria-current={view === "grid" ? "page" : undefined}><Grid3X3 size={14} style={{display:"inline",marginRight:6}}/>Grid</Link>
      <Link className={`filter-chip ${view === "map" ? "active" : ""}`} href={exploreHref({view:"map"})} aria-current={view === "map" ? "page" : undefined}><Map size={14} style={{display:"inline",marginRight:6}}/>Map</Link>
      {location ? <Link className="filter-chip active" href={exploreHref({location:null})}><MapPinned size={14} style={{display:"inline",marginRight:6}}/>{location.label.split(",")[0]} ×</Link> : <span className="filter-chip active"><MapPinned size={14} style={{display:"inline",marginRight:6}}/>{county ?? "Kenya"}</span>}
      {([ ["today", "Today"], ["weekend", "This weekend"], ["week", "Next 7 days"] ] as const).map(([value, label]) => <Link key={value} className={`filter-chip ${date === value ? "active" : ""}`} href={exploreHref({date: date === value ? null : value})}>{label}</Link>)}
      {date && <Link className="filter-chip active" href={exploreHref({date:null})}>Clear date ×</Link>}
      {county && <Link className="filter-chip active" href={exploreHref({county:null})}><Flame size={14} style={{display:"inline",marginRight:6}}/>{county} ×</Link>}
      {category ? <Link className="filter-chip active" href={exploreHref({category:null})}><ListFilter size={14} style={{display:"inline",marginRight:6}}/>{category} ×</Link> : <span className="filter-chip"><ListFilter size={14} style={{display:"inline",marginRight:6}}/>All categories</span>}
      {mood && <Link className="filter-chip active" href={exploreHref({mood:null})}>{mood} ×</Link>}
      {searchQuery && <Link className="filter-chip active" href={exploreHref({query:null})}>“{searchQuery}” ×</Link>}
      {location && [5,10,25,50,100].map((value) => <Link key={value} className={`filter-chip ${value === radius ? "active" : ""}`} href={exploreHref({radius:value})}>{value} km</Link>)}
    </div>

    {view === "map"
      ? <EventMap events={results} selectedLocation={location} radiusKm={location ? radius : undefined} mode="kenya" title={county ? `${county} event map` : "Upcoming events across Kenya"}/>
      : results.length
        ? <div className="event-grid">{results.map((event) => <EventCard key={event.id} event={event}/>)}</div>
        : <div className="form-card"><p className="eyebrow">No matching events</p><h2>Try another date or location.</h2><p className="muted">Past listings are automatically hidden. Event dates and ticket availability can change, so check the original source before booking.</p><Link className="button button-violet" href="/explore">Show all upcoming events</Link></div>}
  </div>;
}

