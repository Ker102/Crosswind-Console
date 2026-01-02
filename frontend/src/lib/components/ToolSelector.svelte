<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";

    interface Tool {
        name: string;
        description?: string;
        server: string;
        category: string;
    }

    interface Server {
        name: string;
        category: string;
    }

    // Props
    export let selectedServer: string = "";
    export let selectedTool: string = "";
    export let loading = false;

    // State
    let servers: Server[] = [];
    let tools: Tool[] = [];
    let loadingServers = true;
    let loadingTools = false;
    let searchQuery = "";

    const dispatch = createEventDispatcher<{
        select: { server: string; tool: string };
    }>();

    const API_BASE = "http://localhost:8000";

    onMount(async () => {
        await fetchServers();
    });

    async function fetchServers() {
        loadingServers = true;
        try {
            const res = await fetch(`${API_BASE}/api/mcp/servers`);
            const data = await res.json();
            servers = data.servers;
        } catch (e) {
            console.error("Failed to fetch servers:", e);
        } finally {
            loadingServers = false;
        }
    }

    async function fetchTools(serverName: string) {
        loadingTools = true;
        tools = [];
        try {
            const res = await fetch(`${API_BASE}/api/mcp/tools/${serverName}`);
            const data = await res.json();
            tools = data.tools;
        } catch (e) {
            console.error("Failed to fetch tools:", e);
        } finally {
            loadingTools = false;
        }
    }

    function handleServerChange(event: Event) {
        const select = event.target as HTMLSelectElement;
        selectedServer = select.value;
        selectedTool = "";
        if (selectedServer) {
            fetchTools(selectedServer);
        } else {
            tools = [];
        }
    }

    function handleToolSelect(tool: Tool) {
        selectedTool = tool.name;
        dispatch("select", { server: selectedServer, tool: tool.name });
    }

    $: filteredTools = tools.filter(
        (t) =>
            t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            (t.description?.toLowerCase().includes(searchQuery.toLowerCase()) ??
                false),
    );
</script>

<div class="tool-selector">
    <div class="server-select">
        <label for="server">MCP Server</label>
        <select
            id="server"
            value={selectedServer}
            on:change={handleServerChange}
            disabled={loadingServers || loading}
        >
            <option value="">Select a server...</option>
            {#each servers as server}
                <option value={server.name}>
                    {server.name} ({server.category})
                </option>
            {/each}
        </select>
    </div>

    {#if selectedServer}
        <div class="tool-list">
            <div class="search-box">
                <input
                    type="text"
                    placeholder="Search tools..."
                    bind:value={searchQuery}
                    disabled={loadingTools || loading}
                />
                <span class="tool-count">{filteredTools.length} tools</span>
            </div>

            {#if loadingTools}
                <div class="loading">
                    <span class="spinner"></span>
                    Loading tools...
                </div>
            {:else}
                <div class="tools-grid">
                    {#each filteredTools as tool}
                        <button
                            class="tool-card"
                            class:selected={selectedTool === tool.name}
                            on:click={() => handleToolSelect(tool)}
                            disabled={loading}
                        >
                            <span class="tool-name"
                                >{tool.name.replace(/_/g, " ")}</span
                            >
                            {#if tool.description}
                                <span class="tool-desc"
                                    >{tool.description.slice(0, 80)}...</span
                                >
                            {/if}
                        </button>
                    {/each}
                </div>
            {/if}
        </div>
    {/if}
</div>

<style>
    .tool-selector {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }

    .server-select label {
        display: block;
        margin-bottom: 0.5rem;
        color: #aaa;
        font-size: 0.875rem;
    }

    .server-select select {
        width: 100%;
        padding: 0.75rem 1rem;
        background: rgba(30, 30, 45, 0.9);
        border: 1px solid rgba(100, 100, 150, 0.4);
        border-radius: 8px;
        color: #fff;
        font-size: 0.95rem;
    }

    .server-select select:focus {
        outline: none;
        border-color: #6366f1;
    }

    .search-box {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .search-box input {
        flex: 1;
        padding: 0.625rem 1rem;
        background: rgba(30, 30, 45, 0.9);
        border: 1px solid rgba(100, 100, 150, 0.4);
        border-radius: 8px;
        color: #fff;
        font-size: 0.875rem;
    }

    .search-box input:focus {
        outline: none;
        border-color: #6366f1;
    }

    .tool-count {
        color: #888;
        font-size: 0.8rem;
        white-space: nowrap;
    }

    .loading {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        padding: 2rem;
        color: #888;
    }

    .spinner {
        width: 20px;
        height: 20px;
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

    .tools-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 0.75rem;
        max-height: 300px;
        overflow-y: auto;
        padding-right: 0.5rem;
    }

    .tools-grid::-webkit-scrollbar {
        width: 6px;
    }

    .tools-grid::-webkit-scrollbar-track {
        background: rgba(30, 30, 45, 0.5);
        border-radius: 3px;
    }

    .tools-grid::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.5);
        border-radius: 3px;
    }

    .tool-card {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding: 0.875rem;
        background: rgba(30, 30, 45, 0.7);
        border: 1px solid rgba(100, 100, 150, 0.3);
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
    }

    .tool-card:hover:not(:disabled) {
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(40, 40, 60, 0.8);
    }

    .tool-card.selected {
        border-color: #6366f1;
        background: rgba(99, 102, 241, 0.15);
    }

    .tool-card:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .tool-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #fff;
        text-transform: capitalize;
        margin-bottom: 0.25rem;
    }

    .tool-desc {
        font-size: 0.7rem;
        color: #888;
        line-height: 1.4;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
</style>
