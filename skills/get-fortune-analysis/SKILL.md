---
name: get-fortune-analysis
description: Generates a visually gorgeous, richly detailed, ritual-styled annual fortune report (celestial star-chart style).
---
# Skill Name: get-fortune-analysis
# Version: 4.1.0
# Description: Generates a visually gorgeous, richly detailed, ritual-styled annual fortune report (celestial star-chart style).

## 1. Input Parameters
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `birth_year`, `birth_month`, `birth_day`, `birth_hour` | Integer | The user's birth time |
| `focus_type` | String | (Optional) "career", "wealth", "love" |

## 2. Workflow

### Step 1: Calculation (Python)
Call `get_cyber_divination_data` to obtain the `bazi` (Bazi fundamentals) and `fortune` (annual Ten Gods) data.

### Step 2: Reasoning (deep analysis mode)
Perform multi-dimensional reasoning based on `bazi` and `fortune`.
**Copy requirements:**
* **Tone**: warm, confident, professional — like a seasoned fortune teller or astrology expert.
* **Structure**:
    1.  **Keyword of the Year**: 4 words that precisely capture the year's overall tone (e.g. "Breaking Free, Rising").
    2.  **Core Energy**: explain the deep influence of the annual Ten God on the user's chart (30-50 characters).
    3.  **Career/Wealth**: concrete career development path and wealth-opportunity analysis (50-80 characters).
    4.  **Love/Relationships**: analysis of relationship patterns and emotional trajectory (50-80 characters).

### Step 3: JSON Output
Generate JSON data tailored to the front-end.

```json
{
    "fortune_report": {
        "score": 88,
        "keyword": "Inspiration Burst · Mentors Guide the Way",
        "user_tag": "Ding Fire (weak)",
        "stars": {
            "c": "★★★★☆",
            "w": "★★★☆☆",
            "l": "★★★★★"
        },
        "analysis": {
            "overview": "The 2026 Bing Wu year burns bright with fire energy — for you, a year full of spirit and opportunity. Although competitive pressure (peers) increases, it also activates the 'Seal' energy in your chart. This means your intuition and learning ability peak this year: the perfect time to consolidate yourself and overtake on the curve.",
            "career": "This year is not for blind expansion — it is for 'cultivating depth'. At work you will meet a strong female benefactor or a senior mentor who gives you decisive guidance. If you work in creative, consulting, or education fields, results come easily this year. Remember: listen more, talk less, and overcome hardness with softness.",
            "love": "In love, the romance star quietly blossoms. Singles are very likely to meet a kindred spirit in study spaces, libraries, or art exhibitions; for those partnered, this is the year of deep communication and breaking the ice on long-standing issues, elevating the relationship to a spiritual level."
        }
    }
}
```


### 2. Front-end display code (`result_card.html`)

