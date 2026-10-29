---
name: skill-finder-cn
description: "Skill Finder | Helps discover and install ClawHub Skills. Answers 'what skill can X', 'find a skill'. Trigger words: find skill, find skill, search skill."
author: DiveeOI
metadata:
  openclaw:
    emoji: 🔍
    requires:
      bins: [clawhub]
---

# Skill Finder

Help users discover and install Skills from ClawHub (https://clawhub.com).

## Purpose

When the user asks:
- "Is there a skill that can help me with...?"
- "Find a skill that can do X"
- "Is there a skill that can..."
- "I need a skill that can..."

This Skill searches ClawHub and recommends relevant Skills.

## Usage

### 1. Search Skills

```bash
clawhub search "<user requirement>"
```

### 2. View Details

```bash
clawhub inspect <skill-name>
```

### 3. Install a Skill

```bash
clawhub install <skill-name>
```

## Workflow

```
1. Understand the user's requirement
2. Extract keywords
3. Search ClawHub
4. List relevant Skills
5. Suggest which ones to install
```

## Example

**User**: "Is there a skill that can help me monitor cryptocurrency prices?"

**Search**: `clawhub search "crypto price monitor"`

**Result**: a list of relevant Skills

---

*Helping users discover the Skills they need 🔍*
