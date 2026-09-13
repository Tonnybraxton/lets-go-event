# Radar compliance and security

Radar crawls public event metadata only. It must not collect attendee lists, private accounts, customer contact details, payment data, or authenticated content. Sources require an explicit compliance status and content-usage mode. Robots policy, contractual restrictions, honest identification, conservative delays, and source-specific limits must be respected.

The URL validator rejects non-HTTP schemes, localhost, private IP ranges, link-local addresses, and reserved networks. Production fetchers must validate every redirect target as well. Radar does not implement CAPTCHA solving, anti-bot bypasses, stealth fingerprinting, or proxy evasion.
