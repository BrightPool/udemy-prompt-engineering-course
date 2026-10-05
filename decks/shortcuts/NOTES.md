# Shortcuts - re-film notes

Lecture `shortcuts` · video_id `39228730` · Part 2, ChatGPT Deep Dive · 00:35 · James
Deck: `shortcuts.pptx` (**6 slides**), built by `build_shortcuts.py`.

This is the shortest lecture in the course, so it gets the shortest deck. Six slides is
deliberate, and the deck was reviewed twice specifically for padding.

---

## The three principles the deck teaches

1. **What it is** - the keyboard is a second set of controls over the same ChatGPT
   interface: every shortcut corresponds to a button you already click.
2. **How it works** - a shortcut is a second door to one action, not a hidden mode; the
   interface runs exactly the same code either way, so nothing about the answer changes.
3. **Why it matters** - it drives the cost of the small, repeated moves to almost nothing,
   and because the actual key combinations differ by platform and move when the product is
   redesigned, the only one worth memorising is the one that shows you the current list.

---

## The one rule the deck follows absolutely

**No key combination appears anywhere in the deck.** They are the most drift-prone content
in the whole course - they differ between macOS, Windows and the web, and they change with
redesigns. They live in this file, for you to say aloud, and on screen in the live demo.

The deck also carries no screenshots, no menu paths and no version numbers.

---

## The current shortcut list, for the spoken track

### Primary-verified from OpenAI's help centre (2026-09-08, headed Playwright)

| Action | Keys | Source |
|---|---|---|
| Search your chat history | **Ctrl + K** (PC) / **Cmd + K** (Mac) | `help.openai.com/en/articles/10056348-how-do-i-search-my-chat-history-in-chatgpt` - also names the **Search** magnifying glass in the left sidebar |
| Stop a streaming response (macOS app) | **Command + .** | `.../9703738-chatgpt-macos-app-release-notes` |
| Find text within a conversation (macOS app) | **Command + F**, or the app menu | same |
| Share the main desktop (macOS app) | **Command + Shift + 1** | same |
| Share the active window (macOS app) | **Command + Shift + 2** | same |
| Toggle the sidebar (macOS app) | exists - the release notes record "added back the keyboard shortcut for toggling the sidebar" but do not print the combination | same |
| Adjust text scaling (Windows app) | **Ctrl + plus** / **Ctrl + minus** | `.../10003026-windows-app-release-notes` |

**There is no dedicated "keyboard shortcuts" article in the OpenAI help centre.** I
searched it directly for "keyboard shortcuts", "shortcuts", "keyboard" and "accessibility"
and none returns one. The list below therefore comes from secondary sources.

### Secondary sources only - `[unverified - James to check on his account]`

The list James recites in the original take, as the open web currently reports it:

