# Custom MCP Servers in ChatGPT - recording notes

Deck: `custom-mcp-servers.pptx` (5 slides), built by `build_custom_mcp_servers.py`.

## Purpose

This is the short principles half of a live demonstration. It explains the benefit of
connecting a custom MCP server without tying the recording to a menu layout.

## Speaking notes

1. **Custom MCP Servers in ChatGPT**
   - A custom MCP server gives ChatGPT a route into a tool or data source that you choose.
   - The connection changes what ChatGPT can reach, not the underlying model.
2. **A live connection to capabilities you choose**
   - The server exposes a limited set of capabilities, such as reading data or creating a ticket.
   - You ask in normal language. ChatGPT decides whether one of those capabilities fits the request.
3. **The server describes what ChatGPT can call**
   - On connection, ChatGPT discovers the advertised tools and their inputs.
   - The server performs the operation and returns a result to the conversation.
4. **Your own systems become part of the conversation**
   - The main benefit is personalisation through reach: your own data and workflows can sit behind the chat.
   - The cost is trust. A connection can only be safe when its tools and permissions are appropriate.
5. **Live handoff**
   - Connect one trusted server, inspect the discovered tools, run one request and verify the external result.

## Current demo path to check before recording

OpenAI's documentation currently describes enabling Developer mode, adding the MCP
connection, reviewing its discovered tools and testing it in a new conversation. The UI
can move, so confirm this path in your own account immediately before filming.

## Sources checked on 2026-09-15

- https://developers.openai.com/plugins/concepts/mcp-server
- https://developers.openai.com/plugins/deploy/connect-chatgpt
- https://developers.openai.com/plugins/guides/security-privacy

## Review rounds

- Round 1, hostile reviewer: reduced the lesson to one definition, one mechanism and one benefit slide. Added the failure mode and trust boundary so the deck does not read as marketing. The first render left the mechanism caption stranded, so the connection loop now fills and explains that space.
- Round 2, student: defined a server through its exposed capabilities before using the term "tool" in the mechanism. Kept the final slide focused on the exact live sequence.
