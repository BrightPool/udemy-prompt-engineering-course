# The Complete Prompt Engineering for AI Bootcamp (2026)

Source code and notebooks for the Udemy course. Each folder below maps to a section of the course. Sections without code (ChatGPT Deep Dive, Midjourney, Claude, etc.) are taught directly in the videos and don't have a corresponding folder here.

## Course Sections (Code Folders)

### Section 6: OpenAI Platform & API

Folder: [`openai_features_and_functionality/`](openai_features_and_functionality/)

Covers the OpenAI Responses API, streaming, token counting, rate limits, structured outputs, tool calling, and building a simple agent. All notebooks use the Responses API unless explicitly comparing it with the older Chat Completions API.

### Section 7: Vector Embeddings & RAG

Folder: [`embeddings_and_vector_databases/`](embeddings_and_vector_databases/)

Covers embeddings, vector search with FAISS, and information retrieval fundamentals.

### Section 8: Advanced Retrieval Techniques

Folder: [`advanced_retrieval_techniques/`](advanced_retrieval_techniques/)

BM25 lexical retrieval, query expansion, hybrid retrieval, Reciprocal Rank Fusion, HyDE, parent document retrieval, MMR, and retrieval evaluation metrics. All notebooks are standalone (no LangChain dependency).

### Section 9: Advanced Prompting Techniques

Folders:
- [`proven_prompting_techniques/`](proven_prompting_techniques/) -- Role prompting, emotion prompting, chain of thought, in-context learning, self-consistency sampling
- [`advanced_text_model_techniques/`](advanced_text_model_techniques/) -- ReAct, prompt optimization, prompt caching, recursive reprompting and revision

### Section 10: LangChain

Folder: [`deep_dive_on_langchain/`](deep_dive_on_langchain/)

18 numbered notebooks covering installation, chat models, prompt templates, streaming, output parsers, summarization chains, document loaders, text splitting, tagging, LangSmith tracing, LangChain Hub, LCEL (runnable interface, RAG, memory, multiple chains, branching/merging), vector stores with the Indexing API, configurable fields, and agents with tools.

### Section 11: LangGraph

Folder: [`deep_dive_on_langgraph/`](deep_dive_on_langgraph/)

6 numbered notebooks: simple LangGraph flows, tool usage and persistence, human in the loop, manually updating state, customizing state, and time travel.

### Section 12: Text Generation Projects

Folder: [`ai_text_model_projects/`](ai_text_model_projects/)

Projects include progressive summarization, summarizing large documents, review classification, AI blog post generation, text to speech, transcribing audio from YouTube, fine-tuning on writing style, and running Llama 3 locally with LM Studio.

### Section 12 (Vision Projects)

Folder: [`vision/`](vision/)

Automating product descriptions and UX landing page analysis using GPT vision capabilities.

### Section 15: Stable Diffusion

Folder: [`advanced_image_model_techniques/`](advanced_image_model_techniques/)

DreamBooth fine-tuning and Stable Diffusion textual inversion training.

### Section 16: Image Generation Projects

Folder: [`ai_image_model_projects/`](ai_image_model_projects/)

Product placement with DreamBooth, AI profile pictures, Stable Diffusion projects, and creative image generation.

### Section 17: Evaluations & Testing

Folders:
- [`prompt_optimization_and_evals/`](prompt_optimization_and_evals/) -- DSPy, Sammo (intro, metaprompting, optimization), social media post generation, FunEval, evaluation metrics
- [`evaluating_quality/`](evaluating_quality/) -- LLM and image model evaluation strategies

### Section 18: Agent Architectures

Folders:
- [`agent_architectures/`](agent_architectures/) -- Prompt chaining, routing, parallelization, orchestrator-workers, agents, evaluator-optimizer pattern
- [`advanced_concepts/`](advanced_concepts/) -- Agent swarms, self-correction, knowledge graphs

### Section 19: Building AI Agents

Folder: [`building_ai_agents/`](building_ai_agents/)

Hands-on agent projects using the OpenAI Responses API: multi-source customer support agent (SQLite + knowledge base), web research with structured reports, blog post generator (planner/writer/critic with reasoning models), SQL data analysis agent (text-to-SQL), docs watcher (long-running stateful loops), deep research agent, and video generation with Sora.

---

## Setup

### Prerequisites

- Python 3.10+
- Jupyter (or VS Code with the Jupyter extension)

### Environment Variables

Create a `.env` file in the project root with the API keys you need:

```bash
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
TAVILY_API_KEY=tvly-xxx
LANGCHAIN_API_KEY=lsv2_xxx
```

Not every notebook requires all keys. The OpenAI key covers the majority of the course.

### Installation

```bash
pip install -r requirements.txt
```

### Secret Scanning

```bash
# Install gitleaks for pre-commit secret scanning
brew install gitleaks
pip install pre-commit
pre-commit install

# Run a manual scan
gitleaks detect --source="." --report-path="gitleaks-report.json"
```
