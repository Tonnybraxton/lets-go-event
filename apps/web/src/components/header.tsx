import Link from "next/link";
import { Compass, MapPin, Search, Ticket, UserRound } from "lucide-react";

export function Header() {
  return <>
    <header className="site-header">
      <div className="shell nav-row">
        <Link href="/" className="brand-mark" aria-label="Let's Go Event home"><span className="brand-dot">L</span> LET&apos;S GO</Link>
        <nav className="nav-links" aria-label="Main navigation"><Link href="/explore">Discover</Link><Link href="/explore?category=Music">Music</Link><Link href="/explore?category=Nightlife">Nightlife</Link><Link href="/explore?category=Festivals">Festivals</Link></nav>
        <div className="nav-actions">
          <Link className="location-pill" href="/explore?location=westlands-nairobi&radius=25"><MapPin size={14} /> Westlands, Nairobi</Link>
          <Link className="button button-ghost" href="/organizer/events/new">Create event</Link>
        </div>
      </div>
    </header>
    <nav className="mobile-nav" aria-label="Mobile navigation">
      <Link href="/"><Compass size={20}/><span>Home</span></Link><Link href="/explore"><Search size={20}/><span>Explore</span></Link><Link href="/explore"><MapPin size={20}/><span>Nearby</span></Link><Link href="/account/tickets"><Ticket size={20}/><span>Tickets</span></Link><Link href="/account"><UserRound size={20}/><span>Profile</span></Link>
    </nav>
  </>;
}
