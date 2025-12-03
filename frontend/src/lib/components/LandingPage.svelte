<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { fly, fade } from "svelte/transition";
  import IconCloud from "./IconCloud.svelte";
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
    Sparkles,
    Clapperboard,
    Globe,
    BrainCircuit,
    TrendingUp,
    Briefcase,
    Github,
    Menu,
    X,
    Bitcoin,
    DollarSign,
  } from "lucide-svelte";
  import {
    Glassdoor,
    Facebook as FacebookIcon,
    Tiktok,
    Tripadvisor,
    Airbnb,
    Svelte,
    Python,
    Fastapi,
    Postgresql,
    Typescript,
    Tailwindcss,
    Vite,
    Threedotjs,
  } from "@steeze-ui/simple-icons";

  // ... (rest of imports)

  let { onSelectCategory } = $props<{
    onSelectCategory: (category: string) => void;
  }>();

  let text = $state("");
  const phrases = ["TRAVEL", "JOBS", "TRENDS"];
  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let timer: number;

  let showLanding = $state(true);
  let isNavExpanded = $state(false);

  const toggleNav = () => {
    isNavExpanded = !isNavExpanded;
  };

  const type = () => {
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      text = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
    } else {
      text = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
    }

    let typeSpeed = 100;

    if (isDeleting) {
      typeSpeed /= 2;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      isDeleting = true;
      typeSpeed = 2000; // Pause at end
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      typeSpeed = 500;
    }

    timer = setTimeout(type, typeSpeed);
  };

  const handleTransition = () => {
    showLanding = false;
  };

  const handleScroll = (e: WheelEvent) => {
    if (showLanding && e.deltaY > 0) {
      handleTransition();
    } else if (!showLanding && e.deltaY < 0) {
      // Only scroll back up if we are at the top of the selection container
      const container = document.querySelector(".selection-scroll-container");
      if (container && container.scrollTop === 0) {
        showLanding = true;
      }
    }
  };

  onMount(() => {
    timer = setTimeout(type, 1000);
    window.addEventListener("wheel", handleScroll);
  });

  onDestroy(() => {
    clearTimeout(timer);
    window.removeEventListener("wheel", handleScroll);
  });
</script>

