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
  { id: "kiambu-town", label: "Kiambu Town, Kiambu", city: "Kiambu", county: "Kiambu", country: "Kenya", countryCode: "KE", latitude: -1.1714, longitude: 36.8356, source: "MANUAL_SEARCH" },
  { id: "machakos-town", label: "Machakos Town, Machakos", city: "Machakos", county: "Machakos", country: "Kenya", countryCode: "KE", latitude: -1.5177, longitude: 37.2634, source: "MANUAL_SEARCH" },
];

export const events: EventListing[] = [
  {
    id: "nbo_20261023_born-to-be-lit", slug: "born-to-be-lit", title: "Born To Be Lit", category: "Music", mood: "Dance all night",
    summary: "An 18+ Nairobi night with DJs, rising artists and surprise performances.", description: "The ticket listing describes an all-night music event with DJs, rising artists and surprise performances. Confirm entry details and availability at the ticket source.",
    image: "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_admin_6a3ec4c64dfe46.04929671.jpg", startAt: "2026-10-23T20:00:00+03:00", endAt: "2026-10-24T02:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "HELSINKI ONGATA RONGAI", address: "Ongata Rongai", area: "Ongata Rongai", city: "Nairobi", county: "Kajiado", country: "Kenya", latitude: -1.396, longitude: 36.75,
    organizer: "Born To Be Lit", organizerVerified: false, priceFromMinor: 50000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["DJs", "Live music", "18+"], ticketTiers: [], managedBy: "DEMO", sourceName: "LipaTix", sourceUrl: "https://lipatix.com/events/born-to-be-lit", isExternalListing: true,
  },
  {
    id: "nbo_20261023_nyumbani-sessions", slug: "nyumbani-sessions-edition-2", title: "Nyumbani Sessions Edition 2", category: "Nightlife", mood: "Meet new people",
    summary: "A Nairobi nightlife session listed for Friday, 23 October.", description: "TikoHUB lists this event in Nairobi for 23 October 2026, with tickets from KES 600. The listing does not show a confirmed start time or precise venue; check the source before travelling.",
    image: "https://tikohub.com/api/media/9eaac4bf-d895-431b-9ac7-19aaf5617d30", startAt: "2026-10-23T20:00:00+03:00", endAt: "2026-10-24T02:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Venue details on ticket page", address: "Nairobi", area: "Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2864, longitude: 36.8172,
    organizer: "See TikoHUB listing", organizerVerified: false, priceFromMinor: 60000, currency: "KES", dateConfirmed: true, timeConfirmed: false, locationApproximate: true,
    tags: ["Nightlife"], ticketTiers: [], managedBy: "DEMO", sourceName: "TikoHUB", sourceUrl: "https://tikohub.com/events?city=Nairobi", isExternalListing: true,
  },
  {
    id: "nbo_20261024_cas-fifa-street", slug: "cas-fifa-street-2-0", title: "CAS FIFA STREET 2.0", category: "Sports", mood: "Play and compete",
    summary: "Football, fashion, food and live entertainment at St Mary's School.", description: "Organised by the IBDP CAS class of 2027 as a fundraiser, the event listing includes football, a BBQ, vendors and an after-party with live performances and DJs.",
    image: "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_admin_6acfcd46d79bb6.42792222.jpg", startAt: "2026-10-24T10:00:00+03:00", endAt: "2026-10-24T18:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "St Mary's School", address: "Off James Gichuru Road", area: "Lavington", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.270, longitude: 36.772,
    organizer: "IBDP CAS class of 2027", organizerVerified: false, priceFromMinor: 50000, currency: "KES", dateConfirmed: true, timeConfirmed: true,
    tags: ["Football", "Community", "Music"], ticketTiers: [], managedBy: "DEMO", sourceName: "LipaTix", sourceUrl: "https://www.lipatix.com/events/cas-fifa-street-2-0", isExternalListing: true,
  },
  {
    id: "nbo_20261031_afrohallows", slug: "afrohallows-goth-gala", title: "AfroHallows Goth Gala", category: "Nightlife", mood: "Costume night",
    summary: "A Halloween goth gala at D&A Liquor House in Lavington.", description: "The ticket listing names D&A Liquor House on James Gichuru Road and lists tickets from KES 900. Check the source for updated ticket availability and event details.",
    image: "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_236_7b742d859a1e25ee205f1f03ab9c9c20_1789323485.jpg", startAt: "2026-10-31T16:00:00+03:00", endAt: "2026-10-31T23:59:00+03:00", timezone: "Africa/Nairobi",
    venue: "D&A Liquor House", address: "909 James Gichuru Road", area: "Lavington", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2855, longitude: 36.773,
    organizer: "AfroHallows", organizerVerified: false, priceFromMinor: 90000, currency: "KES", dateConfirmed: true, timeConfirmed: true,
    tags: ["Halloween", "Goth"], ticketTiers: [], managedBy: "DEMO", sourceName: "LipaTix", sourceUrl: "https://lipatix.com/events/", isExternalListing: true,
  },
  {
    id: "nbo_20261107_rugby-africa-women", slug: "rugby-africa-womens-nairobi", title: "Rugby Africa Women", category: "Sports", mood: "Support local sport",
    summary: "Women's rugby in Nairobi on Saturday, 7 November.", description: "TikoHUB lists a Nairobi women's rugby event for 7 November 2026, with tickets from KES 500. Venue and kick-off time were not available in the listing checked; confirm them with the organiser before making plans.",
    image: "https://k24.digital/wp-content/uploads/2026/10/Kenya-Lionesses.png", startAt: "2026-11-07T12:00:00+03:00", endAt: "2026-11-07T18:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Venue details to be confirmed", address: "Nairobi", area: "Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2864, longitude: 36.8172,
    organizer: "See TikoHUB listing", organizerVerified: false, priceFromMinor: 50000, currency: "KES", dateConfirmed: true, timeConfirmed: false, locationApproximate: true,
    tags: ["Rugby", "Women's sport"], ticketTiers: [], managedBy: "DEMO", sourceName: "TikoHUB", sourceUrl: "https://tikohub.com/events?city=Nairobi", isExternalListing: true,
  },
  {
    id: "nbo_20261114_dancehall-fiesta", slug: "dancehall-fiesta", title: "Dancehall Fiesta", category: "Music", mood: "Dance all night",
    summary: "A dancehall night listed at Siron Rooftop for 14 November.", description: "LipaTix lists Dancehall Fiesta at Siron Rooftop on 14 November 2026. Its public listing shows a 2:00 AM start, so confirm the intended date and entry time with the organiser before going.",
    image: "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_229_da362dee4876f65e2c6a066553dabf66_1788300099.png", startAt: "2026-11-14T02:00:00+03:00", endAt: "2026-11-14T06:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Siron Rooftop", address: "Nairobi", area: "Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2864, longitude: 36.8172,
    organizer: "Boizfromthewest", organizerVerified: false, priceFromMinor: 60000, currency: "KES", dateConfirmed: true, timeConfirmed: false, locationApproximate: true,
    tags: ["Dancehall", "Nightlife"], ticketTiers: [], managedBy: "DEMO", sourceName: "LipaTix", sourceUrl: "https://lipatix.com/events/nairobi/", isExternalListing: true,
  },
  {
    id: "nbo_20261120_nairobi-sports-festival", slug: "nairobi-sports-festival-2026", title: "Nairobi Sports Festival", category: "Sports", mood: "Move and connect",
    summary: "A two-day, multi-sport community festival at the University of Nairobi.", description: "The inaugural festival is announced for 20–21 November at the University of Nairobi Sports Ground. The organisers list football, basketball, volleyball, athletics, cycling, tennis and family activities. Entry is free; check the official site for programme updates.",
    image: "https://www.sportanddev.org/sites/default/files/2026-09/nairobi-fest.png", startAt: "2026-11-20T09:00:00+03:00", endAt: "2026-11-21T18:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "University of Nairobi Sports Ground", address: "University Way", area: "Nairobi CBD", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.279, longitude: 36.816,
    organizer: "Tegla Loroupe Peace Foundation and Ferdinand Omanyala Foundation", organizerVerified: false, priceFromMinor: 0, currency: "KES", dateConfirmed: true, timeConfirmed: false,
    tags: ["Multi-sport", "Family", "Free entry"], ticketTiers: [], managedBy: "DEMO", sourceName: "Nairobi Sports Festival", sourceUrl: "https://nairobisportsfestival.org/", isExternalListing: true,
  },
  {
    id: "nbo_20261204_futurize-ai-health", slug: "futurize-ai-for-health-summit-2026", title: "Futurize AI for Health Summit 2026", category: "Conferences", mood: "Meet new people",
    summary: "Founders, investors and health leaders meet to explore AI and technology in African healthcare.", description: "Futurize describes a one-day summit with founder pitches, keynotes, panels and networking. The official event page lists 4 December 2026 at Antler East Africa, ABC Place, Nairobi, from 8:00 AM to 4:00 PM.",
    image: "https://images.squarespace-cdn.com/content/v1/601b8adcc98783132e680c23/1f381c49-6155-4afb-8771-822627fef7b2/AI%2BHealth%2BSummit%2BWebsite.png", startAt: "2026-12-04T08:00:00+03:00", endAt: "2026-12-04T16:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Antler East Africa, ABC Place", address: "Waiyaki Way", area: "Spring Valley", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2591, longitude: 36.786,
    organizer: "Futurize", organizerVerified: false, priceFromMinor: 0, priceAvailable: false, currency: "KES", dateConfirmed: true, timeConfirmed: true,
    tags: ["Health", "AI", "Technology"], ticketTiers: [], managedBy: "DEMO", sourceName: "Futurize", sourceUrl: "https://www.futurize.studio/summit", isExternalListing: true,
  },
  {
    id: "nbo_20261205_noxen", slug: "noxen", title: "Noxen", category: "Music", mood: "Dance all night",
    summary: "A Nairobi music and nightlife event with DJs and live performances.", description: "The organiser's ticket listing gives a 7:00 PM start on 5 December 2026 in Nairobi. A precise venue and current ticket availability should be confirmed with the organiser.",
    image: "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_205_1393488692367d38c141c56fd9f82e9f_1786946590.jpg", startAt: "2026-12-05T19:00:00+03:00", endAt: "2026-12-06T02:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Nairobi (venue to be confirmed)", address: "Nairobi", area: "Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2864, longitude: 36.8172,
    organizer: "Noxen", organizerVerified: false, priceFromMinor: 70000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Music", "Nightlife"], ticketTiers: [], managedBy: "DEMO", sourceName: "LipaTix", sourceUrl: "https://lipatix.com/events/noxen", isExternalListing: true,
  },
  {
    id: "nbo_20261211_ace-nation", slug: "ace-nation", title: "ACE nation", category: "Music", mood: "Dance all night",
    summary: "A Nairobi concert listing at Funcity Gardens, Utawala.", description: "The LipaTix Nairobi events page lists ACE nation for 11 December at 6:00 PM at Funcity Gardens, Utawala, from KES 1,000. Confirm ticket details at the source.",
    image: "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_admin_6a5e0927e9bd31.22027906.jpg", startAt: "2026-12-11T18:00:00+03:00", endAt: "2026-12-12T00:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Funcity Gardens", address: "Utawala", area: "Utawala", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.268, longitude: 36.97,
    organizer: "Acerumi", organizerVerified: false, priceFromMinor: 100000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Concert", "Music"], ticketTiers: [], managedBy: "DEMO", sourceName: "LipaTix", sourceUrl: "https://lipatix.com/events/", isExternalListing: true,
  },
  {
    id: "nbo_20261215_aurix-shutdown", slug: "aurix-shutdown", title: "AURIX SHUTDOWN", category: "Music", mood: "Dance all night",
    summary: "A Nairobi music event at The Event Space in Westlands.", description: "The LipaTix Nairobi events page lists AURIX SHUTDOWN on 15 December at 4:00 PM at The Event Space, Amee Arcade, Parklands Road, Westlands. Tickets are listed from KES 400.",
    image: "https://lipatix.com/organizer_dashboard/uploads/event_posters/event_218_6cbd0403f6a6fda961838d507b9bbd90_1787674669.png", startAt: "2026-12-15T16:00:00+03:00", endAt: "2026-12-15T23:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "The Event Space, Amee Arcade", address: "Parklands Road", area: "Westlands", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2623, longitude: 36.8021,
    organizer: "aurix.inc", organizerVerified: false, priceFromMinor: 40000, currency: "KES", dateConfirmed: true, timeConfirmed: true,
    tags: ["Music", "Nightlife"], ticketTiers: [], managedBy: "DEMO", sourceName: "LipaTix", sourceUrl: "https://lipatix.com/events/", isExternalListing: true,
  },
  {
    id: "kis_20261031_cabhouse-park-music-fest", slug: "cabhouse-park-music-fest-1", title: "CABHOUSE PARK MUSIC FEST I", category: "Music", mood: "Dance all night",
    summary: "A Kisii music festival featuring local performers, a pool party and more activities.", description: "The event listing names Rikanika Senior, Sparrow Ontondi, King Mose and Vicky Young, with opening acts, an early pool party and other activities. It lists an 11:00 AM start at Cabhouse Park and tickets from KES 700. The listing does not confirm an end time or precise map pin; check the ticket page before travelling.",
    image: "https://madfun-assets.s3.af-south-1.amazonaws.com/events/9b0485c8-2409-4722-b005-b9a925539b80/images/20260911_55d4d5c8c714.jpg", startAt: "2026-10-31T11:00:00+03:00", endAt: "2026-10-31T23:59:00+03:00", timezone: "Africa/Nairobi",
    venue: "Cabhouse Park", address: "Kisii County", area: "Kisii Town", city: "Kisii", county: "Kisii", country: "Kenya", latitude: -0.6817, longitude: 34.7667,
    organizer: "Cabhouse Park", organizerVerified: false, priceFromMinor: 70000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Festival", "Live music", "Pool party"], ticketTiers: [], managedBy: "DEMO", sourceName: "Madfun", sourceUrl: "https://new.madfun.com/events/cabhouse-park-2-anniversary", isExternalListing: true,
  },
  {
    id: "kis_20261231_gusii-fest-crossover", slug: "gusii-fest-crossover-new-year-2027", title: "Gusii Fest Crossover & New Year 2027", category: "Festivals", mood: "Celebrate together",
    summary: "A two-day Kisii celebration of live music, Gusii culture, food and games.", description: "The official Gusii Fest site lists the crossover on 31 December 2026 and the New Year event on 1 January 2027, both from 4:00 PM to 4:00 AM, in Kisii Town. It links to official tickets and says venue details and lineup updates are still to come. Check the organiser for venue confirmation and current ticket prices before travelling or booking.",
    image: "https://gusiifest.com/gusii-new-crossover.png", startAt: "2026-12-31T16:00:00+03:00", endAt: "2027-01-02T04:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Kisii Town (venue to be confirmed)", address: "Kisii Town", area: "Kisii Town", city: "Kisii", county: "Kisii", country: "Kenya", latitude: -0.6817, longitude: 34.7667,
    organizer: "Gusii Fest Entertainment", organizerVerified: false, priceFromMinor: 0, priceAvailable: false, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Festival", "Gusii culture", "Live music", "New Year"], ticketTiers: [], managedBy: "DEMO", sourceName: "Gusii Fest", sourceUrl: "https://gusiifest.com/", isExternalListing: true,
  },
  {
    id: "mac_20261021_machakos-university-hackfest", slug: "machakos-university-hackfest-2026", title: "Machakos University Hackfest 2026", category: "Conferences", mood: "Build something together",
    summary: "Three days of keynotes, breakout sessions, hacking and awards at Machakos University.", description: "The event page lists a three-day university hackfest from 21–23 October 2026, with keynotes and breakout sessions on day one, hacking on day two and awards on day three. Registration and remaining ticket availability are shown by the organizer.",
    image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1600&q=85", startAt: "2026-10-21T08:00:00+03:00", endAt: "2026-10-23T17:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Machakos University", address: "Along the Highway", area: "Machakos Town", city: "Machakos", county: "Machakos", country: "Kenya", latitude: -1.5177, longitude: 37.2634,
    organizer: "MKSU Hackfest", organizerVerified: false, priceFromMinor: 0, priceAvailable: false, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Technology", "Hackathon", "University"], ticketTiers: [], managedBy: "DEMO", sourceName: "Luma", sourceUrl: "https://luma.com/xkf0wx67", isExternalListing: true,
  },
  {
    id: "kiambu_20261031_stageyard-halloween", slug: "stageyard-halloween-kiambu-road-2026", title: "The Stageyard Halloween Edition", category: "Nightlife", mood: "Dance all night",
    summary: "A Halloween dance night with live artists at Cobblestone House on Kiambu Road.", description: "The ticket listing gives 31 October 2026, 7:00 PM–5:00 AM, and names Cobblestone House on Kiambu Road. The venue is near the county boundary, so confirm the exact location and ticket availability with the organizer before travelling.",
    image: "https://images.unsplash.com/photo-1506157786151-b8491531f063?auto=format&fit=crop&w=1600&q=85", startAt: "2026-10-31T19:00:00+03:00", endAt: "2026-11-01T05:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Cobblestone House", address: "Kiambu Road", area: "Kiambu Road", city: "Kiambu", county: "Kiambu", country: "Kenya", latitude: -1.214, longitude: 36.838,
    organizer: "The Stageyard", organizerVerified: false, priceFromMinor: 100000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Halloween", "Live music", "Nightlife"], ticketTiers: [], managedBy: "DEMO", sourceName: "Looped", sourceUrl: "https://looped.co.ke/unified-event/the-stageyard-halloween-edition-33172f1d", isExternalListing: true,
  },
  {
    id: "nbo_20261031_halloween-candy-wonderland", slug: "halloween-candy-wonderland-nairobi-2026", title: "Halloween Candy Wonderland", category: "Family", mood: "Costume night",
    summary: "A family-friendly Halloween tournament and activities in Gigiri.", description: "The event listing gives Saturday, 31 October 2026, 2:00–5:00 PM on Gigiri Road in Nairobi. Wonderland Access tickets are listed at KES 2,000. Check the ticket page for current availability and event details.",
    image: "https://mookh-v3-public.lon1.digitaloceanspaces.com/events/event-featured-1790573458530-04utj.jpeg", startAt: "2026-10-31T14:00:00+03:00", endAt: "2026-10-31T17:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Gigiri Road", address: "Gigiri Road", area: "Gigiri", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.235, longitude: 36.805,
    organizer: "Halloween Padel Tournament", organizerVerified: false, priceFromMinor: 200000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Halloween", "Family", "Sports"], ticketTiers: [], managedBy: "DEMO", sourceName: "MOOKH", sourceUrl: "https://mookh.com/halloweencandywonderland/", isExternalListing: true,
  },
  {
    id: "nbo_20261031_halloween-fright-night", slug: "halloween-fright-night-party-2026", title: "Halloween Fright Night Party", category: "Festivals", mood: "Costume night",
    summary: "A Halloween day party and evening celebration at Village Market.", description: "Ticketsasa lists the event at Village Market on Saturday, 31 October 2026, from 2:00 PM to 11:59 PM. Advance tickets are KES 1,500, group tickets are KES 4,200 for three or KES 7,000 for five, and gate entry is listed at KES 2,000. Verify current availability at the ticket source.",
    image: "https://admin.ticketsasa.com/storage/events/September2026/Asn03ZMqUD-1789394180.jpg", startAt: "2026-10-31T14:00:00+03:00", endAt: "2026-10-31T23:59:00+03:00", timezone: "Africa/Nairobi",
    venue: "Village Market", address: "Limuru Road", area: "Gigiri", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.208, longitude: 36.804,
    organizer: "HAMECO LIMITED EVENTS", organizerVerified: false, priceFromMinor: 150000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Halloween", "Family", "Nightlife"], ticketTiers: [], managedBy: "DEMO", sourceName: "Ticketsasa", sourceUrl: "https://www.ticketsasa.com/events/halloween-fright-night-party", isExternalListing: true,
  },
  {
    id: "nbo_20261031_halloween-lan-party", slug: "halloween-lan-party-nairobi-2026", title: "Halloween LAN Party", category: "Experiences", mood: "Play and compete",
    summary: "A Halloween gaming day with mini tournaments and PC-building sessions.", description: "Looped lists this event on 31 October 2026, 10:00 AM–10:00 PM, at Kylin eSports Arena in Zarafa Suites. Early Bird tickets are listed at KES 1,000. Check the ticket source for current availability.",
    image: "https://zziqdstqvcgxkdotnwsd.supabase.co/storage/v1/object/public/event-images/halloween-lan-party-1b7fe7f6/1790791855_uploaded-image-517a9154", startAt: "2026-10-31T10:00:00+03:00", endAt: "2026-10-31T22:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Kylin eSports Arena, Zarafa Suites", address: "Zarafa Suites", area: "Nairobi", city: "Nairobi", county: "Nairobi", country: "Kenya", latitude: -1.2864, longitude: 36.8172,
    organizer: "CZY eSports x Kylin eSports", organizerVerified: false, priceFromMinor: 100000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Halloween", "Gaming", "Esports"], ticketTiers: [], managedBy: "DEMO", sourceName: "Looped", sourceUrl: "https://looped.co.ke/unified-event/halloween-lan-party-1b7fe7f6", isExternalListing: true,
  },
  {
    id: "mba_20261031_halloween-party", slug: "halloween-party-mombasa-2026", title: "Halloween Party", category: "Music", mood: "Costume night", featured: true,
    summary: "A Halloween celebration with music, themed décor and costume fun in Mombasa.", description: "Mombasa Events lists this party for Saturday, 31 October 2026, at 2:00 PM in Mombasa. Advance tickets are listed at KES 1,050. The listing does not confirm an end time or precise venue; check the ticket page before travelling.",
    image: "https://images.unsplash.com/photo-1506157786151-b8491531f063?auto=format&fit=crop&w=1600&q=85", startAt: "2026-10-31T14:00:00+03:00", endAt: "2026-10-31T23:59:00+03:00", timezone: "Africa/Nairobi",
    venue: "Mombasa (venue to be confirmed)", address: "Mombasa", area: "Mombasa", city: "Mombasa", county: "Mombasa", country: "Kenya", latitude: -4.0435, longitude: 39.6682,
    organizer: "Mombasa Events", organizerVerified: false, priceFromMinor: 105000, currency: "KES", dateConfirmed: true, timeConfirmed: false, locationApproximate: true,
    tags: ["Halloween", "Music", "Costumes"], ticketTiers: [], managedBy: "DEMO", sourceName: "SoldOutAfrica", sourceUrl: "https://soldoutafrica.com/halloween-party", isExternalListing: true,
  },
  {
    id: "mba_20261031_haunted-fest", slug: "haunted-fest-halloween-mombasa-2026", title: "Haunted Fest Halloween Edition", category: "Festivals", mood: "Costume night",
    summary: "A full-day Halloween experience with daytime games and evening activities.", description: "Tufikee lists the event for 31 October 2026 from 11:00 AM at North Coast Beach Hotel in Mombasa. Ticket prices start at KES 1,000 for Early Bird, with Regular at KES 1,500, Gate at KES 2,000, and VIP at KES 3,000. Confirm availability and the programme with the ticket source.",
    image: "https://www.tufikee.com/_next/image?q=75&url=https%3A%2F%2Fhustle.imgix.net%2F41630%252Fproduct%252Fde43a1ef-8de8-4a88-be8b-b2ea639f38ee.png%3Fw%3D1200%26h%3D630%26fit%3Dcrop&w=3840", startAt: "2026-10-31T11:00:00+03:00", endAt: "2026-10-31T23:59:00+03:00", timezone: "Africa/Nairobi",
    venue: "North Coast Beach Hotel", address: "North Coast", area: "Bamburi", city: "Mombasa", county: "Mombasa", country: "Kenya", latitude: -3.998, longitude: 39.735,
    organizer: "Tufikee Vendor", organizerVerified: false, priceFromMinor: 100000, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Halloween", "Family", "Festival"], ticketTiers: [], managedBy: "DEMO", sourceName: "Tufikee", sourceUrl: "https://www.tufikee.com/event/hs-haunted-fest-halloween-edition-dff0c562", isExternalListing: true,
  },
  {
    id: "nak_20261106_kenya-music-cultural-festival", slug: "kenya-music-cultural-festival-nakuru-2026", title: "Kenya Music & Cultural Festival", category: "Festivals", mood: "Celebrate together",
    summary: "A two-day music and culture festival at Shaabab Social Hall, Nakuru.", description: "Nakuru County's public events calendar lists the festival for 6–7 November 2026 at Shaabab Social Hall. Confirm the programme and entry details with the county before travelling.",
    image: "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?auto=format&fit=crop&w=1600&q=85", startAt: "2026-11-06T08:00:00+03:00", endAt: "2026-11-07T16:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Shaabab Social Hall", address: "Nakuru Town", area: "Nakuru Town", city: "Nakuru", county: "Nakuru", country: "Kenya", latitude: -0.3031, longitude: 36.08,
    organizer: "Nakuru County Government", organizerVerified: false, priceFromMinor: 0, priceAvailable: false, currency: "KES", dateConfirmed: true, timeConfirmed: true,
    tags: ["Music", "Culture", "Festival"], ticketTiers: [], managedBy: "DEMO", sourceName: "Nakuru County", sourceUrl: "https://www.nakuru.go.ke/event/", isExternalListing: true,
  },
  {
    id: "mba_20261113_coast-worship-praise-night", slug: "coast-worship-praise-night-mombasa-2026", title: "Coast Worship & Praise Night", category: "Music", mood: "Sing together",
    summary: "An evening worship and praise gathering at Mombasa Showground.", description: "AskGen's November 2026 event calendar lists this gathering at Mombasa Showground on 13 November at 6:00 PM. Check with the organizer for the latest programme and entry details.",
    image: "https://images.unsplash.com/photo-1501612780327-45045538702b?auto=format&fit=crop&w=1600&q=85", startAt: "2026-11-13T18:00:00+03:00", endAt: "2026-11-13T22:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Mombasa Showground", address: "Mombasa", area: "Mombasa", city: "Mombasa", county: "Mombasa", country: "Kenya", latitude: -4.0435, longitude: 39.6682,
    organizer: "See AskGen event calendar", organizerVerified: false, priceFromMinor: 0, priceAvailable: false, currency: "KES", dateConfirmed: true, timeConfirmed: true, locationApproximate: true,
    tags: ["Worship", "Live music", "Community"], ticketTiers: [], managedBy: "DEMO", sourceName: "AskGen", sourceUrl: "https://askgen.co.ke/calendar?month=11&year=2026", isExternalListing: true,
  },
  {
    id: "kis_20261128_nam-2026", slug: "nam-2026-kisumu", title: "NAM 2026 · Made Again", category: "Festivals", mood: "Date night",
    summary: "A sustainable fashion runway and market celebrating independent Lake Region designers.", description: "The official event site lists NAM 2026 for 28 November 2026, 2:00–10:00 PM, at Mirock Gardens in Milimani, Kisumu. Tickets are available through the event's official page; check current ticket tiers before booking.",
    image: "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=1600&q=85", startAt: "2026-11-28T14:00:00+03:00", endAt: "2026-11-28T22:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Mirock Gardens", address: "Milimani", area: "Milimani", city: "Kisumu", county: "Kisumu", country: "Kenya", latitude: -0.1022, longitude: 34.7617,
    organizer: "SHE Limited", organizerVerified: false, priceFromMinor: 0, priceAvailable: false, currency: "KES", dateConfirmed: true, timeConfirmed: true,
    tags: ["Fashion", "Sustainable design", "Market"], ticketTiers: [], managedBy: "DEMO", sourceName: "NAM 2026", sourceUrl: "https://nam.co.ke/", isExternalListing: true,
  },
  {
    id: "kil_20261023_kilifi-creek-festival", slug: "kilifi-creek-festival-2026", title: "Kilifi Creek Festival", category: "Festivals", mood: "Chill weekend",
    summary: "An artist-led film, arts and culture festival along Kilifi Creek, 23–31 October.", description: "The official festival site describes the 2026 edition as returning 23–31 October along Kilifi Creek. Individual programme times and ticket availability may vary; check the festival site for current details.",
    image: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=1600&q=85", startAt: "2026-10-23T10:00:00+03:00", endAt: "2026-10-31T22:00:00+03:00", timezone: "Africa/Nairobi",
    venue: "Kilifi Creek", address: "Kilifi County", area: "Kilifi", city: "Kilifi", county: "Kilifi", country: "Kenya", latitude: -3.6305, longitude: 39.8499,
    organizer: "Kilifi Creek Festival", organizerVerified: false, priceFromMinor: 0, priceAvailable: false, currency: "KES", dateConfirmed: true, timeConfirmed: false, locationApproximate: true,
    tags: ["Film", "Arts", "Culture"], ticketTiers: [], managedBy: "DEMO", sourceName: "Kilifi Creek Festival", sourceUrl: "https://kilificreekfestival.com/", isExternalListing: true,
  },
];

