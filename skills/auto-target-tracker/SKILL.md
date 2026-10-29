---
name: auto-target-tracker
description: Automatic goal progress tracker. When goal-related images (notes, progress, screenshots, records) are detected in the conversation, automatically invokes a VLM to recognize the key information and logs it into the goal journal. Works for all goal-management scenarios: study tracking, fitness tracking, work progress, habit building, creative work logs, and more.
---

# Automatic Goal Progress Tracker

## Trigger Conditions

Automatically triggers when any of the following appears in the conversation:

1. **The user sends an image** (especially study notes, progress screenshots, workout logs, task checklists, creative works, etc.).
2. **The user sends an image during a scheduled goal time slot** (e.g. 08:30, 10:00, 20:00).
3. **The user explicitly says** things like "log this for me", "check my progress", "checking in", "update it", etc.

---

## Workflow

### 1. Detect the image

When an image is detected, check:
- Whether the image file name contains goal-related keywords (progress, goal, task, workout, note, etc.)
- Whether the image content contains goal elements (progress bars, text, code, charts, plans, etc.)
- Whether it is near a scheduled goal reminder time
- Whether the recent conversation context involves working on a goal

### 2. Invoke the VLM to recognize

Use the `vlm` tool to recognize the image:

**Generic prompt template**:
```
"Identify the key information in the image and extract the following based on the goal type:
- Core task/content
- Completion progress or count
- Key data (time, weight, word count, etc.)
- A short piece of execution feedback"
```

**Goal-type-specific prompts**:

| Goal type | Prompt |
|---------|--------|
| Study | "Identify the study notes; extract knowledge points and completion level" |
| Fitness | "Identify the workout log; extract exercise type, sets, reps, weight" |
| Work | "Identify the work progress; extract completed tasks and completion rate" |
| Creative | "Identify the creative work; extract the type, progress, and key elements" |
| Habit | "Identify the check-in record; extract the check-in content and streak days" |

### 3. Parse the goal information

From the VLM's response, extract:
- **Task/content list**: the specific actions or tasks identified
- **Completion level**: estimated progress based on the image content
- **Key data**: quantitative metrics such as time, count, weight, word count
- **Cognitive feedback**: a brief assessment of the current goal state

### 4. Record in the goal journal

Call the `edit_daily` tool to write the recognition results into the daily note for today


### 5. Feed back to the user

Confirm the recognition results with the user:

```
Your goal check-in has been recorded:

📝 Recognition results:
Core content: You photographed today's English vocabulary list — 15 new words memorized.
Progress estimate: Today's vocabulary task is fully done; you're ahead of 80% of learners.
Suggestion: Two of the words were a bit blurry — take an extra look when reviewing tomorrow.

Is the record accurate? Want me to save it into today's goal journal?
```

---

## Recording Format

### Example goal journal entry

```markdown
## 20:00 Check-in record

**Goal type**: 📚 Study

**Image**: ![Goal image](path/to/image.jpg)

**VLM recognition results**:

| Task/Content | Progress/Count | Status |
|----------|----------|------|
| English vocabulary (Unit 1) | 15 words | Completed |
| Math exercises (Chapter 3) | 80% | In progress |

| **Total** | | **2/3 done today** |

**Key data**:
- Study time: 2 hours
- Focus level: High

**Note**: Auto-recognized, confirmed correct by the user

---

## 10:30 Fitness check-in

**Goal type**: 🏃 Fitness

**Image**: ![Workout log](path/to/gym.jpg)

**VLM recognition results**:

| Exercise | Sets | Reps | Weight | Status |
|---------|------|------|------|------|
| Bench press | 4 | 12 | 60kg | ✅ Done |
| Squat | 4 | 10 | 80kg | ✅ Done |
| Pull-up | 3 | 8 | Bodyweight | ⚠️ One set short |

| **Total** | | | **On target today** |

**Key data**:
- Total weight: 2640kg
- Training time: 45 minutes

**Note**: One pull-up set short — make it up next time
```

---

## Integration with the Goal System

### Daily summary

The 22:00 daily summary should include:
- All of today's check-in records
- Goal achievement rate analysis
- Comparison against goals (if goals are set)

### Weekly/monthly reports

