# Model Gateways and Model Agnostic Frameworks

Seven slides for Part 10, Model Gateways. The editable deck matches the supplied course theme and includes speaker notes, official links and an editable comparison table.

## Recording guide

1. Introduce a gateway as a shared entry point between an application and model providers.
2. Separate a model from the provider hosting it. A model can be served by multiple providers.
3. Explain OpenRouter's unified API, model choice and usage reporting. Hosted open-weight models are not running locally.
4. Distinguish the gateway from LangChain and the Vercel AI SDK. Vercel AI Gateway is a separate product.
5. Explain provider fallback versus model fallback, then show price and capability filters.
6. Show the returned account charge and generation metadata and explain that your application owns customer credit conversion and accounting.
7. Open the Python feature notebook. Show setup, the live model catalogue, the two-model comparison and routing. Save deeper optional demos for their own walkthroughs.

Aim for about four to five minutes of explanation, then demonstrate the selected cells at a comfortable pace. The complete feature notebook is a reference, not a script to cover in one short video.

## Companion notebook

`model_gateways/openrouter_features_and_agent.ipynb`

Run from the top. Optional features are disabled by default and use separate switches. Model capabilities and prices are fetched. Core calls incur API charges. Media and hosted tools can add separate charges.

## Links and publication

The Colab link in the deck points to the new notebook on GitHub's `main` branch. It will work after the new file is committed and pushed; publication has not been requested.

Native Google Slides publication is pending installation and connection of the Google Drive plugin. This package currently contains the prepared local editable deck and slide previews. It has been checked locally; Google Slides conversion has not been performed or checked.

## Sources

- https://openrouter.ai/docs/quickstart
- https://openrouter.ai/models
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://openrouter.ai/docs/guides/routing/model-fallbacks
- https://openrouter.ai/docs/guides/community/langchain
- https://openrouter.ai/docs/guides/community/vercel-ai-sdk
- https://vercel.com/docs/ai-gateway
- https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation

Official OpenRouter logo: https://openrouter.ai/brand
