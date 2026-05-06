---
name: meeting-insights-analyzer
description: Analyzes meeting transcripts to uncover behavioral patterns, communication insights, and actionable feedback — identifies conflict avoidance, filler words, speaking ratios, and listening quality.
kind: skill
---

# Meeting Insights Analyzer

This skill transforms your meeting transcripts into actionable insights about your communication patterns, helping you become a more effective communicator and leader.

## When to Use This Skill

- Analyzing your communication patterns across multiple meetings
- Getting feedback on your leadership and facilitation style
- Identifying when you avoid difficult conversations
- Understanding your speaking habits and filler words
- Tracking improvement in communication skills over time
- Preparing for performance reviews with concrete examples
- Coaching team members on their communication style

## What This Skill Does

1. **Pattern Recognition**: Identifies recurring behaviors across meetings
   - Conflict avoidance or indirect communication
   - Speaking ratios and turn-taking
   - Question-asking vs. statement-making patterns
   - Active listening indicators
   - Decision-making approaches

2. **Communication Analysis**: Evaluates communication effectiveness
   - Clarity and directness
   - Use of filler words and hedging language
   - Tone and sentiment patterns
   - Meeting control and facilitation

3. **Actionable Feedback**: Specific, timestamped examples with what happened, why it matters, and how to improve

4. **Trend Tracking**: Compares patterns over time when analyzing multiple meetings

## How to Use

### Setup

1. Download your meeting transcripts to a folder (e.g., `~/meetings/`)
2. Navigate to that folder in Claude Code
3. Ask for the analysis you want

### Quick Start

```
Analyze all meetings in this folder and tell me when I avoided conflict.
```

```
Look at my meetings from the past month and identify my communication patterns.
```

```
Analyze all transcripts and:
1. Identify when I interrupted others
2. Calculate my speaking ratio
3. Find moments I avoided giving direct feedback
4. Track my use of filler words
5. Show examples of good active listening
```

## Analysis Patterns

### Conflict Avoidance
- Hedging language ("maybe", "kind of", "I think")
- Indirect phrasing instead of direct requests
- Changing subject when tension arises
- Agreeing without commitment ("yeah, but...")

### Speaking Ratios
- Percentage of meeting spent speaking
- Interruptions given and received
- Average speaking turn length
- Question vs. statement ratio

### Filler Words
- Count of "um", "uh", "like", "you know", "actually"
- Frequency per minute
- Situations where they increase (nervous, uncertain)

### Active Listening
- Questions that reference others' previous points
- Paraphrasing or summarizing others' ideas
- Building on others' contributions

## Output Format

```markdown
# Meeting Insights Summary

**Analysis Period**: [Date range]
**Meetings Analyzed**: [X meetings]

## Key Patterns Identified

### 1. [Primary Pattern]
- **Observed**: [What you saw]
- **Impact**: [Why it matters]
- **Recommendation**: [How to improve]

**Examples**:
1. **[Meeting Name/Date]** - [Timestamp]
   > [Actual quote from transcript]
   **Why This Matters**: [Explanation]
   **Better Approach**: [Alternative]

## Communication Strengths
1. [Strength with example]

## Speaking Statistics
- Average speaking time: [X% of meeting]
- Questions asked: [X per meeting]
- Filler words: [X per minute]
- Interruptions: [X given / Y received]

## Next Steps
[3-5 concrete actions to improve communication]
```

## Getting Transcripts

- **Granola**: Auto-transcribes meetings, export to folder
- **Zoom**: Enable cloud recording with transcription, download VTT/SRT
- **Google Meet**: Use Google Docs auto-transcription
- **Fireflies.ai / Otter.ai**: Export transcripts in bulk

## Common Analysis Requests

- "When do I avoid difficult conversations?"
- "How often do I interrupt others?"
- "What's my speaking vs. listening ratio?"
- "Do I ask good questions?"
- "How has my communication changed over time?"

*Source: github.com/ComposioHQ/awesome-claude-skills*
