"use client";

import type { DiscoveryLocation, EventListing } from "@letsgo/types";
import dynamic from "next/dynamic";

export interface EventMapProps {
  events: EventListing[];
  selectedLocation?: DiscoveryLocation | undefined;
  radiusKm?: number | undefined;
  mode?: "kenya" | "venue" | undefined;
  compact?: boolean | undefined;
  title?: string | undefined;
}

const LeafletEventMap = dynamic(
  () => import("@/components/leaflet-event-map").then((module) => module.LeafletEventMap),
  {
    ssr: false,
    loading: () => <div className="map-loading" role="status">Preparing the Kenya event map…</div>,
  },
);

export function EventMap({
  events,
  selectedLocation,
  radiusKm,
  mode = "kenya",
  compact = false,
  title = mode === "kenya" ? "Kenya event map" : "Event location",
}: EventMapProps) {
  return <section className={`event-map-card ${compact ? "compact" : ""}`} aria-label={title}>
    <div className="map-heading">
      <div>
        <p className="eyebrow">Location view</p>
        <h2>{title}</h2>
      </div>
      <p>{events.length} {events.length === 1 ? "event location" : "event locations"} shown</p>
    </div>
    <LeafletEventMap
      events={events}
      selectedLocation={selectedLocation}
      radiusKm={radiusKm}
      mode={mode}
      compact={compact}
    />
    <div className="map-legend" aria-label="Map legend">
      <span><i className="legend-dot event"/> Event</span>
      {selectedLocation && <span><i className="legend-dot search"/> Selected search area</span>}
      <span className="map-privacy">Map uses the place you selected—not your live device location.</span>
    </div>
  </section>;
}
