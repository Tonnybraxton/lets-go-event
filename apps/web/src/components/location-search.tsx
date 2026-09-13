"use client";

import type { DiscoveryLocation } from "@letsgo/types";
import { LocateFixed, MapPin, Search, ShieldCheck } from "lucide-react";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";

export function LocationSearch({ locations }: { locations: DiscoveryLocation[] }) {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [interest, setInterest] = useState("");
  const [location, setLocation] = useState(locations[0]!);
  const [radius, setRadius] = useState("25");
  const matches = useMemo(() => query.length < 2 ? [] : locations.filter((item) => item.label.toLowerCase().includes(query.toLowerCase())).slice(0, 5), [locations, query]);

  function choose(item: DiscoveryLocation) {
    setLocation(item); setQuery(item.label);
    window.localStorage.setItem("letsgo.discoveryLocation", JSON.stringify(item));
  }
  function submit(event: React.FormEvent) {
    event.preventDefault();
    const params = new URLSearchParams({ location: location.id, radius });
    if (interest.trim()) params.set("q", interest.trim());
    router.push(`/explore?${params.toString()}`);
  }

  return <div className="discovery-box">
    <form className="discovery-form" onSubmit={submit}>
      <div className="field" style={{position:"relative"}}><label htmlFor="location">Where do you want to go?</label><div style={{display:"flex",alignItems:"center",gap:8}}><MapPin size={17} color="#a78bfa"/><input id="location" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search city or area..." autoComplete="off" /></div>
        {matches.length > 0 && <div className="suggestions" role="listbox">{matches.map((item) => <button className="suggestion" type="button" key={item.id} onClick={() => choose(item)}><span><strong>{item.label.split(",")[0]}</strong><small className="muted" style={{display:"block",marginTop:3}}>{item.city}, {item.country}</small></span><LocateFixed size={16} color="#8b5cf6"/></button>)}</div>}
      </div>
      <div className="field"><label htmlFor="search">What are you looking for?</label><div style={{display:"flex",alignItems:"center",gap:8}}><Search size={17} color="#7e8492"/><input id="search" value={interest} onChange={(event) => setInterest(event.target.value)} placeholder="Concert, festival, comedy..." /></div></div>
      <div className="field"><label htmlFor="radius">Search radius</label><select id="radius" value={radius} onChange={(event) => setRadius(event.target.value)}><option value="5">Within 5 km</option><option value="10">Within 10 km</option><option value="25">Within 25 km</option><option value="50">Within 50 km</option><option value="100">Within 100 km</option></select></div>
      <button className="button button-violet" type="submit">Scan this area <Search size={17}/></button>
    </form>
    <p className="privacy-note"><ShieldCheck size={14}/> You choose where to explore. We never request or track your physical location automatically.</p>
  </div>;
}
