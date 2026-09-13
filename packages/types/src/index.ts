export type DiscoveryLocationSource = "MANUAL_SEARCH" | "SAVED_LOCATION" | "OPTIONAL_GPS";

export interface DiscoveryLocation {
  id: string;
  label: string;
  city: string;
  county: string;
  country: string;
  countryCode: string;
  latitude: number;
  longitude: number;
  source: DiscoveryLocationSource;
}

export interface TicketTier {
  id: string;
  name: string;
  priceMinor: number;
  currency: string;
  remaining: number;
  description: string;
}

export interface EventListing {
  id: string;
  slug: string;
  title: string;
  summary: string;
  description: string;
  category: string;
  mood: string;
  image: string;
  startAt: string;
  endAt: string;
  timezone: string;
  venue: string;
  address: string;
  area: string;
  city: string;
  county?: string;
  country: string;
  latitude: number;
  longitude: number;
  organizer: string;
  organizerVerified: boolean;
  priceFromMinor: number;
  priceAvailable?: boolean;
  currency: string;
  sellingFast?: boolean;
  featured?: boolean;
  hotRank?: number | null;
  dateConfirmed?: boolean;
  timeConfirmed?: boolean;
  locationApproximate?: boolean;
  ticketTiers: TicketTier[];
  tags: string[];
  managedBy?: "DEMO" | "DJANGO";
  sourceName?: string;
  sourceUrl?: string;
  isExternalListing?: boolean;
}

export interface NearbyEvent extends EventListing {
  distanceKm: number;
  distanceLabel: string;
}
