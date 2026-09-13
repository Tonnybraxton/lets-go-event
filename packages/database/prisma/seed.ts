import { PrismaClient, EventStatus, UserRole } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const organizer = await prisma.user.upsert({ where: { email: "organizer.demo@letsgo.local" }, update: {}, create: { email: "organizer.demo@letsgo.local", displayName: "Amani Kamau", role: UserRole.ORGANIZER_OWNER, emailVerified: new Date() } });
  const organization = await prisma.organization.upsert({ where: { slug: "neon-nairobi-collective" }, update: {}, create: { slug: "neon-nairobi-collective", name: "Neon Nairobi Collective", description: "A fictional experience studio for local development.", verifiedAt: new Date(), members: { create: { userId: organizer.id, role: UserRole.ORGANIZER_OWNER } } } });
  const venue = await prisma.venue.upsert({ where: { slug: "alchemist-garden-demo" }, update: {}, create: { slug: "alchemist-garden-demo", name: "The Alchemist Garden (Demo)", address: "Parklands Road", area: "Westlands", city: "Nairobi", country: "Kenya", countryCode: "KE", latitude: -1.2635, longitude: 36.8047, timezone: "Africa/Nairobi" } });
  await prisma.event.upsert({ where: { slug: "nairobi-after-dark" }, update: {}, create: { organizationId: organization.id, venueId: venue.id, slug: "nairobi-after-dark", title: "Nairobi After Dark", summary: "A one-night collision of Afro-house, art and electric city energy.", description: "A fictional demo event used to validate the Let's Go Event commerce flow.", category: "Nightlife", status: EventStatus.PUBLISHED, startAt: new Date("2026-10-17T18:00:00+03:00"), endAt: new Date("2026-10-18T03:00:00+03:00"), timezone: "Africa/Nairobi", publishedAt: new Date(), ticketTypes: { create: [{ name: "First Light", description: "Entry before 9 PM", priceMinor: 180000, currency: "KES", capacity: 200 }, { name: "Night Pass", description: "General admission", priceMinor: 250000, currency: "KES", capacity: 600 }] } } });
}

main().finally(async () => prisma.$disconnect());