| Action | Keys (Windows / Mac) |
|---|---|
| **Open the keyboard shortcuts panel** | **Ctrl + /** / **Cmd + /** |
| Open a new chat | Ctrl + Shift + O / Cmd + Shift + O |
| Toggle the sidebar | Ctrl + Shift + S / Cmd + Shift + S |
| Copy the last response | Ctrl + Shift + C / Cmd + Shift + C |
| Copy the last code block | Ctrl + Shift + ; / Cmd + Shift + ; |
| Focus the chat input | Shift + Esc |
| Delete the current chat | Ctrl + Shift + Backspace / Cmd + Shift + Backspace |
| Send / new line | Enter / Shift + Enter |

Secondary sources also say the shortcut list is reachable **from the help menu** as well as
from the key combination. That is the "new keyboard shortcuts menu" your note points at,
and it is the thing to show on camera - **please confirm on your own account before
filming**, since I could not verify where that menu now sits.

Two more secondary claims I deliberately kept out of the deck and out of the demo list,
because I could not corroborate them anywhere first-party: a **Ctrl + Shift + P** prompt-
template panel, and any Atlas-browser-specific shortcut set.

### Deliberately out of scope

**Option + Space** (macOS) and **Alt + Space** (Windows) open the desktop companion
window. That is a system-wide hotkey, not a shortcut *within* the interface, and the
`desktop-app` deck already covers it. I have left it alone entirely - do not add it here or
the two lectures will collide.

---

## What has changed since filming

The original take is 35 seconds and holds up better than most lectures in the course:
the mechanism is unchanged, the panel still exists, and the six actions James names are all
still real actions.

| Time | What is said | Status |
|---|---|---|
| 0:04 | "toggle the sidebar like this" | Still true. |
| 0:05-0:08 | "Hit Control, forward slash, or if you're on Mac, hit Command, forward slash" | Still the reported combination `[unverified]`, but there is now also a **help-menu route** to the same panel, which is what your note asks you to show. |
| 0:08 | "something called keyboard shortcuts" | Still the panel's name `[unverified]`. |
| 0:11-0:13 | "deleting the chat, opening a new chat, focusing the chat input, copying the last response or the last code block" | All still present. **Chat search (Ctrl/Cmd + K) is missing from the original list** and is now arguably the single most useful one - worth adding on camera. |
| 0:14 | "speed up your ChatGPT workplace" | Slip of the tongue: "workflow". |

---

## Review rounds

**Round 1 - the hostile reviewer.** Four findings, all fixed.
1. Slide 2's copy claimed "every one of these is a button you already know" - an
   over-claim, since one of the listed rows is the shortcut panel itself. Reworded to
   "each line here is something you already do with the pointer".
2. Slide 2 listed "Delete the current chat", which is the least useful action of the set
   and is not first-party verified. Swapped for **Stop the response**, which is
   primary-verified in the macOS release notes and is more useful.
3. Slides 3 and 5 both ended on the same idea ("the keys move, so learn the one that lists
   them"). Two captions restating the deck's thesis in a six-slide deck is padding.
   Slide 3's caption was rewritten to explain its own diagram (learn the *shape* of the
   list) and slide 5 now carries the platform/redesign limit alone.
4. Layout: slide 3's caption was top-aligned at 1.66" against a stack running to 4.41",
   leaving it stranded high. Centred against the bands. Slide 4's arrows were tripping the
   linter's `double-rule` check because a 0.10"-high accent shape above y=2.2 looks like a
   rogue rule; they now use the default arrow height. All four content slides start at
   1.56".

**Round 2 - the student.** Three findings, all fixed; none substantive enough to force a
third round.
1. Slide 3's second band read "new chat, delete, focus" but round 1 had removed "delete"
   from the mock on slide 2. Contradiction between two adjacent slides - now "new chat,
   stop, focus".
2. Slide 3's accent band said "the only one to learn" while the slide title says
   "memorising". Aligned on **memorise**.
3. Layout: slide 2's content bottomed out at 4.02" while slides 3-6 run to 4.35-4.53",
   so it floated visibly high. Restored "Copy the last code block" to the mock (a pair with
   "Copy the last response", and it is in the original transcript), bringing the slide to
   4.25". Slide 4's caption was at x=0.60 while its diagram spans 1.35" to 8.65" - aligned
   the caption to the diagram.

Linter: **clean, 0 errors, 0 warnings, 6 slides.**

---

## For James

1. **Confirm the help-menu route before filming.** Your note says "show the new keyboard
   shortcuts menu", and secondary sources agree the shortcut list is now reachable from the
   help menu as well as from Cmd/Ctrl + /. I could not verify where that menu sits - there
   is no keyboard-shortcuts article in the OpenAI help centre at all. Open it on your own
   account and show whatever is actually there.
2. **Add chat search to the spoken list.** The original take does not mention
   **Ctrl/Cmd + K**, which is the only shortcut in the set that OpenAI documents by name
   for the web, and probably the most useful one a student will adopt. The deck's slide 3
   already makes room for it under "Move around".
3. **Every key combination in this file is for the spoken track only.** None of them are on
   a slide, on purpose. If you want them on screen, put them in the demo half where a
   re-film costs one take rather than a deck rebuild.
4. **Do not stray into the companion window.** Option/Alt + Space belongs to the
   `desktop-app` lecture and is already taught there.
5. The original take says "speed up your ChatGPT **workplace**" at 0:14. It is a small slip
   and worth fixing in the new read.
