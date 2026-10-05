# Scheduled Tasks — deck notes

Lecture `scheduled-tasks` · Part 2 · ChatGPT Deep Dive · re-film · 01:39 · James
Video ID `48151369`. Deck: `scheduled-tasks.pptx`, built by `build_scheduled_tasks.py`.

## The three principles

- **What it is** — a scheduled task is an ordinary prompt saved as a standing
  instruction with a clock attached, so ChatGPT runs it at a time you name rather than
  the moment you type it.
- **How it works** — the clock starts the run, not you: the saved wording is sent on its
  own, with no one in the room to clarify it, and the result comes back as a notification.
- **Why it matters** — because nobody is there to fill the gaps, the prompt has to be
  self-contained; and because tasks keep running silently, a list you never check is a
  liability.

## Research

**Primary source, read directly** via headed Playwright:
`https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt`
("Scheduled tasks in ChatGPT", the page's own stamp read *Updated: 12 days ago* when
read on 2026-09-08). Everything below is from that page unless tagged otherwise.

**Creation.** You create a task by asking ChatGPT to complete an action — the help
page's own example is "Let me know when my package is delivered." No special syntax.
ChatGPT then shows a confirmation card carrying the task's title and its schedule.

**What it can do while you are away.**
- One-time or recurring runs.
- **Monitoring tasks**: check for changes and notify you when a relevant update occurs;
  they can use information from previous runs and stop at a defined end condition.
- **Connected apps**: Gmail, Slack, GitHub, where available for the account. Also
  ChatGPT Health / ChatGPT Finances data where the account has them.
- **Event-triggered (webhook) tasks** run in Work off supported Gmail, Slack or GitHub
  activity. Paid plans only (Plus, Pro, Business, Enterprise, Edu); not on Free or Go,
  not in FedRAMP workspaces.

**What it cannot do.**
- No voice chats, no GPTs.
- A task created in a project **cannot access uploaded files or files stored in that
  project**. This is the exact wording; the deck states it narrowly for that reason
  ("Reach files kept in a project"), rather than the tempting but unverified
  generalisation "it cannot see the files of the chat it came from".
- It cannot ask you a clarifying question. An action that would send a message or change
  external data may require approval, and **the task pauses until you review it**.

**How results reach you.** Notifications: `Settings > Notifications`, choose Push, Email
or both. Browser notification permission is needed for desktop; mobile push requires
creating the task in a supported mobile app and granting permission there.

**Limits.** Active-task caps by plan: **3 Free and Go, 5 Plus, 10 Business and Edu,
15 Pro and Enterprise.** Free users get a one-time task or a recurring task no more than
once per day, on flexible windows ("morning", "afternoon", "night"); hourly schedules and
exact delivery times need an eligible paid plan. Event-triggered tasks: up to 30 runs per
hour and 720 per day across all of them. If you hit the cap, pause or delete something.
None of these numbers are on a slide — they move. The durable point ("there is a cap")
is on slide 6.

**Pausing.** A task may pause because it is inactive, because it needs an action from
you, or because its associated chat was deleted. Deleting a chat associated with a task
pauses the task; deleting the task does not delete the chat.

**Sharing** (new since filming). You can share an active or paused task; the recipient
gets a snapshot of **title, instructions, schedule and original time zone** and creates
their own separate copy. The link does **not** carry your chat history, saved memories,
custom instructions, attached files or connected-app credentials. That is a neat
independent proof of the deck's core principle: the only thing that travels is the
wording, so the wording has to stand alone. Worth a sentence on camera if there is room.

## What has changed since the original recording

The transcript is short and still broadly correct in spirit, but four things have moved:

1. **"Click on GPT-4o with Scheduled Tasks"** — the feature is no longer a model picker
   entry. Tasks are created by asking for the work in an ordinary message.
2. **"Tasks in beta"** — no longer beta, and the task list has its own place rather than
   living behind the profile menu. Per the help page, the list is reached from the
   **Scheduled** page, from `Settings > Notifications > Manage tasks`, or from a
   conversation's `•••` menu via **See scheduled tasks**.
3. **Notifications are broader.** The original lecture only covers the desktop browser
   permission prompt; there are now Push *and* Email preferences under
   `Settings > Notifications`, plus mobile push.
4. **New capability the lecture predates**: monitoring tasks, event-triggered tasks,
   connected apps, and task sharing.

