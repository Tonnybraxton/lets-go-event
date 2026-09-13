"use client";

import type { DiscoveryLocation, EventListing } from "@letsgo/types";
import type { LatLngBoundsExpression, LatLngExpression } from "leaflet";
import Link from "next/link";
import { Circle, CircleMarker, MapContainer, Polygon, Popup, TileLayer, ZoomControl } from "react-leaflet";

interface LeafletEventMapProps {
  events: EventListing[];
  selectedLocation?: DiscoveryLocation | undefined;
  radiusKm?: number | undefined;
  mode: "kenya" | "venue";
  compact: boolean;
}

interface MappedEvent {
  event: EventListing;
  position: LatLngExpression;
  approximate: boolean;
}

const KENYA_CENTER: LatLngExpression = [-0.0236, 37.9062];
const KENYA_BOUNDS: LatLngBoundsExpression = [[-4.95, 33.65], [5.15, 42.2]];
const EAST_AFRICA_BOUNDS: LatLngBoundsExpression = [[-8.5, 28], [10, 48]];
const KENYA_OUTLINE: LatLngExpression[] = [
  [4.62, 41.9], [3.98, 41.91], [3.2, 40.99], [1.05, 41.02], [-1.7, 41.56],
  [-4.68, 39.22], [-4.61, 37.63], [-3.38, 37.58], [-2.84, 33.93], [-1.02, 33.91],
  [0.18, 34.52], [1.67, 34.54], [3.96, 34.2], [4.62, 36.9], [4.62, 41.9],
];

const CITY_CENTRES: Record<string, [number, number]> = {
  nairobi: [-1.2864, 36.8172],
  mombasa: [-4.0435, 39.6682],
  kisumu: [-0.1022, 34.7617],
  nakuru: [-0.3031, 36.08],
  eldoret: [0.5143, 35.2698],
  nanyuki: [0.0167, 37.0728],
  naivasha: [-0.7172, 36.431],
  kisii: [-0.6817, 34.7667],
  migori: [-1.0634, 34.4731],
  bomet: [-0.7813, 35.3416],
  nyeri: [-0.4201, 36.9476],
  kitui: [-1.3667, 38.0167],
  kilifi: [-3.6305, 39.8499],
  molo: [-0.247, 35.737],
};

function mapEvent(event: EventListing): MappedEvent | null {
  const coordinatesAreInKenya = event.latitude >= -5.1 && event.latitude <= 5.2
    && event.longitude >= 33.5 && event.longitude <= 42.3;
  if (coordinatesAreInKenya) {
    return { event, position: [event.latitude, event.longitude], approximate: false };
  }
  const cityCentre = CITY_CENTRES[event.city.toLowerCase()];
  return cityCentre ? { event, position: cityCentre, approximate: true } : null;
}

function MapLayers({ mappedEvents, selectedLocation, radiusKm }: {
  mappedEvents: MappedEvent[];
  selectedLocation?: DiscoveryLocation | undefined;
  radiusKm?: number | undefined;
}) {
  return <>
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    <Polygon
      positions={KENYA_OUTLINE}
      pathOptions={{ color: "#a78bfa", weight: 2, opacity: 0.8, fillColor: "#8b5cf6", fillOpacity: 0.06 }}
    />
    {selectedLocation && <>
      <Circle
        center={[selectedLocation.latitude, selectedLocation.longitude]}
        radius={(radiusKm ?? 25) * 1000}
        pathOptions={{ color: "#8b5cf6", fillColor: "#8b5cf6", fillOpacity: 0.09, weight: 1.5 }}
      />
      <CircleMarker
        center={[selectedLocation.latitude, selectedLocation.longitude]}
        radius={7}
        pathOptions={{ color: "#ffffff", fillColor: "#8b5cf6", fillOpacity: 1, weight: 2 }}
      >
        <Popup><div className="map-popup"><span>Selected search point</span><strong>{selectedLocation.label}</strong></div></Popup>
      </CircleMarker>
    </>}
    {mappedEvents.map(({ event, position, approximate }) => <CircleMarker
      key={event.id}
      center={position}
      radius={9}
      pathOptions={{ color: "#fff7ed", fillColor: "#f97316", fillOpacity: 1, weight: 2 }}
    >
      <Popup minWidth={220}>
        <div className="map-popup">
          <span>{event.category}</span>
          <strong>{event.title}</strong>
          <small>{event.venue}, {event.city}</small>
          {(approximate || event.locationApproximate) && <small>Approximate published location</small>}
          <Link href={`/events/${event.slug}`}>View event →</Link>
        </div>
      </Popup>
    </CircleMarker>)}
  </>;
}

export function LeafletEventMap({ events, selectedLocation, radiusKm, mode, compact }: LeafletEventMapProps) {
  const mappedEvents = events.map(mapEvent).filter((value): value is MappedEvent => value !== null);
  const focusPosition = mappedEvents[0]?.position ?? KENYA_CENTER;
  const mapKey = `${mode}-${events.map((event) => event.id).join("-")}`;
  const layers = <MapLayers mappedEvents={mappedEvents} selectedLocation={selectedLocation} radiusKm={radiusKm}/>;

  return <div className={`leaflet-map-shell ${mode} ${compact ? "compact" : ""}`}>
    {mode === "venue" ? <MapContainer
      key={mapKey}
      center={focusPosition}
      zoom={14}
      minZoom={5}
      maxBounds={EAST_AFRICA_BOUNDS}
      maxBoundsViscosity={0.75}
      scrollWheelZoom
      zoomControl={false}
      className="event-map"
    >
      {layers}
      <ZoomControl position="bottomright"/>
    </MapContainer> : <MapContainer
      key={mapKey}
      bounds={KENYA_BOUNDS}
      minZoom={6}
      maxZoom={12}
      maxBounds={KENYA_BOUNDS}
      maxBoundsViscosity={1}
      scrollWheelZoom
      zoomControl={false}
      className="event-map"
    >
      {layers}
      <ZoomControl position="bottomright"/>
    </MapContainer>}
  </div>;
}
