<script lang="ts">
    import { fly, slide } from "svelte/transition";
    import {
        Loader2,
        Send,
        Database,
        Wrench,
        ChevronDown,
        ChevronRight,
        Bot,
    } from "lucide-svelte";
    import { marked } from "marked";
    import { sendSandboxPrompt, type SandboxResponse } from "../api";
    import type { Domain } from "../types";

    export let category: Domain;

    let prompt = "";
    let loading = false;
    let messages: {
        role: "user" | "model";
        content: string;
        details?: {
            tools?: string[];
            rag?: { title: string; content: string }[];
            latency?: number;
        };
    }[] = [];

    let expandedDetails: Set<number> = new Set();

    function parseMarkdown(content: string): string {
        return marked.parse(content) as string;
    }

    function toggleDetails(index: number) {
        if (expandedDetails.has(index)) {
            expandedDetails.delete(index);
            expandedDetails = expandedDetails; // trigger update
        } else {
            expandedDetails.add(index);
            expandedDetails = expandedDetails; // trigger update
        }
    }

    async function handleSubmit() {
        if (!prompt.trim() || loading) return;

        const currentPrompt = prompt;
        prompt = "";
        loading = true;

        // Add user message
        messages = [...messages, { role: "user", content: currentPrompt }];

        try {
            const response: SandboxResponse = await sendSandboxPrompt({
                prompt: currentPrompt,
                namespace: category,
                history: messages.map((m) => ({
                    role: m.role,
                    content: m.content,
                })),
            });

            // Add model response
            messages = [
                ...messages,
                {
                    role: "model",
                    content: response.output,
                    details: {
                        tools: response.tools_used,
                        rag: response.rag_context,
                        latency: response.latency_ms,
                    },
                },
            ];

            // Auto-expand details if tools or RAG were used
            if (
                response.tools_used.length > 0 ||
                response.rag_context.length > 0
            ) {
                expandedDetails.add(messages.length - 1);
                expandedDetails = expandedDetails;
            }
        } catch (error) {
            console.error("Sandbox Error:", error);
            messages = [
                ...messages,
                {
                    role: "model",
                    content:
                        "Sorry, I encountered an error. Please ensure the backend is running and configured correctly.",
                },
            ];
        } finally {
            loading = false;
        }
    }
</script>

