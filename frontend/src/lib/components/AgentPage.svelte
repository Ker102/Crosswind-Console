<script lang="ts">
    import { onMount } from "svelte";
    import { fly, fade, slide } from "svelte/transition";
    import { Icon } from "@steeze-ui/svelte-icon";
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
                {#each messages as msg}
                    <div
                        class="message {msg.role}"
                        in:fly={{ y: 20, duration: 300 }}
                    >
                        <div class="msg-content">{msg.content}</div>
                    </div>
                {/each}

                {#if isThinking}
                    <div class="thinking-indicator" in:fade>
                        <div class="thinking-header">
                            <Loader2 size={16} class="spin" />
                            <span>Thinking Process</span>
                        </div>
                        <div class="steps">
                            {#each thinkingSteps as step}
                                <div class="step {step.status}">
                                    <div class="step-dot"></div>
                                    <span>{step.text}</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}
            </div>
        {/if}
    </div>

    <!-- Bottom Input Bar -->
    <div class="input-area">
        <div class="input-wrapper">
            <input
                type="text"
                bind:value={prompt}
                onkeydown={(e) => e.key === "Enter" && handleSubmit()}
                placeholder="Ask anything about {currentTheme.name}..."
            />
            <button
                class="send-btn"
                onclick={handleSubmit}
                disabled={!prompt.trim() || isThinking}
            >
                <Send size={20} />
            </button>
        </div>
    </div>
</div>

<style>
    .agent-container {
        width: 100vw;
        height: 100vh;
        background-color: var(--bg);
        color: var(--text);
        display: flex;
        flex-direction: column;
        transition:
            background-color 0.5s ease,
            color 0.5s ease;
        font-family: "Inter", sans-serif;
        position: relative;
        overflow: hidden;
    }

    /* Plants Background */
    .plants-bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.1;
        color: #5d4037;
    }

    .plant {
        position: absolute;
    }
    .p1 {
        bottom: -20px;
        left: -20px;
        transform: rotate(15deg);
    }
    .p2 {
        bottom: -10px;
        right: -10px;
        transform: rotate(-10deg);
    }
    .p3 {
        top: 10%;
        right: 5%;
        transform: rotate(45deg);
        opacity: 0.5;
    }
    .p4 {
        top: 20%;
        left: 10%;
        transform: rotate(-15deg);
        opacity: 0.6;
    } /* Coffee */
    .p5 {
        bottom: 15%;
        left: 25%;
        transform: rotate(10deg);
        opacity: 0.4;
    } /* Notebook */
    .p6 {
        top: 15%;
        right: 20%;
        transform: rotate(-30deg);
        opacity: 0.5;
    } /* Pen */

    /* Top Bar */
    .top-bar {
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(128, 128, 128, 0.1);
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        z-index: 100;
    }

    .left-controls {
        display: flex;
        gap: 1.5rem;
        align-items: center;
    }

    .back-btn {
        background: none;
        border: none;
        color: var(--text);
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.2s;
        padding: 0;
    }
    .back-btn:hover {
        opacity: 1;
    }

    .category-selector {
        position: relative;
    }

    .cat-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(128, 128, 128, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        color: var(--text);
        cursor: pointer;
        font-weight: 700;
        transition: all 0.2s;
        font-size: 1rem;
    }
    .cat-btn:hover {
        background: rgba(128, 128, 128, 0.2);
    }

    .dropdown {
        position: absolute;
        top: 100%;
        left: 0;
        margin-top: 0.5rem;
        background: var(--card-bg);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        padding: 0.5rem;
        min-width: 180px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        z-index: 200;
    }

    .dropdown-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        background: none;
        border: none;
        padding: 0.8rem;
        color: var(--text);
        cursor: pointer;
        text-align: left;
        border-radius: 4px;
        font-weight: 500;
        transition: background 0.2s;
    }
    .dropdown-item:hover {
        background: rgba(128, 128, 128, 0.1);
    }

    .cat-desc {
        font-weight: 400;
        opacity: 0.7;
        font-size: 0.9rem;
        color: var(--text);
    }

    /* Model Toggle */
    .model-toggle {
        display: flex;
        background: rgba(128, 128, 128, 0.1);
        padding: 0.25rem;
        border-radius: 8px;
        gap: 0.25rem;
        border: 1px solid rgba(128, 128, 128, 0.1);
    }

    .model-btn {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        background: none;
        border: none;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        color: var(--text);
        opacity: 0.6;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.2s;
    }

    .model-btn.active {
        background: var(--primary);
        color: #fff; /* Always white text on active button for contrast */
        opacity: 1;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }

    /* Chat Area */
    .chat-area {
        flex: 1;
        overflow-y: auto;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        z-index: 10; /* Above plants */
    }

    .empty-state {
        width: 100%;
        max-width: 900px;
        margin-top: 5vh;
        display: flex;
        flex-direction: column;
        gap: 3rem;
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .hero-section {
        text-align: center;
    }

    .icon-ring {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: rgba(var(--primary), 0.1);
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 1.5rem;
        border: 2px solid var(--primary);
        box-shadow: 0 0 20px rgba(var(--primary), 0.3);
    }

    h1.gradient-title {
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0 0 0.5rem;
        background: linear-gradient(
            135deg,
            var(--primary),
            var(--accent),
            #fff
        );
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        text-transform: uppercase;
    }

    /* Powered By - Minimalist */
    .powered-by-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
        opacity: 0.6;
    }

    .active-indicator {
        width: 8px;
        height: 8px;
        background-color: #00e676; /* Always green for active */
        border-radius: 50%;
        box-shadow: 0 0 8px #00e676;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.2);
            opacity: 0.7;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    .powered-by-text {
        font-size: 0.85rem;
        font-weight: 400;
        letter-spacing: 0.02em;
        color: var(--text);
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }

    .stat-card {
        background: var(--card-bg);
        border: 1px solid rgba(128, 128, 128, 0.1);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        transition: transform 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
    }

    .stat-value {
        font-size: 2rem;
        font-weight: 900;
        color: var(--primary);
        margin-bottom: 0.2rem;
    }

    .stat-label {
        font-size: 0.85rem;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .tools-list {
        background: var(--card-bg);
        border: 1px solid rgba(128, 128, 128, 0.1);
        padding: 1.5rem;
        border-radius: 16px;
    }

    .tools-list h3 {
        font-size: 0.9rem;
        margin: 0 0 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        opacity: 0.8;
        color: var(--text);
        -webkit-text-fill-color: var(--text); /* Reset gradient */
    }

    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
    }

    .tool-tag {
        background: rgba(128, 128, 128, 0.1);
        padding: 0.4rem 0.8rem;
        border-radius: 50px;
        font-size: 0.85rem;
        border: 1px solid rgba(128, 128, 128, 0.1);
        transition: all 0.2s;
    }
    .tool-tag:hover {
        background: var(--primary);
        color: #fff;
        border-color: var(--primary);
    }

    .guidance {
        text-align: center;
        font-size: 1.1rem;
        line-height: 1.6;
        opacity: 0.8;
        max-width: 700px;
        margin: 0 auto;
        font-style: italic;
    }

    /* Messages */
    .messages {
        width: 100%;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
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

    .message.assistant {
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

    .message.assistant .msg-content {
        background: rgba(128, 128, 128, 0.1);
        color: var(--text);
        border-bottom-left-radius: 2px;
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
