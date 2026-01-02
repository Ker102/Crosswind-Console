<script lang="ts">
    import ToolSelector from "./ToolSelector.svelte";
    import DynamicForm from "./DynamicForm.svelte";

    interface FormField {
        name: string;
        type: "text" | "number" | "date" | "select" | "boolean";
        label: string;
        required: boolean;
        description?: string;
        default?: any;
        options?: string[];
        min?: number;
        max?: number;
    }

    interface DynamicFormSchema {
        toolName: string;
        serverName: string;
        description?: string;
        fields: FormField[];
    }

    // State
    let selectedServer = "";
    let selectedTool = "";
    let formSchema: DynamicFormSchema | null = null;
    let loadingSchema = false;
    let executing = false;
    let result: any = null;
    let error: string | null = null;

    const API_BASE = "http://localhost:8000";

    async function handleToolSelect(
        event: CustomEvent<{ server: string; tool: string }>,
    ) {
        const { server, tool } = event.detail;
        selectedServer = server;
        selectedTool = tool;

        // Fetch form schema
        loadingSchema = true;
        formSchema = null;
        result = null;
        error = null;

        try {
            const res = await fetch(
                `${API_BASE}/api/mcp/tools/${server}/${tool}/form`,
            );
            if (!res.ok) throw new Error("Failed to fetch form schema");
            formSchema = await res.json();
        } catch (e: any) {
            error = e.message;
        } finally {
            loadingSchema = false;
        }
    }

    async function handleSubmit(event: CustomEvent<Record<string, any>>) {
        const arguments_ = event.detail;

        executing = true;
        result = null;
        error = null;

        try {
            const res = await fetch(
                `${API_BASE}/api/mcp/tools/${selectedServer}/${selectedTool}/execute`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(arguments_),
                },
            );

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Execution failed");
            }

            result = await res.json();
        } catch (e: any) {
            error = e.message;
        } finally {
            executing = false;
        }
    }
</script>

<div class="detailed-form-mode">
    <div class="panel tool-panel">
        <h2>🔧 Select Tool</h2>
        <ToolSelector
            bind:selectedServer
            bind:selectedTool
            loading={executing}
            on:select={handleToolSelect}
        />
    </div>

    <div class="panel form-panel">
        <h2>📝 Configure</h2>
        {#if loadingSchema}
            <div class="loading">
                <span class="spinner"></span>
                Loading form...
            </div>
        {:else if error && !formSchema}
            <div class="error-box">
                <strong>Error:</strong>
                {error}
            </div>
        {:else}
            <DynamicForm
                schema={formSchema}
                loading={executing}
                on:submit={handleSubmit}
            />
        {/if}
    </div>

    <div class="panel result-panel">
        <h2>📊 Result</h2>
        {#if executing}
            <div class="loading">
                <span class="spinner"></span>
                Executing tool...
            </div>
        {:else if error && result === null}
            <div class="error-box">
                <strong>Execution Error:</strong>
                {error}
            </div>
        {:else if result}
            <div class="result-content">
                {#if result.success}
                    {#each result.result as content}
                        {#if content.type === "text"}
                            <pre class="result-text">{content.text}</pre>
                        {:else}
                            <pre class="result-data">{JSON.stringify(
                                    content.data,
                                    null,
                                    2,
                                )}</pre>
                        {/if}
                    {/each}
                {:else}
                    <div class="error-box">Tool returned an error</div>
                {/if}
            </div>
        {:else}
            <div class="placeholder">
                <p>Select a tool and fill the form to see results</p>
            </div>
        {/if}
    </div>
</div>

<style>
    .detailed-form-mode {
        display: grid;
        grid-template-columns: 1fr 1fr 1.2fr;
        gap: 1.5rem;
        padding: 1.5rem;
        min-height: 600px;
    }

    .panel {
        background: rgba(15, 15, 25, 0.9);
        border: 1px solid rgba(100, 100, 150, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }

    .panel h2 {
        margin: 0 0 1.25rem 0;
        color: #ddd;
        font-size: 1.1rem;
        font-weight: 600;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(100, 100, 150, 0.2);
    }

    .loading {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        padding: 3rem;
        color: #888;
    }

    .spinner {
        width: 24px;
        height: 24px;
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-top-color: #6366f1;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    .error-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 1rem;
        color: #f87171;
        font-size: 0.875rem;
    }

    .placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        min-height: 200px;
        color: #666;
        text-align: center;
    }

    .result-content {
        max-height: 500px;
        overflow-y: auto;
    }

    .result-text,
    .result-data {
        background: rgba(30, 30, 45, 0.8);
        border: 1px solid rgba(100, 100, 150, 0.2);
        border-radius: 8px;
        padding: 1rem;
        color: #ddd;
        font-size: 0.8rem;
        font-family: "JetBrains Mono", "Fira Code", monospace;
        white-space: pre-wrap;
        word-break: break-word;
        overflow-x: auto;
    }

    @media (max-width: 1200px) {
        .detailed-form-mode {
            grid-template-columns: 1fr 1fr;
        }
        .result-panel {
            grid-column: span 2;
        }
    }

    @media (max-width: 768px) {
        .detailed-form-mode {
            grid-template-columns: 1fr;
        }
        .result-panel {
            grid-column: span 1;
        }
    }
</style>