<div class="sandbox-container">
    <div class="messages-area">
        {#if messages.length === 0}
            <div class="empty-state">
                <Bot size={48} class="empty-icon" />
                <h3>Sandbox Mode</h3>
                <p>
                    Ask anything about {category}. I'll use RAG to understand
                    context and remote MCP tools to fetch real-time data.
                </p>
                <div class="examples">
                    <p>Try asking:</p>
                    <ul>
                        {#if category === "travel"}
                            <li>
                                "Find flights from London to Paris next week"
                            </li>
                            <li>"What are the best hotels in Tokyo?"</li>
                            <li>"Plan a weekend trip to Rome"</li>
                        {:else if category === "jobs"}
                            <li>"Find software engineer jobs in Berlin"</li>
                            <li>"Analyze my resume fit for this role..."</li>
                        {:else}
                            <li>"What's trending on Twitter properly?"</li>
                        {/if}
                    </ul>
                </div>
            </div>
        {/if}

        {#each messages as msg, i}
            <div
                class="message-wrapper {msg.role}"
                in:fly={{ y: 20, duration: 300 }}
            >
                <div class="avatar">
                    {#if msg.role === "user"}
                        <div class="user-avatar">U</div>
                    {:else}
                        <div class="model-avatar">
                            <Bot size={16} />
                        </div>
                    {/if}
                </div>

                <div class="message-content">
                    {#if msg.role === "model"}
                        <div class="markdown-body">
                            {@html parseMarkdown(msg.content)}
                        </div>

                        {#if msg.details && (msg.details.tools?.length > 0 || msg.details.rag?.length > 0)}
                            <div class="details-toggle">
                                <button
                                    class="toggle-btn"
                                    on:click={() => toggleDetails(i)}
                                >
                                    {#if expandedDetails.has(i)}
                                        <ChevronDown size={14} />
                                        Hide Execution Details
                                    {:else}
                                        <ChevronRight size={14} />
                                        Show Execution Details ({msg.details
                                            .tools?.length || 0} tools, {msg
                                            .details.rag?.length || 0} docs)
                                    {/if}
                                </button>
                            </div>

                            {#if expandedDetails.has(i)}
                                <div class="execution-details" transition:slide>
                                    {#if msg.details.latency}
                                        <div class="latency-badge">
                                            ⏱️ {msg.details.latency.toFixed(
                                                0,
                                            )}ms
                                        </div>
                                    {/if}

                                    {#if msg.details.rag?.length > 0}
                                        <div class="detail-section">
                                            <h4>
                                                <Database size={14} /> RAG Context
                                            </h4>
                                            {#each msg.details.rag as doc}
                                                <div
                                                    class="rag-item"
                                                    title={doc.content}
                                                >
                                                    <span class="rag-title"
                                                        >📄 {doc.title}</span
                                                    >
                                                    <!-- <span class="rag-snippet">{doc.content.slice(0, 100)}...</span> -->
                                                </div>
                                            {/each}
                                        </div>
                                    {/if}

                                    {#if msg.details.tools?.length > 0}
                                        <div class="detail-section">
                                            <h4>
                                                <Wrench size={14} /> Tools Executed
                                            </h4>
                                            {#each msg.details.tools as tool}
                                                <div class="tool-item">
                                                    <span class="tool-name"
                                                        >🔧 {tool}</span
                                                    >
                                                </div>
                                            {/each}
                                        </div>
                                    {/if}
                                </div>
                            {/if}
                        {/if}
                    {:else}
                        <p>{msg.content}</p>
                    {/if}
                </div>
            </div>
        {/each}

        {#if loading}
            <div class="loading-indicator">
                <Loader2 class="spin" size={20} />
                <span>Thinking with RAG + MCP...</span>
            </div>
        {/if}
    </div>

    <div class="input-area">
        <div class="input-wrapper">
            <input
                type="text"
                bind:value={prompt}
                placeholder="Ask a question requiring tools..."
                on:keydown={(e) =>
                    e.key === "Enter" && !loading && handleSubmit()}
                disabled={loading}
            />
            <button
                class="send-btn"
                on:click={handleSubmit}
                disabled={loading || !prompt.trim()}
            >
                {#if loading}
                    <Loader2 class="spin" size={18} />
                {:else}
                    <Send size={18} />
                {/if}
            </button>
        </div>
    </div>
</div>

<style>
    .sandbox-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        max-width: 900px;
        margin: 0 auto;
    }

    .messages-area {
        flex: 1;
        overflow-y: auto;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .empty-state {
        text-align: center;
        margin-top: 4rem;
        color: rgba(255, 255, 255, 0.6);
    }

    .empty-icon {
        color: rgba(99, 102, 241, 0.8);
        margin-bottom: 1rem;
    }

    .examples {
        margin-top: 2rem;
        text-align: left;
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        display: inline-block;
    }

    .examples ul {
        margin: 0.5rem 0 0 1.2rem;
        color: rgba(255, 255, 255, 0.8);
    }

    .message-wrapper {
        display: flex;
        gap: 1rem;
        max-width: 85%;
    }

    .message-wrapper.user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }

    .message-wrapper.model {
        align-self: flex-start;
    }

    .avatar {
        flex-shrink: 0;
        width: 32px;
        height: 32px;
    }

    .user-avatar,
    .model-avatar {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.8rem;
    }

    .user-avatar {
        background: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .model-avatar {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
    }

    .message-content {
        background: rgba(30, 30, 45, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .user .message-content {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.2);
    }

    /* Execution Details */
    .details-toggle {
        margin-top: 0.75rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 0.5rem;
    }

    .toggle-btn {
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.75rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0;
    }

    .toggle-btn:hover {
        color: rgba(255, 255, 255, 0.8);
    }

    .execution-details {
        margin-top: 0.75rem;
        background: rgba(20, 20, 30, 0.5);
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.8rem;
    }

    .detail-section {
        margin-bottom: 0.75rem;
    }

    .detail-section:last-child {
        margin-bottom: 0;
    }

    .detail-section h4 {
        margin: 0 0 0.5rem 0;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .rag-item,
    .tool-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.35rem 0.6rem;
        border-radius: 4px;
        margin-bottom: 0.25rem;
        border-left: 2px solid rgba(99, 102, 241, 0.5);
    }

    .rag-title {
        color: #c7d2fe;
    }

    .tool-name {
        color: #a5b4fc;
        font-family: monospace;
    }

    .latency-badge {
        display: inline-block;
        background: rgba(0, 0, 0, 0.3);
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
        color: #94a3b8;
        font-size: 0.7rem;
        margin-bottom: 0.5rem;
    }

    /* Input Area */
    .input-area {
        padding: 1.5rem 2rem;
        background: rgba(20, 20, 25, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .input-wrapper {
        display: flex;
        gap: 0.75rem;
        background: rgba(40, 40, 50, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 12px;
    }

    input {
        flex: 1;
        background: transparent;
        border: none;
        padding: 0.75rem;
        color: white;
        font-size: 0.95rem;
    }

    input:focus {
        outline: none;
    }

    .send-btn {
        background: #6366f1;
        color: white;
        border: none;
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
    }

    .send-btn:hover:not(:disabled) {
        background: #4f46e5;
    }

    .send-btn:disabled {
        background: rgba(99, 102, 241, 0.5);
        cursor: not-allowed;
    }

    .spin {
        animation: spin 1s linear infinite;
    }

    .loading-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: rgba(255, 255, 255, 0.5);
        margin: 1rem 0 1rem 2rem;
        font-size: 0.9rem;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>