const djangoApiUrl = process.env.DJANGO_ADMIN_API_URL;

interface DjangoEventResponse {
  items: EventListing[];
}

export async function getAvailableEvents(): Promise<EventListing[]> {
  if (!djangoApiUrl) return upcomingEvents(events);
  try {
    const response = await fetch(`${djangoApiUrl}/events/`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) return upcomingEvents(events);
    const payload = (await response.json()) as DjangoEventResponse;
    if (!Array.isArray(payload.items)) return upcomingEvents(events);

    const merged = new Map<string, EventListing>(
      events.map((event) => [event.slug, { ...event, managedBy: "DEMO" as const }]),
    );
    for (const event of payload.items) {
      const demoEvent = merged.get(event.slug);
      merged.set(event.slug, {
        ...demoEvent,
        ...event,
        managedBy: "DJANGO",
        sourceName: event.sourceName || demoEvent?.sourceName || "",
        sourceUrl: event.sourceUrl || demoEvent?.sourceUrl || "",
        isExternalListing: demoEvent?.isExternalListing ?? event.isExternalListing ?? false,
      });
    }
    return upcomingEvents([...merged.values()]);
  } catch {
    return upcomingEvents(events);
  }
}

export function upcomingEvents(catalogue: EventListing[], now = Date.now()) {
  return catalogue
    .filter((event) => Date.parse(event.endAt) > now)
    .sort((first, second) => first.startAt.localeCompare(second.startAt));
}

