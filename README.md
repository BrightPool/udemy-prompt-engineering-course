# The Complete Prompt Engineering for AI Bootcamp (2026)

This repository is the notebook companion for the coding portions of The Complete Prompt Engineering for AI Bootcamp (2026) on Udemy.

It is built around Jupyter notebooks, small example apps, prompt files, datasets, screenshots, and diagrams rather than a single installable Python package. At the time of writing, the repo contains 248 notebooks covering prompt engineering, OpenAI workflows, retrieval, agents, LangChain, LangGraph, evaluation, vision, and image generation.

## What This Repo Is For

- Course students who want the code from the hands-on lectures
- Developers who want practical prompt engineering and LLM application examples
- Teams looking for reference notebooks for OpenAI APIs, RAG, agent patterns, and eval workflows

## Important Context

This repository does not mirror every lecture one-to-one.

The full course includes non-coding lessons, platform walkthroughs, and conceptual material that live mainly in video. The repo is strongest for the coding-heavy sections of the curriculum, especially:

- OpenAI API workflows
- Advanced prompting techniques
- Retrieval, embeddings, and RAG
- Agent design and orchestration
- LangChain and LangGraph
- Prompt optimization and evaluations
- Vision and image-model projects

## Recommended Starting Points

If you are new to the repo, use one of these paths:

- OpenAI foundations: [openai_features_and_functionality/chat_completions_vs_responses_api.ipynb](openai_features_and_functionality/chat_completions_vs_responses_api.ipynb), [openai_features_and_functionality/responses_api_and_messages.ipynb](openai_features_and_functionality/responses_api_and_messages.ipynb), [openai_features_and_functionality/structured_outputs_using_openai.ipynb](openai_features_and_functionality/structured_outputs_using_openai.ipynb), [openai_features_and_functionality/tool_calling.ipynb](openai_features_and_functionality/tool_calling.ipynb)
- Prompt engineering techniques: [advanced_text_model_techniques/few_shot_learning.ipynb](advanced_text_model_techniques/few_shot_learning.ipynb), [advanced_text_model_techniques/chain_of_thought.ipynb](advanced_text_model_techniques/chain_of_thought.ipynb), [advanced_text_model_techniques/self_consistency_sampling.ipynb](advanced_text_model_techniques/self_consistency_sampling.ipynb), [advanced_text_model_techniques/prompt_optimization.ipynb](advanced_text_model_techniques/prompt_optimization.ipynb)
- Retrieval and RAG: [retrieval_embeddings_and_vector_databases/introduction_to_retrieval.ipynb](retrieval_embeddings_and_vector_databases/introduction_to_retrieval.ipynb), [retrieval_embeddings_and_vector_databases/understanding_vector_embeddings.ipynb](retrieval_embeddings_and_vector_databases/understanding_vector_embeddings.ipynb), [retrieval_embeddings_and_vector_databases/retrieval_augmented_generation_vector_database.ipynb](retrieval_embeddings_and_vector_databases/retrieval_augmented_generation_vector_database.ipynb), [retrieval_embeddings_and_vector_databases/introduction_to_hybrid_retrieval_with_sql_filtering_&_embeddings.ipynb](retrieval_embeddings_and_vector_databases/introduction_to_hybrid_retrieval_with_sql_filtering_&_embeddings.ipynb)
- Agents: [building_ai_agents/multi_source_customer_support_agent.ipynb](building_ai_agents/multi_source_customer_support_agent.ipynb), [building_ai_agents/introduction_to_openai_ai_agents_sdk.ipynb](building_ai_agents/introduction_to_openai_ai_agents_sdk.ipynb), [building_ai_agents/blog_post_generator_agent.ipynb](building_ai_agents/blog_post_generator_agent.ipynb)
- LangGraph: [deep_dive_on_langgraph/1_simple_langgraph.ipynb](deep_dive_on_langgraph/1_simple_langgraph.ipynb) through [deep_dive_on_langgraph/6_time_travel.ipynb](deep_dive_on_langgraph/6_time_travel.ipynb)
- Evals and optimization: [prompt_optimization_and_evals/social_media_posts.ipynb](prompt_optimization_and_evals/social_media_posts.ipynb), [prompt_optimization_and_evals/evaluation_metrics.ipynb](prompt_optimization_and_evals/evaluation_metrics.ipynb), [prompt_optimization_and_evals/dspy-primer-with-every.ipynb](prompt_optimization_and_evals/dspy-primer-with-every.ipynb)

## Repo Map

