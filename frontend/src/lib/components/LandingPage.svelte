<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { fly, fade } from "svelte/transition";
  import IconCloud from "./IconCloud.svelte";
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
  } from "lucide-svelte";

  let text = $state("");
  const phrases = ["TRAVEL", "JOBS", "TRENDS"];
  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let timer: number;

  let showLanding = $state(true);

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
      // Scroll back up to hero
      showLanding = true;
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
  <div class="logo">Crosswind Console</div>

  {#if showLanding}
    <div
      class="landing-content"
      out:fly={{ y: -1000, duration: 1000, opacity: 0 }}
    >
      <IconCloud />
      <div class="content">
        <div class="header">
          <div class="title-wrapper">
            <h1 class="title">
              ACCESS THOUSANDS OF RESOURCES FROM BRANDS AND SERVICES WITH AI TO
              GET STARTED WITH<br />
              <span class="highlight">{text}</span><span class="cursor">|</span>
            </h1>
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
      in:fly={{ y: 1000, duration: 1000, delay: 500 }}
    >
      <!-- Background Logos (Only in Selection View) -->
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

      <h2 class="selection-title">CHOOSE YOUR PATH</h2>
      <div class="cards">
        <div class="card travel">
          <div class="card-icons">
            <Plane size={24} />
            <Mountain size={24} />
            <Car size={24} />
          </div>
          <h3>TRAVEL</h3>
          <p>Explore the world with best deals.</p>
        </div>
        <div class="card jobs">
          <div class="card-icons">
            <Laptop size={24} />
            <Coffee size={24} />
            <AlarmClock size={24} />
          </div>
          <h3>JOBS</h3>
          <p>Find your next career opportunity.</p>
        </div>
        <div class="card trends">
          <div class="card-icons">
            <Twitter size={24} />
            <Instagram size={24} />
            <Facebook size={24} />
            <Linkedin size={24} />
          </div>
          <h3>TRENDS</h3>
          <p>Stay ahead with latest insights.</p>
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

    /* Radial Fade from Bottom (Typewriter Text) - Relaxed Radius */
    background: radial-gradient(
      circle at 50% 100%,
      #ff3bff 0%,
      #ecbfbf 25%,
      #5c24ff 50%,
      #1a1a1a 100%
    );
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    display: inline-block; /* Ensure background-clip works */
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
    text-align: center;
    z-index: 20; /* Above logos */
  }

  .selection-title {
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
</style>
