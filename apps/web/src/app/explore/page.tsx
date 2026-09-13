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
  const catalogue = await getAvailableEvents();
  const national = getTopKenyaEvents(catalogue);
  const location = locationId ? getLocation(locationId) : undefined;
  const baseResults = location ? nearbyEvents(location, radius, catalogue) : national;
  const results = baseResults.filter((event) =>
    (!category || event.category.toLowerCase() === category.toLowerCase())
    && (!mood || event.mood.toLowerCase().includes(mood.toLowerCase()))
    && (!searchQuery || [event.title, event.summary, event.category, event.mood, event.city, event.county].filter(Boolean).join(" ").toLowerCase().includes(searchQuery.toLowerCase()))
    && (!county || event.county?.toLowerCase() === county.toLowerCase()),
  );
  const hotCounties = getHotCounties(catalogue);

  const exploreHref = (updates: {
    view?: "grid" | "map";
    radius?: number;
    category?: string | null;
    mood?: string | null;
    query?: string | null;
    county?: string | null;
    location?: string | null;
  }) => {
    const params = new URLSearchParams();
    const nextLocation = updates.location === undefined ? locationId : updates.location;
    const nextCategory = updates.category === undefined ? category : updates.category;
    const nextMood = updates.mood === undefined ? mood : updates.mood;
    const nextQuery = updates.query === undefined ? searchQuery : updates.query;
    const nextCounty = updates.county === undefined ? county : updates.county;
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
    return `/explore?${params.toString()}`;
  };

  return <div className="shell">
    <header className="page-hero">
      <p className="eyebrow">{location ? "Local discovery" : "Web-researched Kenya collection"}</p>
      <h1>{location ? <>Events around<br/>{location.label.split(",")[0]}</> : <>Top upcoming events<br/>across Kenya</>}</h1>
      <p className="muted">
        {results.length} {searchQuery ? `matching “${searchQuery}”` : category ? category.toLowerCase() : mood ? mood.toLowerCase() : "curated"} {results.length === 1 ? "experience" : "experiences"}
        {location ? ` within ${radius} km of your selected place.` : " mapped from verified public listings and editable in Django Admin."}
      </p>
    </header>

    <section className="hot-counties" aria-labelledby="hot-counties-heading">
      <div className="hot-counties-heading">
        <div><p className="eyebrow"><Flame size={13}/> County hotspots</p><h2 id="hot-counties-heading">Hot counties in this Top 10</h2></div>
        <p>Ranked by the number of curated upcoming listings, then the nearest event date.</p>
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
      {location ? <Link className="filter-chip active" href={exploreHref({location:null})}><MapPinned size={14} style={{display:"inline",marginRight:6}}/>{location.label.split(",")[0]} ×</Link> : <span className="filter-chip active"><MapPinned size={14} style={{display:"inline",marginRight:6}}/>Nationwide Top 10</span>}
      {county && <Link className="filter-chip active" href={exploreHref({county:null})}><Flame size={14} style={{display:"inline",marginRight:6}}/>{county} ×</Link>}
      {category ? <Link className="filter-chip active" href={exploreHref({category:null})}><ListFilter size={14} style={{display:"inline",marginRight:6}}/>{category} ×</Link> : <span className="filter-chip"><ListFilter size={14} style={{display:"inline",marginRight:6}}/>All categories</span>}
      {mood && <Link className="filter-chip active" href={exploreHref({mood:null})}>{mood} ×</Link>}
      {searchQuery && <Link className="filter-chip active" href={exploreHref({query:null})}>“{searchQuery}” ×</Link>}
      {location && [5,10,25,50,100].map((value) => <Link key={value} className={`filter-chip ${value === radius ? "active" : ""}`} href={exploreHref({radius:value})}>{value} km</Link>)}
    </div>

    {view === "map"
      ? <EventMap events={results} selectedLocation={location} radiusKm={location ? radius : undefined} mode="kenya" title={county ? `${county} event map` : "Top 10 events across Kenya"}/>
      : results.length
        ? <div className="event-grid">{results.map((event) => <EventCard key={event.id} event={event}/>)}</div>
        : <div className="form-card"><p className="eyebrow">No matching events</p><h2>Try another county or browse nationwide.</h2><p className="muted">Only web-verified future listings are included in the curated collection.</p><Link className="button button-violet" href="/explore">Show the nationwide Top 10</Link></div>}
  </div>;
}