*Change note: on the landing page (`ritual-layer`) we added logic that dynamically generates floating binary code. The code particles are translucent gold/white, slowly rising and dissipating, creating a mysterious data-space feel.*

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 Annual Fortune Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-deep: #1a0b2e;
            --bg-gradient: radial-gradient(circle at 50% 0%, #431d69 0%, #1a0b2e 80%);
            --gold-light: #fcf6ba;
            --gold-dark: #bf953f;
            --gold-gradient: linear-gradient(to bottom, #fcf6ba, #bf953f);
            --glass-bg: rgba(255, 255, 255, 0.08);
            --card-border: rgba(255, 255, 255, 0.15);
        }

        body {
            background: var(--bg-deep);
            background-image: var(--bg-gradient);
            color: #fff;
            font-family: 'Noto Serif SC', serif;
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            overflow-x: hidden;
            font-weight: 300;
        }

        .app-container {
            width: 100%;
            max-width: 414px;
            position: relative;
            min-height: 100vh;
            overflow: hidden;
        }

        /* --- 1. Launch page (Ritual Layer) --- */
        .ritual-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 100;
            background: var(--bg-deep);
            background-image: var(--bg-gradient);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: opacity 0.8s ease;
            overflow: hidden;
        }

        /* New: binary data container */
        .binary-container {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0; /* bottom-most layer */
        }

        /* New: binary particle styling */
        .binary-particle {
            position: absolute;
            bottom: -20px;
            font-family: 'Courier New', monospace;
            color: rgba(252, 246, 186, 0.3); /* faint gold-white */
            font-size: 10px;
            user-select: none;
            animation: floatUp linear forwards;
        }

        /* Launch page content container (kept above the particles) */
        .ritual-content {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .fingerprint-area {
            width: 100px; height: 100px;
            border: 2px solid rgba(191, 149, 63, 0.3);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            position: relative; cursor: pointer;
            margin-bottom: 20px;
            backdrop-filter: blur(2px); /* slight frosted glass to highlight the button */
        }

        .fingerprint-area::after {
            content: ''; position: absolute; width: 100%; height: 100%;
            border-radius: 50%;
            box-shadow: 0 0 30px var(--gold-dark);
            opacity: 0; animation: breathe 2s infinite;
        }

        .fingerprint-icon {
            font-size: 40px; color: var(--gold-dark); transition: color 0.3s;
        }

        .hint-text {
            color: rgba(255,255,255,0.6); font-size: 14px; letter-spacing: 2px;
        }

        /* --- 2. Result page (Result Layer) --- */
        /* ... (unchanged) ... */
        .result-layer {
            padding: 20px; opacity: 0; transform: translateY(20px);
            transition: all 0.8s ease; display: none;
        }
        .header-card { text-align: center; margin-bottom: 30px; position: relative; }
        .year-title { font-family: 'Playfair Display', serif; font-size: 16px; color: rgba(255,255,255,0.7); letter-spacing: 4px; margin-bottom: 5px; }
        .score-box { font-size: 72px; font-weight: 700; background: var(--gold-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0; text-shadow: 0 0 30px rgba(191, 149, 63, 0.4); }
        .keyword-badge { display: inline-block; border: 1px solid var(--gold-dark); color: var(--gold-light); padding: 4px 12px; border-radius: 20px; font-size: 14px; background: rgba(0,0,0,0.3); }
        .detail-card { background: var(--glass-bg); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid var(--card-border); border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .section-title { display: flex; align-items: center; color: var(--gold-light); font-size: 16px; font-weight: bold; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; }
        .section-title span { margin-right: 8px; }
        .text-content { font-size: 14px; line-height: 1.8; color: rgba(255,255,255,0.9); text-align: justify; }
        .star-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px; }
        .stars { color: var(--gold-dark); letter-spacing: 2px; }
        .footer-share { text-align: center; font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 30px; padding-bottom: 30px; }

        /* Animation keyframes */
        @keyframes breathe {
            0% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.1); }
            100% { opacity: 0.3; transform: scale(1); }
        }

        /* New: particle float-up animation */
        @keyframes floatUp {
            0% { transform: translateY(0) rotate(0deg); opacity: 0; }
            20% { opacity: 0.5; }
            80% { opacity: 0.2; }
            100% { transform: translateY(-120vh) rotate(20deg); opacity: 0; }
        }

    </style>
