# Output JSON Schema

The complete JSON format for interpretation results. The front-end renders the "dream analysis card" based on this format.

## Full structure

```json
{
  "dream_summary": "string — one-sentence summary of the dream (20 characters max)",
  "keywords": ["string — dream keywords, 3-6 of them"],
  "mood": "string — mood classification; enum values below",
  "color_scheme": "string — color scheme name, corresponding to the mood",
  "visual_elements": ["string — visual element identifiers, 5 max, see visual-mapping.md"],
  "interpretations": {
    "zhouGong": {
      "icon": "🔮",
      "title": "Zhou Gong Dream Interpretation",
      "content": "string — main interpretation, 100-200 characters",
      "fortune": "string — verdict: very auspicious / auspicious / neutral / neutral-leaning-inauspicious / inauspicious",
      "advice": "string — one-sentence advice in do/avoid format"
    },
    "freud": {
      "icon": "🧠",
      "title": "Psychological Analysis",
      "content": "string — psychological analysis, 100-200 characters",
      "insight": "string — one-sentence core insight",
      "advice": "string — one concrete self-care suggestion"
    },
    "cyber": {
      "icon": "🌀",
      "title": "Cyber Mystic",
      "content": "string — cyber reading, 100-200 characters",
      "prediction": "string — one outrageous prediction",
      "advice": "string — one funny but concrete action suggestion"
    }
  },
  "overall_advice": "string — overall advice, 1-2 sentences, neutral tone",
  "shareable_text": "string — shareable text with emoji, suitable for social posting, 50 characters max"
}
```

## mood enum values

| Value | Meaning |
|----|------|
| anxious | anxiety, fear, tension |
| peaceful | calm, pleasant, comfortable |
| sad | sadness, loss, regret |
| surreal | fantastical, absurd, surreal |
| exciting | excitement, thrill, adventure |
| nostalgic | nostalgia, warmth, longing |

## Mapping color_scheme to mood

The mood and color_scheme values are identical. The front-end picks colors from the palette table in visual-mapping.md based on the color_scheme value.

## Output requirements

1. The JSON must be valid and directly JSON.parse-able
2. Wrap it in a ```json code block
3. No string field may be empty
4. The keywords array has 3-6 elements
5. The visual_elements array has 1-5 elements
6. The three interpretations' content lengths should stay close (all 100-200 characters)
7. The shareable_text should be fun and make people want to repost it
