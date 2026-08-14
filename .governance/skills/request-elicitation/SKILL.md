---
name: request-elicitation
description: Use when a user message may be an actionable request; confirm the underlying goal and ask only material questions before acting, except for exempt autonomous action classes.
---

# Request Elicitation

Use this skill when the latest user message carries, or may carry, a request to do something. Do not use it for pure conversation, brainstorming, or questions that can be answered without taking action.

## Procedure

1. Reflect the underlying goal in one line.
2. Ask Jason to confirm, adjust, or refute that goal.
3. Ask one to three questions only if their answers would change what you do.
4. If no question would change the action, say there are no material questions.
5. Act only after Jason confirms the goal.

When execution preflight is required, include the intended actions, affected systems or files, expected risk tier, and validation plan in the same confirmation pass. Do not ask for a second confirmation if Jason has already confirmed a pass that included those fields.

## Exemptions

Do not run this gate for the standing autonomous action classes when another loaded policy already authorizes the action: board moves, doc and status updates, and version control.

## Calibration

Default to aggressive use per agent. Tune only downward for a request class when repeated use does not change the resulting action. Do not tune upward without Jason.