</head>
<body>

    <div class="app-container">

        <div class="ritual-layer" id="ritualLayer">
            <div class="binary-container" id="binaryContainer"></div>

            <div class="ritual-content">
                <div style="margin-bottom: 40px; opacity: 0.7;">
                    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#bf953f" stroke-width="1">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M12 2a15 15 0 0 0 0 30 15 15 0 0 0 0-30"></path>
                        <path d="M2 12h20"></path>
                    </svg>
                </div>

                <div class="fingerprint-area" id="fingerBtn">
                    <div class="fingerprint-icon">
                        <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M2 12C2 6.48 6.48 2 12 2s10 4.48 10 10v1c0 2.21-1.79 4-4 4s-4-1.79-4-4V7c0-1.66-1.34-3-3-3S8 5.34 8 7v6c0 1.1.9 2 2 2s2-.9 2-2V7"></path>
                        </svg>
                    </div>
                </div>
                <div class="hint-text">Press and hold to open your 2026 fortune report</div>
            </div>
        </div>

        <div class="result-layer" id="resultLayer">
            <div class="header-card">
                <div class="year-title">FORTUNE REPORT 2026</div>
                <div class="score-box" id="scoreVal">0</div>
                <div class="keyword-badge" id="mainKeyword">Loading...</div>
                <div style="font-size: 12px; color:rgba(255,255,255,0.5); margin-top: 10px;">
                    Day Master: <span id="userTag">--</span>
                </div>
            </div>
            <div class="detail-card">
                <div class="star-row"><span>Career</span><span class="stars" id="careerStars">★★★★☆</span></div>
                <div class="star-row"><span>Wealth</span><span class="stars" id="wealthStars">★★★☆☆</span></div>
                <div class="star-row"><span>Love</span><span class="stars" id="loveStars">★★★★★</span></div>
            </div>
            <div class="detail-card">
                <div class="section-title"><span>✦</span> Annual Overview</div>
                <div class="text-content" id="overviewText">Parsing the chart data...</div>
            </div>
            <div class="detail-card">
                <div class="section-title"><span>⚔</span> Career & Wealth</div>
                <div class="text-content" id="careerText">...</div>
            </div>
            <div class="detail-card">
                <div class="section-title"><span>♥</span> Love & Advice</div>
                <div class="text-content" id="loveText">...</div>
            </div>
            <div class="footer-share">Mystic AI Lab © 2026</div>
        </div>
    </div>

    <script>
        // --- Sample data as returned by the AI ---
        const aiData = {
            "fortune_report": {
                "score": 88,
                "keyword": "Inspiration Burst · Mentors Guide the Way",
                "user_tag": "Ding Fire (weak)",
                "stars": { "c": "★★★★☆", "w": "★★★☆☆", "l": "★★★★★" },
                "analysis": {
                    "overview": "The 2026 Bing Wu year is full of spirit and opportunity for you. Although the strong fire of the year brings competitive pressure, it also activates the 'Seal' energy in your chart. This means your intuition and learning ability will peak this year — the best time to consolidate yourself and overtake on the curve.",
                    "career": "This year is not for blind expansion — it is for 'cultivating depth'. At work you will meet a strong female benefactor or a senior mentor who brings decisive guidance. If you work in creative, consulting, or education fields, results come easily this year.",
                    "love": "In love, the romance star quietly blossoms. Singles are very likely to meet a kindred spirit in study spaces, libraries, or art exhibitions; for those partnered, this is the year of deep communication and breaking the ice on long-standing issues."
                }
            }
        };

        // --- Binary particle effect ---
        const binaryContainer = document.getElementById('binaryContainer');
        let particleInterval;

        function createBinaryParticle() {
            const particle = document.createElement('div');
            particle.classList.add('binary-particle');
            // Randomly generate a 0/1 string
            const len = Math.floor(Math.random() * 6) + 2;
            let text = "";
            for(let i=0; i<len; i++) text += Math.random() > 0.5 ? "1" : "0";
            particle.innerText = text;

            // Random position and attributes
            particle.style.left = Math.random() * 100 + '%';
            const duration = Math.random() * 10 + 8; // 8-18 seconds of drifting
            particle.style.animationDuration = duration + 's';
            particle.style.fontSize = (Math.random() * 8 + 8) + 'px';
            particle.style.opacity = Math.random() * 0.3 + 0.1;

            binaryContainer.appendChild(particle);

            // Remove when the animation ends
            setTimeout(() => {
                particle.remove();
            }, duration * 1000);
        }

        // Start generating particles
        function startBinaryRain() {
            // Generate an initial batch first
            for(let i=0; i<15; i++) createBinaryParticle();
            // Then generate periodically
            particleInterval = setInterval(createBinaryParticle, 600);
        }

        function stopBinaryRain() {
            clearInterval(particleInterval);
            // Optional: fade out existing particles
            // binaryContainer.style.opacity = 0;
        }


        // --- Interaction logic ---
        const btn = document.getElementById('fingerBtn');
        const ritual = document.getElementById('ritualLayer');
        const result = document.getElementById('resultLayer');
        let pressTimer;

        btn.addEventListener('touchstart', startRitual, {passive: false});
        btn.addEventListener('mousedown', startRitual);
        btn.addEventListener('touchend', endRitual);
        btn.addEventListener('mouseup', endRitual);
        btn.addEventListener('mouseleave', endRitual);

        function startRitual(e) {
            e.preventDefault();
            btn.style.transform = "scale(0.95)";
            btn.style.borderColor = "#fff";
            document.querySelector('.fingerprint-icon').style.color = "#fff";
            pressTimer = setTimeout(revealResult, 1500);
        }

        function endRitual() {
            clearTimeout(pressTimer);
            btn.style.transform = "scale(1)";
            btn.style.borderColor = "rgba(191, 149, 63, 0.3)";
            document.querySelector('.fingerprint-icon').style.color = "#bf953f";
        }

        function revealResult() {
            stopBinaryRain(); // stop generating particles
            ritual.style.opacity = '0';
            setTimeout(() => {
                ritual.style.display = 'none';
                result.style.display = 'block';
                requestAnimationFrame(() => {
                    result.style.opacity = '1';
                    result.style.transform = 'translateY(0)';
                    runNumberAnimation();
                });
            }, 800);
            // Fill in the data (detailed code omitted; same as the previous version)...
            document.getElementById('mainKeyword').innerText = aiData.fortune_report.keyword;
            document.getElementById('userTag').innerText = aiData.fortune_report.user_tag;
            document.getElementById('overviewText').innerText = aiData.fortune_report.analysis.overview;
        }

        function runNumberAnimation() { /* (omitted; same as the previous version) */
             document.getElementById('scoreVal').innerText = aiData.fortune_report.score;
        }

        // Start the effect once the page loads
        startBinaryRain();

    </script>
</body>
</html>