<div class="landing-container">
  <!-- Dynamic Island Navigation -->
  <div class="nav-island" class:expanded={isNavExpanded}>
    <div class="nav-content">
      <button class="nav-toggle" onclick={toggleNav} aria-label="Toggle Menu">
        {#if isNavExpanded}
          <X size={20} color="#fff" />
        {:else}
          <Menu size={20} color="#fff" />
        {/if}
      </button>

      {#if isNavExpanded}
        <div class="nav-links" transition:fade={{ duration: 200 }}>
          <a
            href="#start"
            onclick={(e) => {
              e.preventDefault();
              handleTransition();
              toggleNav();
            }}>Start</a
          >
          <a
            href="#connect"
            onclick={(e) => {
              e.preventDefault();
              toggleNav();
            }}>Connect</a
          >
          <a
            href="#capabilities"
            onclick={(e) => {
              e.preventDefault();
              toggleNav();
            }}>Capabilities</a
          >
          <a
            href="#pricing"
            onclick={(e) => {
              e.preventDefault();
              toggleNav();
            }}>Pricing</a
          >
        </div>
      {/if}
    </div>
  </div>

  <button class="logo" onclick={() => (showLanding = true)}
    >Crosswind Console</button
  >

  {#if showLanding}
    <div class="landing-content" transition:fly={{ y: -1000, duration: 1000 }}>
      <IconCloud />
      <div class="content">
        <div class="header">
          <div class="title-wrapper">
            <h1 class="title">
              INTELLIGENT ORCHESTRATION FOR<br />
              <span class="highlight">{text}</span><span class="cursor">|</span>
            </h1>
            <p class="description">
              Harness the power of Gemini 3 Pro to analyze thousands of signals
              from global platforms. From travel deals to career opportunities
              and viral trends, Crosswind Console turns data into action.
            </p>
          </div>
        </div>

        <button class="cta-button" onclick={handleTransition}>
          GET STARTED <span class="arrow">→</span>
        </button>
      </div>
    </div>
  {:else}
    <div
      class="selection-container"
      transition:fly={{ y: 1000, duration: 1000 }}
    >
      <!-- Background Logos (Fixed in Selection View) -->
      <div class="background-logos">
        <!-- MCP Logo -->
        <img
          src="/mcp.png"
          alt="MCP"
          class="bg-logo mcp-logo"
          style="top: 10%; left: 10%; transform: rotate(-15deg);"
        />
        <!-- Firecrawl Logo (PNG) -->
        <img
          src="/firecrawl.png"
          alt="Firecrawl"
          class="bg-logo firecrawl-logo"
          style="top: 20%; right: 15%; transform: rotate(10deg); width: 100px;"
        />
        <!-- Gemini Logo (User Asset) -->
        <img
          src="/gemini_logo_v2.png"
          alt="Gemini"
          class="bg-logo gemini-logo"
          style="bottom: 15%; left: 20%; transform: rotate(5deg); width: 80px; border-radius: 10px;"
        />
        <!-- Playwright Logo (User Asset - Transparent) -->
        <img
          src="/playwright_masks_transparent.png"
          alt="Playwright"
          class="bg-logo playwright-logo"
          style="bottom: 25%; right: 10%; transform: rotate(-10deg); width: 80px;"
        />
      </div>

      <div class="selection-scroll-container">
        <div class="section categories-section">
          <h2 class="selection-title">CHOOSE YOUR PATH</h2>
          <div class="cards">
            <div
              class="card travel"
              onclick={() => onSelectCategory("travel")}
              role="button"
              tabindex="0"
              onkeydown={(e) => e.key === "Enter" && onSelectCategory("travel")}
            >
              <div class="card-icons">
                <Plane size={24} />
                <Mountain size={24} />
                <Car size={24} />
              </div>
              <h3>TRAVEL</h3>
              <p>Explore the world with best deals.</p>
            </div>
            <div
              class="card jobs"
              onclick={() => onSelectCategory("jobs")}
              role="button"
              tabindex="0"
              onkeydown={(e) => e.key === "Enter" && onSelectCategory("jobs")}
            >
              <div class="card-icons">
                <Laptop size={24} />
                <Coffee size={24} />
                <AlarmClock size={24} />
              </div>
              <h3>JOBS</h3>
              <p>Find your next career opportunity.</p>
            </div>
            <div
              class="card trends"
              onclick={() => onSelectCategory("trends")}
              role="button"
              tabindex="0"
              onkeydown={(e) => e.key === "Enter" && onSelectCategory("trends")}
            >
              <div class="card-icons">
                <Twitter size={24} />
                <Instagram size={24} />
                <Facebook size={24} />
                <Linkedin size={24} />
              </div>
              <h3>TRENDS</h3>
              <p>Stay ahead with latest insights.</p>
            </div>
            <div
              class="card stocks"
              role="button"
              tabindex="0"
              style="cursor: default;"
            >
              <div class="card-icons">
                <Bitcoin size={24} />
                <TrendingUp size={24} />
                <DollarSign size={24} />
              </div>
              <h3>STOCKS & CRYPTO</h3>
              <p class="coming-soon">Coming Soon</p>
            </div>
          </div>
        </div>

        <!-- How It Works Section -->
        <div class="section how-it-works-section">
          <h2 class="section-title">HOW DOES IT WORK?</h2>
          <p class="section-desc">
            Our powerful AI model connects to hundreds of tools and APIs to
            scrape, orchestrate, and analyze data in real-time, providing you
            with the most accurate and actionable results.
          </p>

          <div class="workflow-visual">
            <div class="step">
              <div class="step-icon"><Globe size={40} /></div>
              <h4>CONNECT</h4>
              <p>Access 100+ Global APIs</p>
            </div>
            <div class="connector">→</div>
            <div class="step">
              <div class="step-icon"><BrainCircuit size={40} /></div>
              <h4>ORCHESTRATE</h4>
              <p>Gemini 3 Pro Analysis</p>
            </div>
            <div class="connector">→</div>
            <div class="step">
              <div class="step-icon"><Sparkles size={40} /></div>
              <h4>DELIVER</h4>
              <p>Actionable Insights</p>
            </div>
          </div>

          <div class="data-showcase">
            <div class="data-card">
              <div class="data-icon"><Plane size={32} /></div>
              <div class="data-stat">2M+</div>
              <div class="data-label">Flights & Stays</div>
            </div>
            <div class="data-card">
              <div class="data-icon"><Briefcase size={32} /></div>
              <div class="data-stat">100M+</div>
              <div class="data-label">Job Opportunities</div>
            </div>
            <div class="data-card">
              <div class="data-icon"><TrendingUp size={32} /></div>
              <div class="data-stat">1B+</div>
              <div class="data-label">Social Signals</div>
            </div>
          </div>
        </div>

        <div class="section tech-section">
          <h2 class="section-title">TECHNOLOGIES STACK</h2>
          <div class="tools-grid">
            <div class="tool-icon" title="Svelte">
              <Icon src={Svelte} size="40" />
            </div>
            <div class="tool-icon" title="Python">
              <Icon src={Python} size="40" />
            </div>
            <div class="tool-icon" title="FastAPI">
              <Icon src={Fastapi} size="40" />
            </div>
            <div class="tool-icon" title="PostgreSQL">
              <Icon src={Postgresql} size="40" />
            </div>
            <div class="tool-icon" title="TypeScript">
              <Icon src={Typescript} size="40" />
            </div>
            <div class="tool-icon" title="TailwindCSS">
              <Icon src={Tailwindcss} size="40" />
            </div>
            <div class="tool-icon" title="Vite">
              <Icon src={Vite} size="40" />
            </div>
            <div class="tool-icon" title="Three.js">
              <Icon src={Threedotjs} size="40" />
            </div>
            <!-- Crucial Tech -->
            <div class="tool-icon" title="Firecrawl">
              <img
                src="/firecrawl.png"
                alt="Firecrawl"
                style="width: 40px; height: 40px; object-fit: contain;"
              />
            </div>
            <div class="tool-icon" title="MCP">
              <img
                src="/mcp.png"
                alt="MCP"
                style="width: 40px; height: 40px; object-fit: contain;"
              />
            </div>
            <div class="tool-icon" title="RapidAPI">
              <Globe size={40} />
            </div>
          </div>
        </div>

        <div class="section connect-section">
          <h2 class="section-title">CONNECT WITH ME</h2>
          <div class="connect-content">
            <div class="social-links">
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                title="LinkedIn"
              >
                <Linkedin size={32} />
              </a>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                title="GitHub"
              >
                <Github size={32} />
              </a>
              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                title="Instagram"
              >
                <Instagram size={32} />
              </a>
              <a
                href="https://yourwebsite.com"
                target="_blank"
                rel="noopener noreferrer"
                class="social-link"
                title="Website"
              >
                <Globe size={32} />
              </a>
            </div>
            <p>Let's build something amazing together.</p>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap");

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: "Inter", sans-serif;
    overflow: hidden;
  }

  .landing-container {
    width: 100vw;
    height: 100vh;
    background: radial-gradient(
        circle at 10% 20%,
        rgba(100, 100, 255, 0.4) 0%,
        transparent 40%
      ),
      radial-gradient(
        circle at 90% 10%,
        rgba(255, 150, 255, 0.4) 0%,
        transparent 40%
      ),
      radial-gradient(
        circle at 50% 50%,
        rgba(255, 255, 255, 0.8) 0%,
        rgba(255, 200, 200, 0.2) 100%
      );
    background-color: #ffe0e0;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden; /* Ensure logos don't overflow */
  }

  /* Background Logos */
  .background-logos {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none; /* Let clicks pass through */
    z-index: 0; /* Behind selection content */
    position: fixed; /* Keep fixed while scrolling */
  }

  .bg-logo {
    position: absolute;
    opacity: 0.4; /* Increased visibility */
    filter: grayscale(0%); /* Remove grayscale for better visibility */
  }

  .mcp-logo {
    width: 100px;
    height: auto;
  }

  .landing-content {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 10; /* Above logos */
  }

  .logo {
    position: absolute;
    top: 2rem;
    left: 3rem;
    font-weight: 900;
    font-size: 1.5rem;
    color: #1a1a1a;
    z-index: 30;
    letter-spacing: -0.05em;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    font-family: inherit;
  }

  .content {
    text-align: center;
    z-index: 10;
    position: relative;
    max-width: 80vw;
  }

  .title-wrapper {
    position: relative;
    display: inline-block;
    max-width: 1200px;
  }

  .title {
    font-size: 3.5rem;
    line-height: 1.1;
    font-weight: 900;
    margin: 0;
    letter-spacing: -0.05em;
    text-transform: uppercase;

    /* Radial Fade from Bottom (Typewriter Text) - Tighter Radius */
    background: radial-gradient(
      circle at 50% 100%,
      #ff3bff 0%,
      #ecbfbf 10%,
      #5c24ff 25%,
      #1a1a1a 50%
    );
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    display: inline-block; /* Ensure background-clip works */
  }

  .description {
    font-size: 1.1rem;
    color: #555;
    margin-top: 1.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
    font-weight: 500;
  }

  .highlight {
    background: inherit;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    font-weight: 800;
  }

  .cursor {
    animation: blink 1s step-end infinite;
    color: #1a1a1a;
    font-weight: 100;
  }

  @keyframes blink {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0;
    }
  }

  .cta-button {
    margin-top: 3rem;
    background: #000;
    color: #fff;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: 0.1em;
  }

  .cta-button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  }

  .arrow {
    color: #b388ff;
  }

  /* Selection View Styles */
  .selection-container {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 20;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .selection-scroll-container {
    width: 100%;
    height: 100%;
    overflow-y: auto;
    padding-top: 10vh; /* Start content a bit down */
    padding-bottom: 5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5rem;
    /* Hide scrollbar for cleaner look */
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  .selection-scroll-container::-webkit-scrollbar {
    display: none;
  }

  .section {
    width: 100%;
    max-width: 1200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    z-index: 10; /* Above logos */
  }

  .selection-title,
  .section-title {
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 3rem;
    color: #1a1a1a;
    letter-spacing: -0.02em;
  }

  .cards {
    display: flex;
    gap: 2rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .card {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 20px;
    width: 250px;
    cursor: pointer;
    transition:
      transform 0.3s ease,
      background 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .card:hover {
    transform: translateY(-10px);
    background: rgba(255, 255, 255, 0.9);
  }

  .card-icons {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    color: #555;
  }

  .card h3 {
    font-size: 1.5rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
    color: #1a1a1a;
  }

  .card p {
    font-size: 0.9rem;
    color: #666;
    line-height: 1.4;
  }

  .travel h3 {
    color: #00a991;
  }

  /* Jobs Card - Brown-Greyish Vibe */
  .jobs {
    background: rgba(180, 170, 160, 0.2); /* Brownish tint */
    border-color: rgba(140, 130, 120, 0.4);
  }
  .jobs:hover {
    background: rgba(180, 170, 160, 0.4);
  }
  .jobs h3 {
    color: #6d5e52; /* Brown-grey text */
  }
  .jobs .card-icons {
    color: #6d5e52;
  }

  .trends h3 {
    color: #ff0000;
  }

  /* Stocks Card - Purple/White Vibe */
  .stocks {
    background: rgba(255, 255, 255, 0.6);
    border-color: rgba(147, 51, 234, 0.3);
  }
  .stocks:hover {
    background: rgba(255, 255, 255, 0.9);
    border-color: rgba(147, 51, 234, 0.6);
  }
  .stocks h3 {
    color: #9333ea; /* Purple text */
  }
  .stocks .card-icons {
    color: #9333ea;
  }
  .coming-soon {
    font-style: italic;
    font-weight: 700;
    color: #888 !important;
  }

  /* Tools & Tech Section */
  .tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: 2rem;
    width: 80%;
    justify-items: center;
  }

  .tool-icon {
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(5px);
    padding: 1rem;
    border-radius: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: transform 0.2s ease;
    color: #333;
  }

  .tool-icon:hover {
    transform: scale(1.1);
    background: rgba(255, 255, 255, 0.8);
    color: #000;
  }

  /* Connect Section */
  .connect-content {
    font-size: 1.2rem;
    color: #333;
    background: rgba(255, 255, 255, 0.4);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(5px);
  }

  /* How It Works Section */
  .how-it-works-section {
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    padding: 4rem 2rem;
    border-radius: 30px;
    margin: 2rem 0;
    border: 1px solid rgba(255, 255, 255, 0.5);
  }

  .section-desc {
    font-size: 1.1rem;
    color: #555;
    max-width: 700px;
    margin: 0 auto 3rem;
    line-height: 1.6;
  }

  .workflow-visual {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin-bottom: 4rem;
    flex-wrap: wrap;
  }

  .step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .step-icon {
    width: 80px;
    height: 80px;
    background: #fff;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    color: #333;
  }

  .step h4 {
    margin: 0;
    font-weight: 900;
    color: #1a1a1a;
  }

  .step p {
    margin: 0;
    font-size: 0.9rem;
    color: #666;
  }

  .connector {
    font-size: 2rem;
    color: #aaa;
    font-weight: 300;
  }

  .data-showcase {
    display: flex;
    justify-content: center;
    gap: 3rem;
    flex-wrap: wrap;
  }

  .data-card {
    background: rgba(255, 255, 255, 0.5);
    padding: 2rem;
    border-radius: 20px;
    width: 180px;
    text-align: center;
    transition: transform 0.3s ease;
  }
  .data-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.8);
  }

  .data-icon {
    color: #555;
    margin-bottom: 1rem;
  }

  .data-stat {
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #333, #666);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
  }

  .data-label {
    font-size: 0.9rem;
    font-weight: 700;
    color: #666;
    text-transform: uppercase;
  }
  .social-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
  }

  .social-link {
    color: #333;
    transition:
      transform 0.2s ease,
      color 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    backdrop-filter: blur(5px);
  }

  .social-link:hover {
    transform: translateY(-5px) scale(1.1);
    color: #000;
    background: rgba(255, 255, 255, 0.8);
  }

  /* Dynamic Island Navigation */
  .nav-island {
    position: absolute;
    top: 2rem;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(20px);
    border-radius: 40px;
    padding: 0.5rem;
    z-index: 100;
    transition:
      width 0.4s cubic-bezier(0.16, 1, 0.3, 1),
      height 0.4s cubic-bezier(0.16, 1, 0.3, 1),
      border-radius 0.4s ease;
    width: 120px; /* Wider notch */
    height: 40px; /* Sleeker height */
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }

  .nav-island.expanded {
    width: 500px; /* Expanded width */
    height: 60px; /* Taller when expanded */
    border-radius: 30px;
  }

  .nav-content {
    display: flex;
    align-items: center;
    width: 100%;
    height: 100%;
    position: relative;
  }

  .nav-toggle {
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    position: absolute;
    left: 50%; /* Center initially */
    transform: translateX(-50%);
    z-index: 2;
  }

  .nav-island.expanded .nav-toggle {
    left: 10px; /* Move to left when expanded */
    transform: translateX(0);
  }

  .nav-toggle:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .nav-links {
    display: flex;
    gap: 2rem;
    margin-left: 60px; /* Space for toggle */
    width: 100%;
    justify-content: space-around;
    white-space: nowrap;
  }

  .nav-links a {
    color: #fff;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    transition: color 0.2s ease;
    opacity: 0.8;
  }

  .nav-links a:hover {
    color: #b388ff;
    opacity: 1;
  }
</style>
