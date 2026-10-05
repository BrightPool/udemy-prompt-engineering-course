# Local Models with LM Studio - recording notes

Deck: `local-models-lm-studio.pptx` (4 slides), built by `build_local_models_lm_studio.py`.
Pairs with the rewritten LM Studio notebook in `ai_text_model_projects/`.

## Speaking notes

1. **Local Models with LM Studio**: run a model on your own machine and call it like a cloud API.
2. **A model that runs on your own machine**: why (prompts stay local, no per-token bill, offline, free to repeat experiments) and what you give up (smaller, less capable models, hardware limits, you manage downloads and updates). Reach for local when privacy or volume matters more than peak quality.
3. **How it works - same SDK, different address**: LM Studio exposes an OpenAI-compatible server on localhost. Change `base_url` and pass any placeholder `api_key`, then use the loaded model's identifier as `model`. Everything else in your code stays the same.
4. **Handoff**: load a model, start the server, change the base URL and run the notebook.

Say aloud, not on slides: the default port (1234) can be changed in LM Studio's server settings; which model you load depends on your RAM.

## Review rounds

- Round 1 (hostile): "Your data never leaves the device" overclaimed, changed to "Prompts stay on your machine". The code caption said only two arguments change, which is false (the model name must match the local model), rewritten. Layout: code started at 1.66" while the panels slide started at 1.56", aligned both to 1.56". Panels trailed dead space, shortened to fit and pulled the caption up. Replaced deckkit `compare()` (its row glyph is an em dash) with a local `panels()` helper using a bullet dot.
- Round 2 (student): "open-weight" in the subtitle was never defined, replaced with "AI model". The code caption wrapped to two lines, shortened. Titles read top to bottom tell the story (why local, how to connect, do it live).
