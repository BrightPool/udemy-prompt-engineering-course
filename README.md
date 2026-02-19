# The Complete Prompt Engineering for AI Bootcamp (2026)

Source code and notebooks for the Udemy course. This README covers the **coding sections** with links to the relevant folders. Video-only sections (Introduction, Five Principles, Core Concepts, ChatGPT Deep Dive, Prompting Techniques, Midjourney, Claude, Google Veo3, Other AI Models & Tools, Resources & Next Steps) are taught entirely in the Udemy videos and have no corresponding code here.

---

## Course Sections (with Code)

1. [OpenAI Platform & API](#openai-platform--api)
2. [Embeddings and Vector Databases](#embeddings-and-vector-databases)
3. [Building AI Agents](#building-ai-agents)
4. [Advanced Retrieval Techniques](#advanced-retrieval-techniques)
5. [Advanced Prompting Techniques](#advanced-prompting-techniques)
6. [LangChain](#langchain)
7. [LangGraph](#langgraph)
8. [Text Generation Projects](#text-generation-projects)
9. [Flux AI & Fal](#flux-ai--fal)
10. [Image Generation Projects](#image-generation-projects)
11. [Evaluations & Testing](#evaluations--testing)
12. [Agent Architectures](#agent-architectures)
13. [Fine-Tuning](#fine-tuning)

---

### OpenAI Platform & API

Folder: [`openai_features_and_functionality/`](openai_features_and_functionality/)

Covers the OpenAI Responses API, streaming, token counting, rate limits, structured outputs, tool calling, and building a simple agent. All notebooks use the Responses API unless explicitly comparing it with the older Chat Completions API.

- Responses API & Messages
- Coding Notebook with Different OpenAI Services
- How to Count Tokens using tiktoken
- Managing The Message History
- What is Streaming?
- Rate Limits Retrying and How to Overcome These Problems
- Chat Completions vs Responses API
- Tool (Function) Calling
- Building a Simple Agent with Tools
- Parallelization of requests with Async OpenAI

### Embeddings and Vector Databases

Folder: [`embeddings_and_vector_databases/`](embeddings_and_vector_databases/)

Covers embeddings, vector search with FAISS, information retrieval, RAG with Supabase PGVector, and hybrid retrieval.

- Understanding Vector Embeddings
- Information Retrieval with Vector Databases
- RAG with Supabase PGVector
- Hybrid Retrieval

### Building AI Agents

Folder: [`building_ai_agents/`](building_ai_agents/)

Hands-on agent projects using the OpenAI Responses API.

- Multi-Source Customer Support Agent
- Web Research + Structured Report Agent
- Blog Post Generator Agent
- SQL + Data Analysis Agent
- Docs Watcher (OpenAI/Anthropic/Temporal release notes)
- Deep Research Agent
- Video Generation Agent

### Advanced Retrieval Techniques

Folder: [`advanced_retrieval_techniques/`](advanced_retrieval_techniques/)

BM25 lexical retrieval, query expansion, hybrid retrieval, Reciprocal Rank Fusion, HyDE, parent document retrieval, MMR, and retrieval evaluation metrics. All notebooks are standalone (no LangChain dependency).

- BM25: The Foundation of Lexical Search
- Hybrid Search - Combining Dense and Sparse Retrieval
- Query Expansion with LLMs
- RAG-Fusion and Reciprocal Rank Fusion
- HyDE and Parent Document Retrieval
- MMR and Retrieval Evaluation Metrics

### Advanced Prompting Techniques

Folders:
- [`proven_prompting_techniques/`](proven_prompting_techniques/) -- Role prompting, emotion prompting, in-context learning, self-consistency sampling
- [`advanced_text_model_techniques/`](advanced_text_model_techniques/) -- ReAct, prompt optimization, prompt caching, personas of thought

Notebooks:
- Role Prompting
- Emotion Prompting
- In Context Learning
- Self-Consistency Sampling
- Reason and Act (ReAct)
- Personas of Thought
- Prompt Optimization
- Structured Outputs for OpenAI
- Prompt Caching in Practice
- OpenAI Realtime - Example
- Semantic Caching
- Reasoning Models Deep Dive - Prompting o1 o3 and o4
- Advanced Reasoning Techniques - Graph of Thoughts and Skeleton-of-Thought

### LangChain

Folder: [`deep_dive_on_langchain/`](deep_dive_on_langchain/)

18 numbered notebooks covering the full LangChain stack.

- What Is LangChain?
- Installation
- Chat Models
- Chat Prompt Templates
- Streaming
- Output Parsers
- Summarizing Large Amounts of Text
- Document Loaders Text Splitting & Creating LangChain Documents
- Tagging Documents
- Tracing with LangSmith
- LangChain Hub - LangSmith
- LCEL - The Runnable Protocol
- LCEL - Chat Models itemgetter & RAG
- LCEL - Chat Message History & Memory
- LCEL - Creating Multiple Chains
- LCEL - Conditional Logic Branching & Merging
- LangChain Vector Databases + the Indexing API
- LCEL Configurable Fields
- LangChain Agents & Tools

### LangGraph

Folder: [`deep_dive_on_langgraph/`](deep_dive_on_langgraph/)

- Introduction To LangGraph
- Simple LangGraph Flows
- Tool Usage and Persistence
- Human In The Loop
- Manually Updating The State
- Customizing State in LangGraph
- Time Travel
- RAG in LangGraph (Self Corrective RAG)
- Extra Content: Advanced Branching/Subgraphs

### Text Generation Projects

Folders:
- [`ai_text_model_projects/`](ai_text_model_projects/) -- Coding projects
- [`vision/`](vision/) -- Vision-based projects

Notebooks:
- Progressive Summarization
- Summarizing An Entire Book
- Review Classification
- AI Blog Post Generation
- Text To Speech using OpenAI
- Using LangChain + Llama3 Locally with LMStudio
- Transcribing audio from a Youtube Video
- Fine-Tuning on Writing Style
- Social Media Posting
- Reverse Engineering a Publication
- Building a GPT wrapper with Flask and HTMX
- Qualitative Analysis
- Claim Detection
- OpenAI Realtime - Twilio Example
- Automating Product Descriptions via GPT-V
- Automating UX Landing Page Analysis via GPT-V
- Natural Language to SQL Query Builder
- Customer Service Chatbot with Escalation

### Flux AI & Fal

Folder: [`standard_image_model_practices/`](standard_image_model_practices/)

- Text to Image with Flux
- Async Text to Image with Flux
- X/Y/Z Prompt Grids
- Image Upscaling with Clarity
- Image to Image with Flux
- Image Editing with Flux.Kontext
- Advanced Inpainting with Flux
- Draw Image Mask with Gradio
- Segment Anything Masking
- Advanced Outpainting with Flux
- Advanced Consistent Characters
- ControlNet with Flux Pro
- Fine-Tuning with Flux Lora
- Image to Video with Kling AI

### Image Generation Projects

Folder: [`ai_image_model_projects/`](ai_image_model_projects/)

- Product Placement
- Tagging Ad Creative
- AI Profile Picture
- Nano Banana

### Evaluations & Testing

Folders:
- [`prompt_optimization_and_evals/`](prompt_optimization_and_evals/) -- DSPy, Sammo, evaluation frameworks
- [`evaluating_quality/`](evaluating_quality/) -- LLM and image model evaluation strategies

Notebooks:
- Prompt Optimization with DSPy
- Eval metrics with DSPy
- Prompt Optimization: 5 Principles of Prompting
- Prompt Optimization: Advanced
- Sammo - Introduction
- Sammo - Metaprompting
- Sammo - Testing and Optimization
- LLM & Image Model Performance: Advanced Evaluation Strategies

### Agent Architectures

Folders:
- [`agent_architectures/`](agent_architectures/) -- Prompt chaining, routing, parallelization, orchestrator-workers, agents, evaluator-optimizer
- [`advanced_concepts/`](advanced_concepts/) -- Agent swarms, self-correction, knowledge graphs

Notebooks:
- Prompt Chaining
- Routing
- Parallelization
- LLM Orchestrators
- Agents
- Mixture of Experts - Aggregator
- Evaluator Optimizer
- MCP - Building Custom MCP Servers in Python
- OpenAI Agents SDK - Introduction
- OpenAI Agents SDK - Building Agents with Persistent Memory
- OpenAI Agents SDK - Agent Handoffs and Multi-Agent Coordination

### Fine-Tuning

- QLoRA and LoRA Fine-Tuning - Parameter-Efficient Methods

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
