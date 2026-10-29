# Brand Tag Controlled Vocabulary

The `brand_inspiration` entries in `index.json` are tagged along multiple dimensions using the controlled vocabulary below. **When adding or modifying brand tags, pick terms from this table** to avoid near-synonym splitting (e.g. "restrained / minimal / minimalist") that causes search misses.

The vocabulary was induced from the real content of 89 brand DESIGN.md files and aligned with the dimension design of `deck-templates`' `template.json`.

---

## `industry` (array, ≥1)
AI · Developer tools · Productivity/collaboration · Finance/payments · Automotive · Luxury · Social/messaging · E-commerce/retail ·
Media/publishing · Infrastructure/enterprise · Consumer electronics/tech · Content/creative tools · Mobility/local life · Telecom · Documents/education

## `product_type` (array, ≥1)
SaaS · Official site/marketing page · Developer platform · Consumer app · Content platform · E-commerce/transactions · Brand showcase page ·
Product launch page · Documentation site · Portfolio/personal

## `mood` (array, ≥2)
Minimalist · Restrained · Precision/engineered · Technical · Luxurious · Dramatic · Dark-native · Image-first · Editorial/magazine ·
Warm · Friendly/approachable · Energetic/bright · Content-first · Corporate/trustworthy · Gradient atmosphere · Illustration-rich · Retro/playful · Futuristic/sci-fi

Notes (near-synonym distinctions kept deliberately unmerged):
- `Minimalist` = structural subtraction; `Restrained` = quiet, not loud. They can coexist or appear alone.
- `Precision/engineered` = precisely calibrated visuals; `Technical` = code/developer temperament.

## Single-value dimensions
- `formality`: high / medium / low
- `density`: high / medium / low
- `scheme`: light / dark / both
- `era`: retro / modern / futuristic

## Natural-language fields
- `best_for`: the scenarios it fits best (one sentence)
- `avoid_for`: the scenarios it does not fit (one sentence)

---

## Retrieval usage
Filter `index.json` by the required dimensions → lock in candidate brands → read only the matched brand's `DESIGN.md` for full tokens and rules.
Array dimensions support many-to-many: one brand can match multiple values in the same dimension (e.g. Stripe belongs to both finance/payments and developer tools).
