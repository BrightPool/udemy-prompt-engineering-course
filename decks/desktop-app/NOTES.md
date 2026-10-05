# ChatGPT Desktop Application - re-film notes

Lecture `desktop-app` · video_id `44003766` · Part 2, ChatGPT Deep Dive · 05:25 · James
Deck: `desktop-app.pptx` (11 slides), built by `build_desktop_app.py`.

---

## The three principles the deck teaches

1. **What it is** - ChatGPT running as an application on your computer rather than a page
   you navigate to: same account, same conversations, same models, a keystroke away on top
   of whatever you already have open.
2. **How it works** - proximity buys it context you would otherwise have retyped (the
   window you point at, the app you were in, a file or folder, a page, your voice), and
   every one of those arrives only through a permission your computer asks you to grant.
3. **Why it matters** - the cost of asking a question falls to almost nothing, and the
   price is that something able to see your work now sits next to your work, so the
   failure mode flips from "vague answers" to "you sent more than you meant to".

The deck deliberately never lists platforms, hotkeys, menu paths or version numbers. This
is the most drift-prone lecture in the course, so all of that lives below for you to say
aloud over the live demo.

---

## The outdated references, with timestamps

Fifteen, rather than the ten you expected. Ordered as they appear.

| # | Time | What is said | What is true now |
|---|---|---|---|
| 1 | 0:02 | "the **new** ChatGPT desktop application" | Not new, and the name now means something different. The desktop app was rebuilt to combine **Chat**, **Work** and **Codex**; the app in this footage has been renamed **ChatGPT Classic** and still ships, but new agentic features land only in the new app. |
| 2 | 0:08 | "go to openai.com slash chatgpt slash desktop" | The download page is **chatgpt.com/download** (openai.com/chatgpt/download resolves there). Its copy today: "Bring ChatGPT to your desktop with ChatGPT Work and Codex, plus context from your email, screenshots, files, and anything on your screen." ChatGPT Classic has its own separate download links at the foot of that page. |
| 3 | 0:13 | "you can download it for either your macOS or Windows" | **This is your platform note.** Incomplete rather than wrong. Today: desktop on macOS and Windows, mobile on iOS and Android, the web, a Chrome extension, and OpenAI's own browser (ChatGPT Atlas). The deck's line is "one of several places it runs" - state the current list on camera. |
| 4 | 0:21 | "your chat history on the left hand" | The sidebar is now **Recents**, holding Chat and Work chats together with filter, sort and pin, plus **Projects**. A top-left menu switches between ChatGPT and Codex; inside ChatGPT a toggle at the top of the page switches Chat and Work. |
| 5 | 0:24 | "bottom left ... click on settings" | Settings has moved. Nothing in the deck depends on where it sits. |
| 6 | 0:34 | "whether you want to use for chat training" | The control is now **"Improve the model for everyone"**, alongside temporary chat and the wider data controls. |
| 7 | 0:46-0:49 | "different types of **GPT-4** capabilities ... browsing, DALL·E and code" | Two problems. GPT-4 is several generations back (see the model note below), and per-capability toggles for browsing / DALL·E / code no longer exist - those capabilities are folded into the model and picked automatically. |
| 8 | 1:06-1:11 | "choose between **Ember, Juniper, Breeze or Cove**" | That voice list is stale. Voice now has three modes under Settings > Voice: **Live** (the current real-time experience, and the default), **Advanced** (the previous real-time one, for video and screen sharing on mobile) and **Standard** (turn-by-turn, transcribes first). |
| 9 | 1:19-1:22 | "click on the headphones ... ChatGPT will enter a voice communication" | The entry point has changed, and more importantly so has the model of it - see 10. |
| 10 | 1:48-2:11 | pause it, cancel it, go to the top left, find "a voice chat that's just ended" as a separate item in history | **No longer how it works.** Voice runs *inside* a chat: you follow the response in text as it speaks, can type when you cannot speak, and can scroll back without starting over. There is no separate "voice chat" entry to hunt for afterwards. This is the single biggest correction in the lecture and the deck's slide 7 replaces it. |
| 11 | 2:13-3:41 | run a voice conversation in the app and a second ChatGPT session in a browser window at the same time | The reason for the trick has gone (voice is no longer a separate chat), and **only one Voice conversation can run at a time**. The genuinely current version of "talk while you work" is Voice in Work / Codex, where you speak to start and coordinate tasks while they run. |
| 12 | 3:44-3:51 | "the latency of voice is gonna be reduced significantly ... when that model comes out" | It came out. Delete the prediction. |
| 13 | 4:00-4:02 | "you can do this on **Macintosh** by holding the alt or option in space" | **Second half of your platform note.** The companion window is not Mac-only: **Option+Space** on macOS, **Alt+Space** on Windows, and the Windows hotkey is rebindable (it silently fails if another app already owns the combination). |
| 14 | 4:14-4:17, 5:03 | "attachment icon ... take screenshot or take photo" | Still exists in ChatGPT Classic, but it is now the *smallest* of the desktop-only powers. The lecture stops at screenshots and never mentions **Work with Apps** (reading and editing your editor, notes app or terminal), **local files and folders**, or the app's **own built-in browser**. |
| 15 | 4:37 | "we can send vision directly to Spotify" | Simple misstatement. The screenshot goes to ChatGPT; nothing is sent to Spotify. |

