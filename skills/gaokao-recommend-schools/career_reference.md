# Major & Career-Direction Reference (for agent reference during analysis)

This document is a **reference knowledge base**; it does not replace personalized
judgment. The agent should combine the student's profile with the real volunteer data
in `parsed.json` to produce `analysis.json`.

---

## Analysis dimensions (the agent must consider)

| Dimension | Description |
|------|------|
| Subject selection vs. major requirements | Check the `claim` field (e.g. "physics and chemistry") and avoid recommending majors whose subject requirements are not met |
| Per-subject scores | Strong math/physics → engineering, computer science, electronic information; strong biology/chemistry → medicine, life sciences; strong Chinese/English → economics & management, law, humanities |
| Interests & hobbies | Map them to concrete major classes rather than staying vague |
| Career direction | Distinguish the "primary direction" from "backup directions" and explain why |
| Family situation | Willingness to pursue further study, financial capacity, regional preferences, acceptance of long training paths (e.g. medicine) |
| City opportunities | Industries and internship/employment resources of the preferred cities |
| Admission probability | Combine with the reach/match/safety tiers to explain why a school/major is flagged as recommended |

**Hard constraint**: the `university_name`, `university_code`, `major_name`, and
`major_code` in `recommended_majors` / `recommended_schools` must come from `parsed.json`,
otherwise the HTML cannot be tagged as recommended.

---

## Common major directions & career outcomes

### 🧑‍💻 Information & hard tech

| Major class | Typical major-name keywords | Career outcomes | Training characteristics |
|----------|------------------|----------|----------|
| Computer science | computer science, software, artificial intelligence, big data | Internet, AI, fintech, gaming | Broad job market, fierce competition, requires continuous learning |
| Electronic information | electronic information, communications, microelectronics, integrated circuits | Chips, communications equipment, consumer electronics | Core of hard tech; high math/physics demands |
| Automation | automation, robotics, control | Smart manufacturing, autonomous driving, industrial software | Interdisciplinary, solid engineering foundation |

**Suited for students** who: have outstanding math/physics scores, are interested in programming/technology, and whose family supports further study or accepts intensive learning.

---

### 🩺 Medicine & health

| Major class | Typical major-name keywords | Career outcomes | Training characteristics |
|----------|------------------|----------|----------|
| Clinical medicine | clinical medicine, stomatology | Top-tier (Grade 3A) hospitals, primary care, research | Long programs (5+ years); graduate school / standardized residency training common |
| Basic / preventive medicine | basic medicine, preventive medicine, public health | Disease control, research, public-health administration | Research- and management-oriented |
| Pharmacy / nursing | pharmacy, nursing | Pharmaceutical companies, hospital nursing positions | Relatively stable employment |

**Suited for students** who: have good biology/chemistry, can accept a long training cycle, whose family supports graduate study, and who value career stability.

---

### ⚙️ Engineering & advanced manufacturing

| Major class | Typical major-name keywords | Career outcomes | Training characteristics |
|----------|------------------|----------|----------|
| Mechanical / vehicles | mechanical engineering, vehicles, intelligent manufacturing | Automotive, equipment manufacturing, new energy | Stable traditional-engineering foundation |
| Aerospace | aerospace, aircraft | Defense industry, space program, civil aviation | Concentrated in a few universities; the "Seven Sons of National Defense" are worth attention |
| Electrical / energy | electrical engineering, energy & power, new energy | Power grid, new energy, power equipment | Many opportunities at state-owned / central enterprises |
| Materials / civil engineering | materials, civil engineering, architecture | Infrastructure, new materials, real-estate-related | Highly cyclical industries; factor in the city |

**Suited for students** who: have solid physics, prefer real-economy industries, and can accept an engineer's growth path.

---

### 📊 Economics, finance & management

| Major class | Typical major-name keywords | Career outcomes | Training characteristics |
|----------|------------------|----------|----------|
| Finance / economics | finance, economics, public finance | Banking, securities, consulting, corporate finance | Prestigious universities and internship resources matter |
| Business administration | business administration, marketing, accounting | Corporate management, auditing, operations | Broad-entry major; start accumulating internships early |
| Statistics | statistics, economic statistics | Data analysis, risk control, research positions | Math + business hybrid |

**Suited for students** who: have good Chinese/English, communicate well, and aim at first-tier-city finance/business resources.

---

### ⚖️ Law, education & public service

| Direction | Keywords | Notes |
|------|--------|------|
| Law | law, intellectual property | Bar-exam threshold; highly polarized employment |
| Teacher training / education | normal education, pedagogy, psychology | High stability; pay attention to ministry-affiliated / province-affiliated normal universities |
| Public administration | administrative management, public administration | Civil-service and public-institution track |

---

## Preferred cities & industry reference

| City | Key industries & employment characteristics |
|------|-------------------|
| Beijing | Dense with internet HQs, central SOEs, research institutes, and financial HQs; rich internship and further-study resources |
| Shanghai | Finance, foreign companies, biopharmaceuticals, integrated circuits; highly international |
| Shenzhen | Hard tech, internet, innovation & entrepreneurship; active private and tech companies |
| Hangzhou | E-commerce, digital economy, AI applications; the Alibaba ecosystem plus a startup scene |
| Wuhan | Optics Valley tech innovation, university resources, manufacturing; cost-effective central-China hub |
| Chengdu | Gaming, internet, electronic information; relatively friendly cost of living among the new first-tier cities |
| Xi'an | Aerospace, electronic information, defense industry; deep science-and-education heritage |
| Guangzhou | Greater Bay Area manufacturing, healthcare, trade; province-affiliated universities closely tied to industry |
| Nanjing | Software, advanced manufacturing, a large cluster of universities |
| Tianjin | Manufacturing, port economy, concentrated engineering universities |

---

## University-tier quick reference (aids school recommendation)

| Tag | Application-strategy tip |
|------|--------------|
| 985 / Double First-Class | Core reach/match targets; look at strong disciplines and postgraduate-recommendation rates |
| 211 | The backbone of match/safety; weigh city and major ranking |
| Postgraduate-recommendation eligibility | Weight it higher when further study is planned |
| Ministry-affiliated / province-affiliated | High industry recognition in teacher training, medicine, etc. |
| Seven Sons of National Defense / Six Military-Industry Schools | Engineering and defense-related directions |

---

## Recommended output counts

| Field | Recommended count | Notes |
|------|----------|------|
| `major_directions` | 2–4 | Sort by match level; each entry carries a personalized description |
| `recommended_majors` | 8–15 | Cover reach/match/safety; prioritize core "match"-tier majors |
| `recommended_schools` | 6–12 | Deduplicate schools; reach/match/safety all represented |

`modal.body` uses HTML fragments (`<h4>`, `<ul>`, `<li>`, `<strong>`); the content must be written **specifically for this student**, avoiding templated boilerplate.
