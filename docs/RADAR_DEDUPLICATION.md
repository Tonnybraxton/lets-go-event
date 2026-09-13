# Radar deduplication

Radar fingerprints normalized title, local event date, venue, and city. It then compares new observations with canonical events in a ±1-day window using token-set title and venue similarity. Scores at or above 72 create a `DuplicateCandidate`; they do not silently merge records. Administrators confirm or dismiss candidates and both source observations remain preserved.