**Also worth a line on camera:** the lecture predates most of what makes the desktop app
interesting. Nothing in it mentions Work, Codex, the built-in browser, local folders, or
the operating-system permissions all of that needs.

---

## Research, verified 2026-09-08

All of the following was read directly from first-party OpenAI pages via headed
Playwright. Everything is **primary-verified** unless tagged otherwise.

### The app itself

Source: `help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app`,
`.../20001275-chatgpt-work-and-codex`, `.../9275200-downloading-the-chatgpt-macos-app`,
`.../9982051-using-the-chatgpt-windows-app`, and `chatgpt.com/download`.

- The new ChatGPT desktop app **combines Chat, Work and Codex**, on macOS and Windows. The
  help centre dates the change to **9 July**. The previous app is **ChatGPT Classic**; it
  keeps getting model updates, bug fixes and security patches, and no migration is forced.
- Navigation: ChatGPT or Codex from the **top-left menu**; inside ChatGPT, **Chat** or
  **Work** from the toggle at the top of the page. Chat and Work chats share **Recents**
  (sort, filter, pin). Existing **Projects** carry over.
- Chat syncs between web and desktop. Cloud Work chats sync across web, mobile and
  desktop. **Codex is not selectable on web or mobile** (remote Codex chats are reachable
  from the Remote tab in the mobile app).
- System requirements: macOS 14 with Apple Silicon or Intel; Windows 10 (x64 and arm64)
  17763.0 or higher.
- The **companion window / chat bar** is **Option+Space** (macOS) and **Alt+Space**
  (Windows). The Windows hotkey is under Settings > App > Companion window hotkey and will
  not fire if another Windows application already owns the combination.

### What it can do that a browser tab cannot

- **Work with Apps** (`.../10119604-work-with-apps-on-macos`, macOS only as of today):
  ChatGPT can read and edit content in supported apps. Text editors: Apple Notes, Notion,
  TextEdit, Quip. Code editors: Xcode, VS Code family (including Cursor and Windsurf),
  JetBrains family, Script Editor. Terminals: Terminal, iTerm, Warp, Prompt. It includes
  the **last 200 lines of open panes**, or your selection plus neighbouring text. It works
  through the **macOS Accessibility API** (VS Code needs an extension), so revoking
  Accessibility permission for ChatGPT turns it off. A banner over the chat bar shows
  which apps it is currently reading. Enterprise admins can disable it workspace-wide.
- **Screenshot tool** (`.../9295245`): the Plus icon in the prompt window, listing open
  application windows. Requires **Screen & Audio Recording** permission, and may need an
  app restart after granting.
- **Built-in browser** (`.../20001277`, macOS and Windows): opens from the toolbar or
  Cmd+Shift+B / Ctrl+Shift+B, in Work or Codex. You and ChatGPT see the same page; it can
  work across tabs, download files, and wait while you sign in. It has **its own browser
  state** - it does not use your Chrome profile or your signed-in Chrome sessions. It asks
  before using a new website, and allowed/blocked hosts are managed in desktop settings.
  There is an **Annotation mode** for marking up an element and asking for a change.
  OpenAI's own guidance: *treat website content as untrusted*, enter credentials in the
  browser and never in the chat, and check which account is active before approving.
- **Local files and folders**: in the desktop app, Work and Codex can open a local folder.
  Messages and task context may still be stored in the cloud even when the work runs
  locally.
- **Voice** (`.../20001274-chatgpt-voice`): Voice works *within* a chat - you listen while
  following the text, can type instead, and can scroll back. **Live** can interrupt
  naturally and use web search and memory. **Voice in Work and Codex** is a desktop-only
  capability on macOS and Windows and can start and coordinate tasks; it may need
  microphone, and for computer context also Screen & Audio Recording and Accessibility.
  Only one Voice conversation runs at a time; a single Live conversation can last up to
  two hours.

### The honest cost

- Everything captured this way becomes part of your chat history and is retained under
  your ordinary data settings. Work with Apps content "may be used to improve model
  performance" unless you turn off *Improve the model for everyone* or use temporary chat;
  business plans (Team, Enterprise) are excluded by default.
- Page content read in the built-in browser is untrusted input. This is the prompt
  injection surface, and it is the reason the app asks per-website.
- Extra reach is bought with operating-system permissions: Accessibility, Screen & Audio
  Recording, microphone. That is the honest trade the deck names on slides 8 and 10.