| Area | Folders | What you'll find |
| --- | --- | --- |
| Core prompting and OpenAI | `openai_features_and_functionality/`, `advanced_text_model_techniques/` | Responses API, structured outputs, tool calling, streaming, async requests, few-shot prompting, ReAct, self-consistency, prompt optimization |
| Retrieval and agents | `retrieval_embeddings_and_vector_databases/`, `advanced_retrieval_techniques/`, `building_ai_agents/`, `agent_architectures/` | Embeddings, hybrid retrieval, retriever evaluation, support agents, OpenAI Agents SDK, orchestration patterns |
| Framework deep dives | `deep_dive_on_langchain/`, `deep_dive_on_langgraph/` | LangChain chat models, LCEL, vectorstores, agents, LangGraph state, persistence, human-in-the-loop, RAG, streaming |
| Projects and evals | `ai_text_model_projects/`, `prompt_optimization_and_evals/`, `evaluating_quality/` | Blog generation, long-document summarization, transcription, text-to-speech, realtime voice, DSPy, SAMMO, eval metrics |
| Vision and image models | `vision/`, `advanced_image_model_techniques/`, `ai_image_model_projects/`, `standard_image_model_practices/` | Multimodal analysis, product descriptions, FLUX/FAL image workflows, older Stable Diffusion and DreamBooth projects, placeholder image-practices folder |
| Supporting assets | `building_ai_agents/resources/`, `images/`, `docs/` | Sample datasets, prompt files, screenshots, architecture diagrams, and internal planning or audit material |

## Running The Notebooks

Most notebooks are designed to be opened in Jupyter or Google Colab.

For local use, a minimal setup looks like this:

```bash
python -m venv .venv
source .venv/bin/activate
pip install jupyterlab
jupyter lab
```

Notes:

- Many notebooks install additional dependencies inline with `%pip install`
- There is no single repo-wide `requirements.txt` or `pyproject.toml` for every notebook
- Most notebooks expect `OPENAI_API_KEY`
- Many notebooks will prompt for missing credentials with `getpass` if they are not already set in your environment

## Credentials And External Services

Do not commit API keys or secrets to git.

Most notebooks can be run with just `OPENAI_API_KEY`, but some sections need extra services:

- `ANTHROPIC_API_KEY` for some prompt-caching comparisons
- `SUPABASE_URL` and `SUPABASE_KEY` for pgvector examples
- `LANGCHAIN_API_KEY` and `TAVILY_API_KEY` for some agent and tracing workflows
- `FAL_KEY` for several FLUX image-generation notebooks
- Twilio plus ngrok for the realtime voice example in `ai_text_model_projects/openai_realtime_example_with_twilio/`
- Hugging Face or Google Cloud credentials for some older image-model project notebooks

Use environment variables or your preferred local secret manager. If you use 1Password CLI, inject secrets locally rather than storing them in tracked files.

## Notes On Repo Coverage

Some folders are more complete than others:

- `deep_dive_on_langgraph/` is a structured sequence and works well as a guided learning track
- `deep_dive_on_langchain/` is richer as a library of concepts than as a strict linear path
- `building_ai_agents/resources/` contains the datasets, prompts, and knowledge-base files used by the agent notebooks
- `ai_text_model_projects/openai_realtime_example_with_twilio/` is a standalone example app with its own [README](ai_text_model_projects/openai_realtime_example_with_twilio/README.md) and pinned [requirements.txt](ai_text_model_projects/openai_realtime_example_with_twilio/requirements.txt)
- `standard_image_model_practices/` is currently just a placeholder and should not be treated as a populated section
- Several vision and image notebooks depend on external assets, uploads, or cloud credentials and are not fully self-contained after clone

## For Contributors

If you are maintaining or updating the repo, the existing hygiene tools are still useful:

```bash
brew install gitleaks
pip install pre-commit
pre-commit install
gitleaks detect --source="." --report-path="gitleaks-report.json"
```

## Suggested Learning Paths

If you want a more deliberate progression:

1. OpenAI and prompting: `openai_features_and_functionality/` -> `advanced_text_model_techniques/`
2. Retrieval: `retrieval_embeddings_and_vector_databases/` -> `advanced_retrieval_techniques/`
3. Agents: `building_ai_agents/` -> `agent_architectures/`
4. Frameworks: `deep_dive_on_langchain/` and `deep_dive_on_langgraph/`
5. Applied projects: `ai_text_model_projects/`, `prompt_optimization_and_evals/`, `vision/`, `advanced_image_model_techniques/`

If you are following the Udemy course, use the videos for the full teaching sequence and use this repo as the coding companion.