The weekly report should include:
- Effective execution time this week
- Goal coverage
- Consecutive check-in days
- Adaptive difficulty suggestions: if targets were consistently met, suggest increasing next week's workload

---

## Common Scenarios

### Scenario 1: Study check-in

**User action**: sends a photo of handwritten notes

**Auto-recognition**:
- Extract knowledge points
- Compute study progress
- Record in the study log

**Example feedback**:
```
📚 Study notes recognized:
- Supervised learning algorithms for machine learning (completed)
- Gradient descent optimizers (in progress)
- Regularization to prevent overfitting (not started)

Progress: 33% | Estimated 2 more hours to finish
```

### Scenario 2: Fitness check-in

**User action**: sends a photo of a workout log

**Auto-recognition**:
- Extract exercise types
- Tally sets, reps, weight
- Compute training volume

**Example feedback**:
```
🏃 Workout log recognized:
- Bench press 60kg × 12 × 4 sets ✅
- Squat 80kg × 10 × 4 sets ✅
- Pull-up bodyweight × 8 × 3 sets ✅

Total training volume: 2640kg | Duration: 45 minutes
```

### Scenario 3: Work progress

**User action**: sends a project progress screenshot

**Auto-recognition**:
- Extract completed tasks
- Compute completion percentage
- Identify remaining tasks

**Example feedback**:
```
💼 Work progress recognized:
- Requirements doc (completed) ✅
- Prototype design (completed) ✅
- Frontend development (in progress) 🔄 80%
- Backend development (not started) ⏳

Overall project progress: 67%
```

### Scenario 4: Creative check-in

**User action**: sends a photo of a creative work

**Auto-recognition**:
- Extract the creative type
- Identify key elements
- Estimate completion

**Example feedback**:
```
🎨 Creative work recognized:
Type: illustration
Elements: character, background scene
Completion: line art 100%, coloring 60%

Suggestion: You finished the character line art today — background coloring can start tomorrow
```

### Scenario 5: Habit check-in

**User action**: sends a habit tracker calendar screenshot

**Auto-recognition**:
- Extract consecutive check-in days
- Identify today's check-in status
- Compute check-in rate

**Example feedback**:
```
✅ Habit check-ins recognized:
Early rising: 15-day streak | 100% check-in rate
Reading: 8-day streak | 73% check-in rate
Exercise: 21-day streak | 100% check-in rate

🎉 Exercise has hit a 3-week streak — keep it up!
```

---

## Scope

This skill ONLY:
- Recognizes goal-related images and extracts key information
- Records check-in data into daily note files
- Provides progress feedback and suggestions

This skill NEVER:
- Automatically performs any actions based on the recognition results
- Uploads images to external services (other than the VLM API)
- Accesses image resources the user has not authorized
- Modifies the user's goal plans (only records progress)

---

## Security & Privacy

**Data that stays local:**
- The structured recognition results
- Content recorded into the daily note / long-term memory and USER.md
- Check-in history data

**This skill does NOT:**
- Share goal progress or check-in data with third parties
- Auto-publish check-in information to social platforms
- Access the user's other image resources

---

## Notes

1. **Privacy**: images and recognition results are stored locally only and are never uploaded to the cloud (except for the VLM API call used for recognition)
2. **Accuracy**: VLM recognition is for reference only and may be inaccurate due to blurry handwriting, image quality, etc.
3. **Timely confirmation**: users are advised to confirm the recognition results promptly after recording; discrepancies can be corrected manually
4. **Goal type detection**: the system infers the goal type from the image content; if it is wrong, adjust manually
5. **Progress estimation**: progress percentages are estimated from the image content and may be inaccurate; users are advised to update manually on a regular basis

---

## Integration Suggestions

### With SOUL.md

Fold the auto-tracker into the day-to-day goal-management workflow:

```markdown
### 2. Smart Logging & Estimation (Logging & Estimation)

- Whenever the user sends any goal-related image:
  1. Automatically invoke auto-target-tracker to recognize the content
  2. Extract the key information and estimate progress
  3. Immediately record it in the daily note
  4. Sync the goal progress to USER.md
```

### With HEARTBEAT.md

Include the following in the heartbeat check:

```markdown
## Daily summary
- At 22:00, automatically read all of today's check-in records
- Generate a goal progress report
- Send it to the user
```