### Model lineup

Per the shared brief facts: the flagship is **GPT-6 Astra**, with the **GPT-5.6** family
(Sol, Terra, Luna, Cyber) below it. The lecture's "GPT-4 capabilities" is two generations
stale. The help centre also confirms **GPT-6 Pro, powered by GPT-6 Astra** rolling out in
ChatGPT. Do not put a version number on a slide; say it aloud if you want to.

---

## What each review round changed

**Round 1 - the hostile reviewer.** Six findings, all fixed.
1. The definition mock (slide 2) was a generic chat exchange that would have suited any
   lecture in the course. Retagged the window "Over your work" and rewrote the prompt so
   it refers to a selection the app can see.
2. Slide 3's example was a code-debugging one, which is wrong for a lecture flagged
   no-code friendly. Replaced with a spreadsheet that is not adding up.
3. Slide 4's "a general tool with a coding mode" was a current-build fact about Codex
   being bundled, and off-audience. Replaced with "useful to anyone with a screen".
4. Slide 8 listed "the browser profile you use every day" as something out of reach -
   true, but too deep in the weeds. Replaced with "your screen when you have not asked".
5. Slide 9's caption stopped at "lands in your history"; extended it to name that it is
   stored under whatever data settings you already have, which is the actual consequence.
6. Layout: the captions on slides 5 and 6 were top-aligned at 1.60/1.62 against columns
   running to 4.68 and 4.96, leaving both slides visibly bottom-heavy on the right. Both
   moved down (2.56 and 2.60) to centre against the diagram they annotate.

**Round 2 - the student.** Five findings, all fixed. Read as a first-time viewer at 1.5x.
1. "permit it" in the slide 5 title was more formal than the step it describes. Now
   "summon it, point it, allow it", matching step 3's wording.
2. "captured as a picture" on slide 6 did not connect to the idea of a screenshot for
   someone who had not met the term. Now "as a picture of it".
3. Slide 6's caption opened "It never receives your computer", which parses badly. Now
   "It is never handed your whole machine."
4. "Your whole home folder" on slide 10 is jargon for a non-technical student. Now
   "Everything on your machine, to save a click".
5. Slide 8 said "operating system" where slide 5 said "your computer". Made consistent.
Titles read top to bottom as a complete story, so no title rewrites were needed.

**Round 3** (run because round 2 turned up more than two findings). Three findings.
1. Slide 2 had a bare role label with nothing beneath it, sitting directly above the
   "User" label - two stacked labels reading as clutter. Moved that text into the window
   tag instead.
2. Slide 7 had the same shape: a divider and a label with no content under them. Added the
   line the label was promising.
3. Slide 8's mock window was named "Access", which is abstract. Renamed "Permissions".

Lint is clean after every round: `11 slides, nothing to fix`.

---

## For James

1. **The lecture's biggest single error is the voice model, not the platform claim.**
   Roughly 1:48 to 3:41 - about a third of the runtime - teaches a workflow that no longer
   exists: end the voice chat, find it as a separate item in history, run a second session
   in a browser window alongside it. Voice now lives inside the chat, and only one
   conversation runs at a time. That whole segment needs re-shooting rather than patching.
2. **Decide how much of the new app you want in a Part 2 lecture.** The desktop app is now
   Chat + Work + Codex, and Codex is a developer tool. This lecture is flagged no-code
   friendly, so the deck deliberately says "useful to anyone with a screen" and never names
   Codex. If you want Work or Codex covered, it probably wants to be its own lecture rather
   than a paragraph here - your call, and it is worth checking against `agent-mode` and
   `scheduled-tasks`, which already carry some of that ground.
3. **Which app do you demo?** ChatGPT Classic matches the old footage and is simpler; the
   new app is where everything is going. My assumption in the deck is that you demo the new
   one, since slide 8's permission boundary and the built-in browser only exist there.
4. **Say the platform list aloud.** The deck says "one of several places it runs" by
   design. Worth naming on camera: macOS, Windows, iOS, Android, the web, the Chrome
   extension, and Atlas - and worth saying explicitly that the companion window is
   Option+Space on Mac *and* Alt+Space on Windows, since the original lecture implied Mac
   only.
5. **The permission demo is the strongest live moment available.** Handoff card 4 is "open
   the permissions and take one back". Granting Screen Recording, showing what gets
   attached, then revoking it and showing the same question go through with nothing
   attached makes the trade concrete in about forty seconds.
6. **Unverified, worth a glance on your own account:** whether "Work with Apps" still
   carries that exact name and is still macOS-only. The help article is dated 25 days ago
   and describes the Classic app; the new app's local-file access is documented separately
   and phrased differently ("Work in the desktop app can also use local files and desktop
   apps with your permission"). The principle on slide 6 holds either way, but do not name
   the feature on camera without checking the label.
