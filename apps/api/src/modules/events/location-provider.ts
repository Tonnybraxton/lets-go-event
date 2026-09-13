import type { DiscoveryLocation } from "@letsgo/types";

export interface LocationProvider {
  searchLocations(query: string): Promise<DiscoveryLocation[]>;
  geocode(placeId: string): Promise<DiscoveryLocation | null>;
  reverseGeocode(latitude: number, longitude: number): Promise<DiscoveryLocation | null>;
}

export const LOCATION_PROVIDER = Symbol("LOCATION_PROVIDER");

export class DemoLocationProvider implements LocationProvider {
  private readonly places: DiscoveryLocation[] = [
    { id: "westlands-nairobi", label: "Westlands, Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.2676, longitude: 36.8108, source: "MANUAL_SEARCH" },
    { id: "kilimani-nairobi", label: "Kilimani, Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.2921, longitude: 36.7836, source: "MANUAL_SEARCH" },
    { id: "nairobi-cbd", label: "Nairobi CBD, Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.2864, longitude: 36.8172, source: "MANUAL_SEARCH" },
    { id: "nyali-mombasa", label: "Nyali, Mombasa", city: "Mombasa", county: "Mombasa", country: "Kenya", countryCode: "KE", latitude: -4.0435, longitude: 39.7115, source: "MANUAL_SEARCH" },
  ];
  async searchLocations(query: string) { return this.places.filter((place) => place.label.toLowerCase().includes(query.toLowerCase())).slice(0, 8); }
  async geocode(placeId: string) { return this.places.find((place) => place.id === placeId) ?? null; }
  async reverseGeocode() { return null; }
}
