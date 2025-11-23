<script lang="ts">
  import { Canvas } from '@threlte/core'
  import Blob from './Blob.svelte'
  import { onMount } from 'svelte'

  let mounted = false
  onMount(() => {
    mounted = true
  })
</script>

<div class="landing-container">
  <div class="content">
    <div class="header">
      <span class="subtitle">EMBRACE OUR DESIGN ENHANCING</span>
      <h1 class="title">
        YOUR<br />
        JOURNEY
        <div class="blob-container">
          {#if mounted}
            <Canvas>
              <ambientLight intensity={1} />
              <directionalLight position={[5, 5, 5]} intensity={2} />
              <Blob />
            </Canvas>
          {/if}
        </div>
      </h1>
    </div>
    
    <button class="cta-button">
      GET STARTED <span class="arrow">→</span>
    </button>
  </div>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    overflow: hidden;
  }

  .landing-container {
    width: 100vw;
    height: 100vh;
    background: 
      radial-gradient(circle at 10% 20%, rgba(100, 100, 255, 0.4) 0%, transparent 40%),
      radial-gradient(circle at 90% 10%, rgba(255, 150, 255, 0.4) 0%, transparent 40%),
      radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.8) 0%, rgba(255, 200, 200, 0.2) 100%);
    background-color: #ffe0e0;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
  }

  .content {
    text-align: center;
    z-index: 10;
    position: relative;
  }

  .subtitle {
    font-size: 0.9rem;
    letter-spacing: 0.3em;
    color: #ff80ab;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: block;
  }

  .title {
    font-size: 12rem;
    line-height: 0.85;
    font-weight: 900;
    color: #1a1a1a;
    margin: 0;
    position: relative;
    letter-spacing: -0.05em;
  }

  .blob-container {
    position: absolute;
    width: 300px;
    height: 300px;
    top: 40%;
    right: 10%;
    transform: translate(50%, -50%);
    z-index: 20;
    pointer-events: none; /* Let clicks pass through to text if needed */
  }

  .cta-button {
    margin-top: 4rem;
    background: #000;
    color: #fff;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: 0.1em;
  }

  .cta-button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  }

  .arrow {
    color: #b388ff;
  }
</style>
