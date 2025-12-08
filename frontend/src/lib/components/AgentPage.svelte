<script lang="ts">
    import { onMount } from "svelte";
    import { fly, fade, slide } from "svelte/transition";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { marked } from "marked";
    import {
        Plane,
        Mountain,
        Car,
        Laptop,
        Coffee,
        AlarmClock,
        Twitter,
        Instagram,
        Facebook,
        Linkedin,
        Send,
        Bot,
        Zap,
        BrainCircuit,
        ChevronDown,
        Loader2,
        Globe,
        Search,
        TrendingUp,
        MapPin,
        FileText,
        BarChart3,
        Briefcase,
        Leaf,
        Sprout,
        Flower,
        BookOpen,
        PenTool,
    } from "lucide-svelte";
    import { sendLLMPrompt } from "../api";

    // Configure marked for clean output
    marked.setOptions({
        breaks: true,
        gfm: true,
    });

    // Parse markdown to HTML
    function parseMarkdown(content: string): string {
        return marked.parse(content) as string;
    }

    // Props
    let { category, onBack, onCategoryChange } = $props<{
        category: string;
        onBack: () => void;
        onCategoryChange: (cat: string) => void;
    }>();

    // State
    let prompt = $state("");
    let isThinking = $state(false);
    let model = $state("thinking"); // thinking (Gemini 3 Pro), fast (Gemini 2 Fast)
    let messages = $state([]);
    let showDropdown = $state(false);
    let thinkingSteps = $state([]);

    // Theme Configuration
    const themes = {
        travel: {
            name: "Travel",
            primary: "#00e676", // Electric Green
            secondary: "#006633",
            bg: "#050505", // Very Dark
            text: "#ffffff",
            accent: "#69f0ae",
            cardBg: "rgba(0, 20, 10, 0.9)",
            icon: Plane,
            description: "Global Travel Orchestration",
        },
        jobs: {
            name: "Jobs",
            primary: "#8d6e63", // Warm Brown
            secondary: "#5d4037",
            bg: "#f5f5dc", // Creamy Beige (Cozy)
            text: "#3e2723", // Dark Brown Text
            accent: "#d7ccc8",
            cardBg: "rgba(255, 255, 255, 0.85)",
            icon: Briefcase,
            description: "Career Acceleration System",
        },
        trends: {
            name: "Trends",
            primary: "#ff0033", // Electric Red
            secondary: "#b71c1c",
            bg: "#ffffff", // White
            text: "#000000",
            accent: "#ff8a80",
            cardBg: "rgba(255, 240, 240, 0.95)",
            icon: TrendingUp,
            description: "Viral Intelligence Engine",
        },
    };

    // Capabilities Data
    const capabilities = {
        travel: {
            stats: [
                { value: "5+", label: "Global APIs Reachable" },
                { value: "2M+", label: "Listings Accessible" },
                { value: "Real-time", label: "Route Optimization" },
            ],
            tools: [
                "Airbnb Server",
                "Booking.com API",
                "TripAdvisor Content API",
                "Google Places API",
                "Google Geocoding API",
                "Google Routes API",
            ],
            guidance:
                "Ask me to plan a complete itinerary, find hidden gems in specific neighborhoods, or compare prices across platforms for your next trip.",
        },
        jobs: {
            stats: [
                { value: "100M+", label: "Listings Scannable" },
                { value: "AI", label: "Resume Optimization" },
                { value: "Global", label: "Market Intelligence" },
            ],
            tools: [
                "JSearch API",
                "Active Jobs DB",
                "ResumeOptimizer Pro",
                "LinkedIn Data Analysis",
                "Glassdoor Insights",
            ],
            guidance:
                "I can help you find roles that match your exact skills, optimize your resume for ATS systems, and provide salary insights for negotiations.",
        },
        trends: {
            stats: [
                { value: "Billions", label: "Signals Reachable" },
                { value: "5", label: "Major Platforms" },
                { value: "Predictive", label: "Viral Engines" },
            ],
            tools: [
                "X (Twitter) API",
                "TikTok Scraper",
                "Instagram Scraper",
                "Facebook Scraper",
                "YouTube Data API v3",
                "Google Trends API",
            ],
            guidance:
                "Task me with identifying emerging viral topics, analyzing sentiment across platforms, or tracking competitor performance in real-time.",
        },
    };

    let currentTheme = $derived(themes[category] || themes.travel);
    let CurrentIcon = $derived(currentTheme.icon);
    let currentCapabilities = $derived(
        capabilities[category] || capabilities.travel,
    );

    const handleSubmit = async () => {
        if (!prompt.trim()) return;

        const currentPrompt = prompt;
        const userMsg = { role: "user", content: currentPrompt };

        // Optimistically add user message
        messages = [...messages, userMsg];
        prompt = "";
        isThinking = true;
        thinkingSteps = [
            { text: "Sending request to Gemini...", status: "pending" },
        ];

        try {
            // Simulate steps for UI feedback while waiting
            const stepInterval = setInterval(() => {
                const steps = [
                    "Orchestrating MCP tools...",
                    "Reasoning with Gemini...",
                    "Synthesizing response...",
                ];
                const nextStep = steps[thinkingSteps.length % steps.length];
                thinkingSteps = [
                    ...thinkingSteps,
                    { text: nextStep, status: "pending" },
                ];
            }, 2000);

            const response = await sendLLMPrompt({
                prompt: currentPrompt,
                mode: category, // Map category to mode
                history: messages.map((m) => ({
                    role: m.role === "assistant" ? "model" : "user",
                    content: m.content,
                })),
            });

            clearInterval(stepInterval);

            messages = [
                ...messages,
                {
                    role: "assistant",
                    content: response.output || "No response received.",
                },
            ];
        } catch (error) {
            console.error("LLM Error:", error);
            messages = [
                ...messages,
                {
                    role: "assistant",
                    content:
                        "Sorry, I encountered an error connecting to the agent. Please try again.",
                },
            ];
        } finally {
            isThinking = false;
            thinkingSteps = [];
        }
    };

    const handleCategorySwitch = (newCat: string) => {
        onCategoryChange(newCat);
        showDropdown = false;
        messages = []; // Clear messages on switch
    };
