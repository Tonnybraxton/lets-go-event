import { z } from "zod";

export const discoverySearchSchema = z.object({
  location: z.string().trim().min(2).max(120),
  radius: z.coerce.number().min(2).max(100).default(25),
  category: z.string().trim().max(60).optional(),
  date: z.enum(["any", "today", "weekend", "week"]).default("any"),
});

export const organizerEventSchema = z.object({
  title: z.string().trim().min(5).max(120),
  summary: z.string().trim().min(20).max(240),
  category: z.string().trim().min(2).max(60),
  venue: z.string().trim().min(2).max(120),
  address: z.string().trim().min(5).max(180),
  city: z.string().trim().min(2).max(80),
  startsAt: z.iso.datetime(),
  timezone: z.string().trim().min(3).max(80),
  ticketName: z.string().trim().min(2).max(60),
  ticketPriceMinor: z.coerce.number().int().min(0),
  ticketQuantity: z.coerce.number().int().min(1).max(100_000),
});

export type DiscoverySearchInput = z.infer<typeof discoverySearchSchema>;
export type OrganizerEventInput = z.infer<typeof organizerEventSchema>;
