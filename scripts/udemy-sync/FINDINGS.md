# Udemy ↔ Repo Drift Findings

Issues discovered while reconciling Udemy lecture resources with notebooks in
this repo. Captured 2026-04-27 from `out/notebook_matches.json`.

## High priority

### 1. `dsypy.ipynb` typo — should be `dspy.ipynb`

- **Lecture:** `[44009372] Prompt Optimization with DSPy - Coding`
- **Section:** Prompt Optimization & Evals
- **Udemy resource:** Colab titled `dspy.ipynb`
  → https://colab.research.google.com/drive/1YBAo6IxnsVi_V7cyR_qz4Q86r-BxDgnr?usp=sharing
- **Repo file:** `prompt_optimization_and_evals/dsypy.ipynb` (note the typo: `dsypy`, not `dspy`)
- **Action:** rename `prompt_optimization_and_evals/dsypy.ipynb` → `prompt_optimization_and_evals/dspy.ipynb`. Confirm this is the notebook that backs the lecture (the repo also has `dspy_primer_with_every.ipynb`, which is a different artefact).

### 2. `chatgpt_chunking.ipynb` — referenced by Udemy, missing from repo

- **Lecture:** `[37093616] Overcoming the Token Limit in ChatGPT`
- **Section:** Standard Text Model Practices
- **Udemy resource:** Colab titled `chatgpt_chunking.ipynb`
  → https://colab.research.google.com/drive/1gP70RiT4LcSkiApHf9LJ2qYf3yxSFOxJ?usp=sharing
- **Repo file:** none
- **Action:** decide whether to (a) add `chatgpt_chunking.ipynb` to the repo (probably under `advanced_text_model_techniques/` or `standard_image_model_practices/`), or (b) replace the Udemy resource with whichever notebook actually backs this video.

### 3. DreamBooth basename mismatch (case + word splits)

| Udemy resource title                                  | Repo file                                                       |
| ----------------------------------------------------- | --------------------------------------------------------------- |
| `Product_DreamBooth_Stable_Diffusion.ipynb`           | `ai_image_model_projects/product_dream_booth_stable_diffusion.ipynb` |
| `Profile_Picture_DreamBooth_Stable_Diffusion.ipynb`   | `ai_image_model_projects/profile_picture_dream_booth_stable_diffusion.ipynb` |

- **Lectures:** `[37220440] Product Placement - Coding`, `[38468510] AI Profile Picture - Coding`
- **Why it didn't auto-match:** the matcher normalises by lowercasing and splitting on non-alphanumerics — `DreamBooth` becomes `dreambooth` (one token), but the repo file uses `dream_booth` (two tokens), so basenames differ.
- **Action:** either rename the repo files to `*_dreambooth_*.ipynb` (one-word) or update the Udemy resource titles to match the repo's `dream_booth` spacing. Pick one canonical spelling.

## Medium priority

### 4. `notebook.ipynb` — generic Colab default name

- **Lecture:** `[41237902] Making a Brand Logo`
- **Section:** AI Image Model Projects
- **Udemy resource:** Colab titled literally `notebook.ipynb` (Colab's default name)
  → https://colab.research.google.com/drive/1LmgcCJi5hoeC0YqQjzE9uggOmbGgQYTk?usp=sharing
- **Action:** open the Colab, rename it to something descriptive (e.g. `brand_logo_generation.ipynb`), and either upload that notebook to the repo or point the lecture at the existing one.

### 5. `dspy_primer_with_every.ipynb` and `dspy.ipynb` coexist

Once the typo in finding #1 is fixed there will be two DSPy notebooks in
`prompt_optimization_and_evals/`. Worth confirming each lecture points at the
right one, especially for the "DSPy Primer" lecture if there is one.

## Not actionable (informational)

| Resource           | Why we skip                                                                  |
| ------------------ | ---------------------------------------------------------------------------- |
| `Github Repository` (lecture 42525002) | Points at the repo root, not a notebook. Expected.                |
| `Github Folder` (lecture 55292971)     | Points at `building_ai_agents/building_a_coding_agent/` directory. Expected. |
| `ComfyUI_colab.ipynb` (lecture 46269705) | External Colab from `comfyanonymous/ComfyUI`, not in our repo. Expected. |

## Ambiguous matches (auto-picked, worth eyeballing)

These resolved to a unique-by-basename match but the basename appears in more
than one folder, so the matcher picked the first hit. All three look correct
on inspection, but flagging for sanity:

- `automating_product_descriptions.ipynb` (lecture 42387198) → `ai_text_model_projects/automating_product_descriptions.ipynb` (also exists at `vision/automating_product_descriptions.ipynb`)
- `ux_landing_page_analysis.ipynb` (lecture 42882572) → `ai_text_model_projects/ux_landing_page_analysis.ipynb` (also at `vision/ux_landing_page_analysis.ipynb`)
- `evaluation_metrics.ipynb` (lecture 41918608) → `evaluating_quality/evaluation_metrics.ipynb` (also at `prompt_optimization_and_evals/evaluation_metrics.ipynb`)