Nothing in the deck contradicts the old lecture; it teaches the mechanism the old
lecture assumed.

## Deck shape (9 slides)

1. Title
2. What is it? - a prompt with a clock attached *(mock: request → task saved)*
3. Not a reminder, a result *(compare)*
4. How it works - the clock starts the run, not you *(flow with a recurrence loop)*
5. What a run has to go on *(layers → "Runs with nobody to ask")*
6. Where it stops *(can / cannot panel)*
7. Why it matters - a vague instruction fails on a schedule *(table, incl. failure mode)*
8. Tasks outlive the reason you made them *(task list mock)*
9. Let's see it in action

Kept to 9 for a 01:39 lecture. The `layers` slide follows the house frame but its bands
are this feature's own components and its closing node is "Runs with nobody to ask" —
deliberately not the reference deck's wording.

## Review rounds

**Round 1 — hostile reviewer.** Five findings, all fixed.
1. Slide 2's assistant reply ("Set up. I'll run this on weekdays and message you with
   the result.") read like placeholder text — rewritten so it restates the actual job.
2. Slide 4's caption claimed "nothing sits open in the background", which is a guess
   about someone else's infrastructure. Replaced with the claim we can defend: *you* are
   not part of the run.
3. Slide 6's beside copy made two points (approval-pausing *and* the boundary list).
   Rewritten to one governing idea, with approval as its consequence.
4. Slide 6's "Multiply freely - each plan caps…" was awkward across two lines; rewritten.
5. Slide 8's window tag and its inner label said the same thing twice.
   Layout: slide 4 had a 0.95" hole between the flow and its caption — added the
   recurrence loop, which fills it and makes the repeat visible; slide 5's caption was
   stranded at the top of a tall diagram, moved down to sit against it; slide 7's table
   started at 1.55" while every other slide started at 1.52" — aligned.

**Round 2 — the student.** Two substantive findings, both fixed, so no third round.
1. Slide 6 said a task "cannot reach the files of the chat it came from". The verified
   limit is narrower — it is about **projects**. Narrowed the line to match the source
   rather than launder a generalisation.
2. Slide 2's saved-task line read "Weekdays, 07:00, your time zone", which is awkward as
   a stored value, and the time-zone point is already made properly on slide 5.
   Simplified to "Every weekday at 07:00".
   Craft: straight quotes on slide 5 replaced with typographic ones. Layout: nudged
   slide 5's caption to 2.55" so it centres against the three bands. Final sweep — every
   slide's content starts at 1.52", nothing crosses 5.10", bottoms sit in a 4.1"-4.8"
   band.

Linter: **clean, 9 slides, nothing to fix.**

## For James

- **Your note — "where to find all your scheduled tasks" — is in the demo half, not on a
  slide.** The current routes, per the help page: the **Scheduled** page;
  `Settings > Notifications > Manage tasks`; or a conversation's `•••` menu →
  **See scheduled tasks**. The task panel itself offers Edit, Pause, Delete and Manage
  tasks. Please confirm on your own account before filming — I read the documentation,
  not the product. The *principle* behind your note is on slide 8: tasks accumulate
  silently, so the list is where you retire what has served its purpose.
- **The desktop app may not have it.** The help page says Scheduled's availability
  depends on app and version, and to use the web if it is missing. Worth checking which
  surface you film on.
- **Your plan changes what you can demo.** Hourly schedules and exact delivery times need
  a paid plan; Free is capped at daily and uses flexible windows. If you show an hourly
  or minute-precise schedule, say that it is a paid-tier behaviour.
- **Boundary with `agent-mode`.** This deck stays strictly on the *time* dimension — work
  that runs without you present. It does not touch multi-step autonomy. The one place
  they nearly meet is approval-gated actions (a task that would change something outside
  ChatGPT pauses for review); I have kept that as a limit of tasks, not as agentic
  behaviour. Flagging in case the agent-mode deck also claims it.
- **Optional line worth saying on camera**: a shared task link carries only the title,
  instructions, schedule and time zone — not your memories, custom instructions or files.
  It is the cleanest possible demonstration of why the prompt has to be self-contained.
- Everything in this file is primary-verified from OpenAI's own help page except the
  characterisation of what has changed since the original recording, which is my reading
  of the old transcript against that page. `[unverified - James to check on his account]`
  applies to any of the click paths above.
