import type { DiscoveryLocation, EventListing, NearbyEvent } from "@letsgo/types";

export const locations: DiscoveryLocation[] = [
  { id: "westlands-nairobi", label: "Westlands, Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.2676, longitude: 36.8108, source: "MANUAL_SEARCH" },
  { id: "kilimani-nairobi", label: "Kilimani, Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.2921, longitude: 36.7836, source: "MANUAL_SEARCH" },
  { id: "nairobi-cbd", label: "Nairobi CBD, Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.2864, longitude: 36.8172, source: "MANUAL_SEARCH" },
  { id: "karen-nairobi", label: "Karen, Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.3197, longitude: 36.6932, source: "MANUAL_SEARCH" },
  { id: "nyali-mombasa", label: "Nyali, Mombasa", city: "Mombasa", county: "Mombasa", country: "Kenya", countryCode: "KE", latitude: -4.0435, longitude: 39.7115, source: "MANUAL_SEARCH" },
  { id: "kisumu-cbd", label: "Kisumu CBD, Kisumu", city: "Kisumu", county: "Kisumu", country: "Kenya", countryCode: "KE", latitude: -0.1022, longitude: 34.7617, source: "MANUAL_SEARCH" },
  { id: "kisii-town", label: "Kisii Town, Kisii", city: "Kisii", county: "Kisii", country: "Kenya", countryCode: "KE", latitude: -0.6817, longitude: 34.7667, source: "MANUAL_SEARCH" },
  { id: "migori-town", label: "Migori Town, Migori", city: "Migori", county: "Migori", country: "Kenya", countryCode: "KE", latitude: -1.0634, longitude: 34.4731, source: "MANUAL_SEARCH" },
  { id: "bomet-town", label: "Bomet Town, Bomet", city: "Bomet", county: "Bomet", country: "Kenya", countryCode: "KE", latitude: -0.7813, longitude: 35.3416, source: "MANUAL_SEARCH" },
  { id: "nakuru-town", label: "Nakuru Town, Nakuru", city: "Nakuru", county: "Nakuru", country: "Kenya", countryCode: "KE", latitude: -0.3031, longitude: 36.08, source: "MANUAL_SEARCH" },
  { id: "eldoret-town", label: "Eldoret, Uasin Gishu", city: "Eldoret", county: "Uasin Gishu", country: "Kenya", countryCode: "KE", latitude: 0.5143, longitude: 35.2698, source: "MANUAL_SEARCH" },
  { id: "kitui-town", label: "Kitui Town, Kitui", city: "Kitui", county: "Kitui", country: "Kenya", countryCode: "KE", latitude: -1.3667, longitude: 38.0167, source: "MANUAL_SEARCH" },
  { id: "kilifi-town", label: "Kilifi Town, Kilifi", city: "Kilifi", county: "Kilifi", country: "Kenya", countryCode: "KE", latitude: -3.6305, longitude: 39.8499, source: "MANUAL_SEARCH" },
];

export const events: EventListing[] = [
  {
    id: "evt_01", slug: "nairobi-after-dark", title: "Nairobi After Dark", category: "Nightlife", mood: "Dance all night",
    summary: "A one-night collision of Afro-house, art and electric city energy.", description: "Step into a cinematic celebration of Nairobi after sunset. Three rooms, a live visual installation, local food pop-ups and a line-up built for dancing until late.",
    image: "https://images.unsplash.com/photo-1636819193902-9dbfff16bfb1?auto=format&fit=crop&w=1800&q=88", startAt: "2026-10-17T18:00:00+03:00", endAt: "2026-10-18T03:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "The Alchemist Garden", address: "Parklands Road", area: "Westlands", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2635, longitude: 36.8047,
    organizer: "Neon Nairobi Collective", organizerVerified: true, priceFromMinor: 180000, currency: "KES", sellingFast: true, featured: true,
    tags: ["Afro house", "Live art", "Food"], ticketTiers: [
      { id: "tt_01", name: "First Light", priceMinor: 180000, currency: "KES", remaining: 24, description: "Entry before 9 PM" },
      { id: "tt_02", name: "Night Pass", priceMinor: 250000, currency: "KES", remaining: 183, description: "General admission" },
      { id: "tt_03", name: "Skyline", priceMinor: 650000, currency: "KES", remaining: 18, description: "Elevated deck and lounge access" },
    ],
  },
  {
    id: "evt_02", slug: "sunset-sessions", title: "Sunset Sessions", category: "Music", mood: "Chill weekend",
    summary: "Golden-hour soul, acoustic sets and a skyline made for slow Sundays.", description: "A warm rooftop gathering with stripped-back live performances, thoughtful cocktails and panoramic Nairobi views.",
    image: "/images/events/sunset-sessions-cover.png", startAt: "2026-09-27T15:00:00+03:00", endAt: "2026-09-27T22:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "The View Rooftop", address: "Wood Avenue", area: "Kilimani", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2929, longitude: 36.7854,
    organizer: "Sunday Social Club", organizerVerified: true, priceFromMinor: 120000, currency: "KES", featured: true,
    tags: ["Soul", "Rooftop", "Sunset"], ticketTiers: [{ id: "tt_04", name: "Sunset Entry", priceMinor: 120000, currency: "KES", remaining: 96, description: "General admission" }],
  },
  {
    id: "evt_03", slug: "city-food-weekend", title: "City Food Weekend", category: "Food & Drink", mood: "Meet new people",
    summary: "Forty kitchens, one garden and the best new flavours in the city.", description: "Discover emerging chefs, bold Kenyan flavours and small-batch makers in a relaxed two-day garden market.",
    image: "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1600&q=85", startAt: "2026-10-03T11:00:00+03:00", endAt: "2026-10-04T21:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Jamhuri Gardens", address: "Ngong Road", area: "Woodley", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.3097, longitude: 36.7774,
    organizer: "Soko Experiences", organizerVerified: true, priceFromMinor: 50000, currency: "KES",
    tags: ["Food", "Market", "Family"], ticketTiers: [{ id: "tt_05", name: "Day Pass", priceMinor: 50000, currency: "KES", remaining: 440, description: "Single-day admission" }],
  },
  {
    id: "evt_04", slug: "laugh-nairobi", title: "Laugh Nairobi", category: "Comedy", mood: "Laugh out loud",
    summary: "Fresh voices, sharp stories and one unapologetically funny night.", description: "An original showcase of Kenya's rising fictional comedy talent in an intimate theatre setting.",
    image: "https://images.unsplash.com/photo-1527224857830-43a7acc85260?auto=format&fit=crop&w=1600&q=85", startAt: "2026-09-18T19:30:00+03:00", endAt: "2026-09-18T22:30:00+03:00", timezone: "Africa/Nairobi",
    venue: "City Stage", address: "Koinange Street", area: "Nairobi CBD", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2832, longitude: 36.8182,
    organizer: "Punchline KE", organizerVerified: true, priceFromMinor: 100000, currency: "KES", sellingFast: true,
    tags: ["Comedy", "18+"], ticketTiers: [{ id: "tt_06", name: "Regular", priceMinor: 100000, currency: "KES", remaining: 31, description: "Reserved theatre seating" }],
  },
  {
    id: "evt_05", slug: "coastline-festival", title: "Coastline Festival", category: "Festivals", mood: "Adventure",
    summary: "Two sunlit days of music, movement and coastal creativity.", description: "A fictional beachfront festival celebrating East African sound, fashion and food.",
    image: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1800&q=88", startAt: "2026-11-07T12:00:00+03:00", endAt: "2026-11-08T23:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Nyali Beach Grounds", address: "Links Road", area: "Nyali", city: "Mombasa", county: "Mombasa", country: "Kenya", latitude: -4.0416, longitude: 39.7131,
    organizer: "Coast Culture Lab", organizerVerified: true, priceFromMinor: 350000, currency: "KES", featured: true,
    tags: ["Festival", "Beach", "Music"], ticketTiers: [{ id: "tt_07", name: "Weekend Pass", priceMinor: 350000, currency: "KES", remaining: 820, description: "Both festival days" }],
  },
  {
    id: "evt_06", slug: "nairobi-tech-summit", title: "Nairobi Tech Summit", category: "Conferences", mood: "Meet new people",
    summary: "Builders, founders and designers shaping the next decade of African technology.", description: "A practical day of product talks, demos and small-group sessions for technology teams.",
    image: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=1600&q=85", startAt: "2026-10-22T08:00:00+03:00", endAt: "2026-10-22T18:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "KICC", address: "Harambee Avenue", area: "Nairobi CBD", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2884, longitude: 36.8233,
    organizer: "Build Africa Forum", organizerVerified: true, priceFromMinor: 450000, currency: "KES",
    tags: ["Technology", "Networking"], ticketTiers: [{ id: "tt_08", name: "Builder Pass", priceMinor: 450000, currency: "KES", remaining: 210, description: "Full summit access" }],
  },
];

const djangoApiUrl = process.env.DJANGO_ADMIN_API_URL ?? "http://127.0.0.1:8000/api";

interface DjangoEventResponse {
  items: EventListing[];
}

export async function getAvailableEvents(): Promise<EventListing[]> {
  try {
    const response = await fetch(`${djangoApiUrl}/events/`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) return events;
    const payload = (await response.json()) as DjangoEventResponse;
    if (!Array.isArray(payload.items)) return events;

    const merged = new Map<string, EventListing>(
      events.map((event) => [event.slug, { ...event, managedBy: "DEMO" as const }]),
    );
    for (const event of payload.items) merged.set(event.slug, { ...event, managedBy: "DJANGO" });
    return [...merged.values()];
  } catch {
    return events;
  }
}

export function getTopKenyaEvents(catalogue: EventListing[]) {
  return catalogue
    .filter((event) => typeof event.hotRank === "number")
    .sort((first, second) => (first.hotRank ?? 99) - (second.hotRank ?? 99));
}

export function getHotCounties(catalogue: EventListing[]) {
  const summary = new Map<string, { county: string; eventCount: number; nextStartAt: string }>();
  for (const event of catalogue.filter((item) => typeof item.hotRank === "number")) {
    const county = event.county?.trim();
    if (!county) continue;
    const current = summary.get(county);
    summary.set(county, {
      county,
      eventCount: (current?.eventCount ?? 0) + 1,
      nextStartAt: current && current.nextStartAt < event.startAt ? current.nextStartAt : event.startAt,
    });
  }
  return [...summary.values()].sort(
    (first, second) => second.eventCount - first.eventCount
      || first.nextStartAt.localeCompare(second.nextStartAt)
      || first.county.localeCompare(second.county),
  );
}

export function formatMoney(amountMinor: number, currency = "KES") {
  return new Intl.NumberFormat("en-KE", { style: "currency", currency, maximumFractionDigits: 0 }).format(amountMinor / 100);
}

export function getLocation(id?: string) {
  return locations.find((location) => location.id === id) ?? locations[0]!;
}

function distanceKm(aLat: number, aLng: number, bLat: number, bLng: number) {
  const radians = (degrees: number) => (degrees * Math.PI) / 180;
  const earthRadiusKm = 6371;
  const dLat = radians(bLat - aLat);
  const dLng = radians(bLng - aLng);
  const value = Math.sin(dLat / 2) ** 2 + Math.cos(radians(aLat)) * Math.cos(radians(bLat)) * Math.sin(dLng / 2) ** 2;
  return 2 * earthRadiusKm * Math.asin(Math.sqrt(value));
}

export function nearbyEvents(location: DiscoveryLocation, radius = 25, catalogue = events): NearbyEvent[] {
  return catalogue
    .map((event) => {
      const km = distanceKm(location.latitude, location.longitude, event.latitude, event.longitude);
      return { ...event, distanceKm: km, distanceLabel: `${km < 10 ? km.toFixed(1) : Math.round(km)} km from ${location.label.split(",")[0]}` };
    })
    .filter((event) => event.distanceKm <= radius)
    .sort((a, b) => Number(Boolean(b.featured)) - Number(Boolean(a.featured)) || a.distanceKm - b.distanceKm);
}

export async function getNearbyEvents(location: DiscoveryLocation, radius = 25) {
  return nearbyEvents(location, radius, await getAvailableEvents());
}

export async function getEvent(slug: string) {
  const demoEvent = events.find((event) => event.slug === slug);
  try {
    const response = await fetch(`${djangoApiUrl}/events/${encodeURIComponent(slug)}/`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (response.ok) return { ...((await response.json()) as EventListing), managedBy: "DJANGO" as const };
  } catch {
    // The customer application remains available while the optional CMS is offline.
  }
  return demoEvent;
}
