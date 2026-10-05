# Computer Use with Desktop Applications - recording notes

Deck: `computer-use-with-applications.pptx` (5 slides), built by
`build_computer_use_with_applications.py`.

## Purpose

This is the short principles half of a demonstration showing ChatGPT operating a desktop
application through its visible interface.

## Speaking notes

1. **Computer Use with Desktop Applications**
   - Computer Use lets ChatGPT see and operate approved application interfaces.
2. **The assistant works through the visible interface**
   - It uses the same controls a person sees: windows, menus, text fields and buttons.
   - This helps when no dedicated integration reaches the task.
3. **Each action follows what is on screen**
   - ChatGPT observes the current state, takes one action and inspects the result.
   - The repeated observation is what lets it adapt as the interface changes.
4. **It reaches work with no direct integration**
   - Prefer a plugin or MCP tool for structured, repeatable data operations.
   - Use Computer Use when the interface itself is the only practical route.
   - Keep sensitive changes under human review.
5. **Live handoff**
   - Choose one app, describe a narrow outcome, approve access and keep control of the task.

## Current demo path to check before recording

OpenAI's current documentation says Computer Use is available through the ChatGPT
desktop app in supported regions on macOS and Windows. It requires the Computer Use
plugin, operating-system permissions and approval for the target app. The current prompt
pattern is to mention `@Computer` or the application by name. Confirm availability and
labels on your account before filming.

## Sources checked on 2026-09-15

- https://learn.chatgpt.com/docs/computer-use
- https://learn.chatgpt.com/use-cases/use-your-computer-with-codex

## Review rounds

- Round 1, hostile reviewer: removed platform-specific setup from the slides and added the distinction between structured integrations and visual control.
- Round 2, student: made the observe-and-check loop explicit, then added the wrong-window failure mode and take-over guidance.
