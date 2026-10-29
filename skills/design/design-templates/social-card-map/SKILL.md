---
name: social-card-map
description: Map / itinerary / route-led social cards — route + 3 stops / neighborhood map + recommendation labels / one-day itinerary + simplified path / place card + mini map + travel notes / two-district two-route comparison. Geography must be aggressively simplified: label only necessary places, give a clear path hierarchy, and pair with city/date/duration/walking-driving context. Triggers: "make a travel route card / itinerary map card / neighborhood map card / weekend walk route / city guide". NOT fabricating real map data, NOT map-as-background decoration.
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: pattern.html
source_priority: skill-first
triggers:
  - "make a travel route card"
  - "itinerary map card"
  - "neighborhood map card"
  - "weekend walk route"
  - "city guide card"
  - "map check-in card"
related_patterns: social-card-editorial
---

# Social Card Map / Travel Template

Use when location, route, itinerary, distance, neighborhood, or place relationship is central to the card.

## Core Rule

A map card must clarify spatial relationships. Do not add a map shape only as decoration.

## Structure Options

- route map + 3 stops
- neighborhood map + recommendation labels
- day itinerary + simple path
- place card + mini map + travel note
- comparison: two areas / two routes

## Must Do

- Simplify geography aggressively.
- Label only necessary places.
- Use a clear route/path hierarchy.
- Include context: city, date, duration, walking/driving/transit if relevant.

## Avoid

- Map details too dense for phone viewing.
- Fake exact map data when none is provided.
- Decorative map backgrounds unrelated to content.

## Pattern Source Rule

Read this `SKILL.md` first. Do **not** read `pattern.html` by default.

Read `pattern.html` only when you need concrete layout rhythm, spatial relationships, or interaction/annotation behavior that this markdown cannot fully specify. When read, extract patterns only; do not copy DOM, CSS classes, exact spacing, placeholder copy, or styling wholesale.
