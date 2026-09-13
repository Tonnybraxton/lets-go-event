KENYA_COUNTIES = (
    "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet", "Embu", "Garissa",
    "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho", "Kiambu", "Kilifi",
    "Kirinyaga", "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia", "Lamu", "Machakos",
    "Makueni", "Mandera", "Marsabit", "Meru", "Migori", "Mombasa", "Murang'a", "Nairobi",
    "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri", "Samburu", "Siaya",
    "Taita-Taveta", "Tana River", "Tharaka-Nithi", "Trans Nzoia", "Turkana", "Uasin Gishu",
    "Vihiga", "Wajir", "West Pokot",
)

CITY_COUNTIES = {
    "nairobi": "Nairobi", "mombasa": "Mombasa", "kisumu": "Kisumu", "nakuru": "Nakuru",
    "eldoret": "Uasin Gishu", "naivasha": "Nakuru", "nanyuki": "Laikipia",
    "kakamega": "Kakamega", "malindi": "Kilifi", "kilifi": "Kilifi", "thika": "Kiambu",
    "kisii": "Kisii", "migori": "Migori", "bomet": "Bomet", "nyeri": "Nyeri",
    "kitui": "Kitui", "molo": "Nakuru", "kisaju": "Kajiado", "kiserian": "Kajiado",
}


def resolve_county(city: str = "", county: str = "", address: str = "") -> str:
    for candidate in KENYA_COUNTIES:
        if candidate.casefold() == county.strip().casefold():
            return candidate
    haystack = f"{city} {address}".casefold()
    for key, value in CITY_COUNTIES.items():
        if key in haystack:
            return value
    return ""