export function getTopKenyaEvents(catalogue: EventListing[]) {
  return upcomingEvents(catalogue).filter((event) => event.country.toLowerCase() === "kenya").sort((first, second) =>
    (first.hotRank ?? Number.MAX_SAFE_INTEGER) - (second.hotRank ?? Number.MAX_SAFE_INTEGER)
    || first.startAt.localeCompare(second.startAt),
  );
}

export function getHotCounties(catalogue: EventListing[]) {
  const summary = new Map<string, { county: string; eventCount: number; nextStartAt: string }>();
  for (const event of upcomingEvents(catalogue)) {
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
  const demoEvent = upcomingEvents(events).find((event) => event.slug === slug);
  if (!djangoApiUrl) return demoEvent;
  try {
    const response = await fetch(`${djangoApiUrl}/events/${encodeURIComponent(slug)}/`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (response.ok) {
      const apiEvent = (await response.json()) as EventListing;
      const publishedEvent = {
        ...demoEvent,
        ...apiEvent,
        managedBy: "DJANGO" as const,
        sourceName: apiEvent.sourceName || demoEvent?.sourceName || "",
        sourceUrl: apiEvent.sourceUrl || demoEvent?.sourceUrl || "",
        isExternalListing: demoEvent?.isExternalListing ?? apiEvent.isExternalListing ?? false,
      };
      return Date.parse(publishedEvent.endAt) > Date.now() ? publishedEvent : undefined;
    }
  } catch {
    // The customer application remains available while the optional CMS is offline.
  }
  return demoEvent;
}