</script>

<div
    class="agent-container"
    style="
  --primary: {currentTheme.primary};
  --secondary: {currentTheme.secondary};
  --bg: {currentTheme.bg};
  --text: {currentTheme.text};
  --accent: {currentTheme.accent};
  --card-bg: {currentTheme.cardBg};
"
>
    <!-- Cozy Plants for Jobs Theme -->
    {#if category === "jobs"}
        <div class="plants-bg" transition:fade>
            <div class="plant p1"><Leaf size={120} strokeWidth={1} /></div>
            <div class="plant p2"><Sprout size={100} strokeWidth={1} /></div>
            <div class="plant p3"><Flower size={80} strokeWidth={1} /></div>
            <div class="plant p4"><Coffee size={90} strokeWidth={1} /></div>
            <div class="plant p5"><BookOpen size={110} strokeWidth={1} /></div>
            <div class="plant p6"><PenTool size={70} strokeWidth={1} /></div>
        </div>
    {/if}

    <!-- Top Bar -->
    <div class="top-bar">
        <div class="left-controls">
            <button class="back-btn" onclick={onBack}>←</button>

            <div class="category-selector">
                <button
                    class="cat-btn"
                    onclick={() => (showDropdown = !showDropdown)}
                >
                    <CurrentIcon size={20} />
                    <span class="cat-name">{currentTheme.name}</span>
                    <ChevronDown size={16} />
                </button>

                {#if showDropdown}
                    <div
                        class="dropdown"
                        transition:fly={{ y: -10, duration: 200 }}
                    >
                        {#each Object.entries(themes) as [key, theme]}
                            {@const ThemeIcon = theme.icon}
                            <button
                                class="dropdown-item"
                                onclick={() => handleCategorySwitch(key)}
                            >
                                <ThemeIcon size={16} />
                                {theme.name}
                            </button>
                        {/each}
                    </div>
                {/if}
            </div>

            <span class="cat-desc">| {currentTheme.description}</span>
        </div>

        <div class="model-toggle">
            <button
                class="model-btn {model === 'thinking' ? 'active' : ''}"
                onclick={() => (model = "thinking")}
                title="Gemini 3 Pro (Reasoning)"
            >
                <BrainCircuit size={18} />
                <span>Thinking</span>
            </button>
            <button
                class="model-btn {model === 'fast' ? 'active' : ''}"
                onclick={() => (model = "fast")}
                title="Gemini 2 Fast"
            >
                <Zap size={18} />
                <span>Fast</span>
            </button>
        </div>
    </div>

    <!-- Main Chat Area -->
    <div class="chat-area">
        {#if messages.length === 0}
            <div class="empty-state" in:fade>
                <div class="hero-section">
                    <div class="icon-ring">
                        <CurrentIcon size={48} color="var(--primary)" />
                    </div>
                    <h1 class="gradient-title">{currentTheme.description}</h1>

                    <!-- Simplified Powered By -->
                    <div class="powered-by-container">
                        <div class="active-indicator"></div>
                        <p class="powered-by-text">
                            Powered by Crosswind AI & Gemini 3 Pro
                        </p>
                    </div>
                </div>

                <div class="stats-grid">
                    {#each currentCapabilities.stats as stat}
                        <div class="stat-card">
                            <div class="stat-value">{stat.value}</div>
                            <div class="stat-label">{stat.label}</div>
                        </div>
                    {/each}
                </div>

                <div class="tools-list">
                    <h3><Bot size={16} /> INTEGRATED TOOLS</h3>
                    <div class="tags">
                        {#each currentCapabilities.tools as tool}
                            <span class="tool-tag">{tool}</span>
                        {/each}
                    </div>
                </div>

                <div class="guidance">
                    <p>{currentCapabilities.guidance}</p>
                </div>
            </div>
        {:else}
            <div class="messages">
                <div class="message-spacer"></div>
                {#each messages as msg}
                    <div
                        class="message {msg.role}"
                        in:fly={{ y: 20, duration: 300 }}
                    >
                        {#if msg.role === "model" || msg.role === "assistant"}
                            <div class="msg-content markdown-body">
                                {@html parseMarkdown(msg.content)}
                            </div>
                        {:else}
                            <div class="msg-content">{msg.content}</div>
                        {/if}
                    </div>
                {/each}

                {#if isThinking}
                    <div class="thinking-indicator" in:slide>
                        <div class="thinking-header">
                            <Loader2 class="spin" size={16} />
                            <span>Reasoning...</span>
                        </div>
                        <div class="steps">
                            {#each thinkingSteps as step}
                                <div
                                    class="step {step.status}"
                                    in:slide={{ axis: "y" }}
                                >
                                    {#if step.status === "pending"}
                                        <div class="step-dot"></div>
                                    {:else if step.status === "done"}
                                        <div
                                            class="step-dot"
                                            style="background: var(--primary)"
                                        ></div>
                                    {/if}
                                    <span>{step.text}</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}
            </div>
        {/if}
    </div>

    <!-- Input Area -->
    <div class="input-area">
        <div class="input-wrapper">
            <input
                type="text"
                placeholder="Ask anything..."
                bind:value={prompt}
                onkeydown={(e) =>
                    e.key === "Enter" && !isThinking && handleSubmit()}
            />
            <button
                class="send-btn"
                onclick={handleSubmit}
                disabled={!prompt.trim() || isThinking}
            >
                {#if isThinking}
                    <Loader2 class="spin" size={20} />
                {:else}
                    <Send size={20} />
                {/if}
            </button>
        </div>
    </div>
</div>

<style>
    /* Container */
    .agent-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        background: var(--bg);
        color: var(--text);
        position: relative;
        overflow: hidden;
    }

    /* Plants Background (Jobs Theme) */
    .plants-bg {
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        opacity: 0.08;
    }
    .plant {
        position: absolute;
        color: var(--primary);
    }
    .p1 {
        top: 10%;
        left: 5%;
    }
    .p2 {
        top: 60%;
        left: 8%;
    }
    .p3 {
        bottom: 15%;
        left: 15%;
    }
    .p4 {
        top: 20%;
        right: 8%;
    }
    .p5 {
        bottom: 25%;
        right: 5%;
    }
    .p6 {
        top: 50%;
        right: 12%;
    }

    /* Top Bar */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(128, 128, 128, 0.05);
        border-bottom: 1px solid rgba(128, 128, 128, 0.1);
        position: relative;
        z-index: 10;
    }

    .left-controls {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .back-btn {
        background: transparent;
        border: 1px solid rgba(128, 128, 128, 0.3);
        color: var(--text);
        width: 36px;
        height: 36px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }
    .back-btn:hover {
        background: rgba(128, 128, 128, 0.1);
    }

    .category-selector {
        position: relative;
    }

    .cat-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: transparent;
        border: 1px solid rgba(128, 128, 128, 0.3);
        color: var(--text);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .cat-btn:hover {
        background: rgba(128, 128, 128, 0.1);
    }

    .cat-name {
        font-weight: 600;
    }

    .dropdown {
        position: absolute;
        top: calc(100% + 0.5rem);
        left: 0;
        background: var(--card-bg);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        overflow: hidden;
        min-width: 150px;
        z-index: 100;
        backdrop-filter: blur(10px);
    }

    .dropdown-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        width: 100%;
        padding: 0.75rem 1rem;
        background: transparent;
        border: none;
        color: var(--text);
        cursor: pointer;
        font-size: 0.9rem;
        transition: background 0.2s;
    }
    .dropdown-item:hover {
        background: rgba(128, 128, 128, 0.1);
    }

    .cat-desc {
        color: var(--text);
        opacity: 0.6;
        font-size: 0.85rem;
    }

    .model-toggle {
        display: flex;
        gap: 0.5rem;
        background: rgba(128, 128, 128, 0.1);
        padding: 0.25rem;
        border-radius: 8px;
    }

    .model-btn {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.5rem 0.75rem;
        background: transparent;
        border: none;
        color: var(--text);
        opacity: 0.6;
        cursor: pointer;
        border-radius: 6px;
        font-size: 0.8rem;
        transition: all 0.2s;
    }
    .model-btn:hover {
        opacity: 0.8;
    }
    .model-btn.active {
        background: var(--primary);
        color: #fff;
        opacity: 1;
    }

    /* Chat Area */
    .chat-area {
        flex: 1;
        overflow-y: auto;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        z-index: 1;
    }

    /* Empty State */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        max-width: 700px;
        text-align: center;
        padding: 2rem 0;
    }

    .hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .icon-ring {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(128, 128, 128, 0.05);
        border: 2px solid var(--primary);
    }

    .gradient-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }

    .powered-by-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .active-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--primary);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .powered-by-text {
        font-size: 0.85rem;
        opacity: 0.7;
        margin: 0;
    }

    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        width: 100%;
    }

    .stat-card {
        background: var(--card-bg);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.25rem;
    }

    .stat-label {
        font-size: 0.8rem;
        opacity: 0.7;
    }

    /* Tools List */
    .tools-list {
        width: 100%;
    }

    .tools-list h3 {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.6;
        margin-bottom: 1rem;
    }

    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
    }

    .tool-tag {
        background: var(--card-bg);
        border: 1px solid rgba(128, 128, 128, 0.15);
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }

    /* Guidance */
    .guidance {
        background: var(--card-bg);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        width: 100%;
    }

    .guidance p {
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.6;
        opacity: 0.85;
    }

    /* Messages */
    .messages {
        width: 100%;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .message-spacer {
        height: 1rem;
    }

    .message {
        display: flex;
        flex-direction: column;
        max-width: 80%;
    }

    .message.user {
        align-self: flex-end;
        align-items: flex-end;
    }

    .message.assistant,
    .message.model {
        align-self: flex-start;
    }

    .msg-content {
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-size: 1rem;
        line-height: 1.5;
    }

    .message.user .msg-content {
        background: var(--primary);
        color: #fff;
        border-bottom-right-radius: 2px;
    }

    .message.assistant .msg-content,
    .message.model .msg-content {
        background: rgba(128, 128, 128, 0.1);
        color: var(--text);
        border-bottom-left-radius: 2px;
    }

    /* Global Markdown Styles */
    :global(.markdown-body) {
        font-family: inherit;
        line-height: 1.6;
        color: var(--text);
    }
    :global(.markdown-body p) {
        margin-bottom: 1rem;
    }
    :global(.markdown-body h1),
    :global(.markdown-body h2),
    :global(.markdown-body h3) {
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        line-height: 1.25;
    }
    :global(.markdown-body code) {
        background: rgba(128, 128, 128, 0.1);
        padding: 0.2em 0.4em;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9em;
    }
    :global(.markdown-body pre) {
        background: rgba(0, 0, 0, 0.2);
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
        margin: 1rem 0;
    }
    :global(.markdown-body pre code) {
        background: transparent;
        padding: 0;
    }
    :global(.markdown-body ul),
    :global(.markdown-body ol) {
        margin-bottom: 1rem;
        padding-left: 2rem;
    }
    :global(.markdown-body li) {
        margin-bottom: 0.25rem;
    }
    :global(.markdown-body blockquote) {
        border-left: 4px solid var(--primary);
        padding-left: 1rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.7);
    }
    :global(.markdown-body table) {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    /* Wrapped TH styles follow */
    .markdown-body :global(th) {
        background: rgba(128, 128, 128, 0.1);
        font-weight: 600;
    }

    /* Thinking Indicator */
    .thinking-indicator {
        align-self: flex-start;
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 8px;
        padding: 1rem;
        width: 100%;
        max-width: 400px;
    }

    .thinking-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
        color: var(--primary);
    }

    .steps {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        opacity: 0.6;
    }

    .step.done {
        opacity: 1;
        color: var(--text);
    }
    .step.pending {
        opacity: 0.8;
        font-style: italic;
    }

    .step-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
    }

    :global(.spin) {
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    /* Input Area */
    .input-area {
        padding: 2rem;
        background: var(--bg);
        display: flex;
        justify-content: center;
        border-top: 1px solid rgba(128, 128, 128, 0.1);
        z-index: 100;
    }

    .input-wrapper {
        width: 100%;
        max-width: 800px;
        position: relative;
        display: flex;
        align-items: center;
    }

    input {
        width: 100%;
        padding: 1rem 3.5rem 1rem 1.5rem;
        border-radius: 50px;
        border: 1px solid rgba(128, 128, 128, 0.3);
        background: var(--card-bg);
        color: var(--text);
        font-size: 1rem;
        outline: none;
        transition:
            border-color 0.2s,
            box-shadow 0.2s;
    }

    input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1); /* Subtle glow */
    }

    .send-btn {
        position: absolute;
        right: 0.5rem;
        background: var(--primary);
        color: #fff;
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: transform 0.2s;
    }

    .send-btn:hover:not(:disabled) {
        transform: scale(1.05);
    }
    .send-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>
