# Radar geography

Radar includes all 47 Kenyan counties and resolves common cities to counties before review. Unknown locations remain unresolved and reduce the quality score. SQLite development stores decimal coordinates. Production can enable the existing PostGIS container and extend venue resolution with spatial points and an approved geocoder. Geocoding must be cached, rate-limited, attributed, and reviewed before use.
