import { Inject, Injectable, NotFoundException } from "@nestjs/common";
import { DemoLocationProvider, LOCATION_PROVIDER, type LocationProvider } from "./location-provider.js";
import { distanceBetweenKm } from "./geo.js";

type GeoEvent = { id: string; slug: string; title: string; category: string; venue: string; area: string; city: string; latitude: number; longitude: number; startAt: string; priceFromMinor: number; currency: string; popularity: number };

const demoEvents: GeoEvent[] = [
  { id: "evt_01", slug: "nairobi-after-dark", title: "Nairobi After Dark", category: "Nightlife", venue: "The Alchemist Garden", area: "Westlands", city: "Nairobi", latitude: -1.2635, longitude: 36.8047, startAt: "2026-10-17T18:00:00+03:00", priceFromMinor: 180000, currency: "KES", popularity: 98 },
  { id: "evt_02", slug: "sunset-sessions", title: "Sunset Sessions", category: "Music", venue: "The View Rooftop", area: "Kilimani", city: "Nairobi", latitude: -1.2929, longitude: 36.7854, startAt: "2026-09-27T15:00:00+03:00", priceFromMinor: 120000, currency: "KES", popularity: 88 },
  { id: "evt_03", slug: "city-food-weekend", title: "City Food Weekend", category: "Food & Drink", venue: "Jamhuri Gardens", area: "Woodley", city: "Nairobi", latitude: -1.3097, longitude: 36.7774, startAt: "2026-10-03T11:00:00+03:00", priceFromMinor: 50000, currency: "KES", popularity: 82 },
];

@Injectable()
export class EventsService {
  constructor(@Inject(LOCATION_PROVIDER) private readonly locations: LocationProvider) {}
  autocomplete(query: string) { return this.locations.searchLocations(query); }
  async nearby(locationId: string, radiusKm: number, category?: string) {
    const location = await this.locations.geocode(locationId);
    if (!location) throw new NotFoundException("Discovery location not found");
    const items = demoEvents.map((event) => ({ ...event, distanceKm: Number(distanceBetweenKm(location, event).toFixed(1)) })).filter((event) => event.distanceKm <= radiusKm && (!category || event.category === category)).sort((a, b) => (b.popularity - a.popularity) * .04 + a.distanceKm - b.distanceKm);
    return { discoveryLocation: location, radiusKm, count: items.length, items };
  }
}

export const locationProvider = { provide: LOCATION_PROVIDER, useClass: DemoLocationProvider };
