<script lang="ts">
  import { onDestroy, onMount } from 'svelte'
  import * as THREE from 'three'
  import { categoryMeta, selectedDomain } from '../state'
  import type { Domain } from '../types'

  let host: HTMLDivElement
  let renderer: THREE.WebGLRenderer | null = null
  let frame = 0
  let mesh: THREE.Mesh | null = null
  let scene: THREE.Scene | null = null
  let camera: THREE.PerspectiveCamera | null = null
  let domain: Domain = 'jobs'

  const unsubscribe = selectedDomain.subscribe((value) => {
    domain = value
    if (mesh) {
      const accent = categoryMeta[domain].accent
      ;(mesh.material as THREE.MeshStandardMaterial).color.set(accent)
    }
  })

  onMount(() => {
    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100)
    camera.position.set(0, 1.5, 4)

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(host.clientWidth, host.clientHeight)
    host.appendChild(renderer.domElement)

    const ambient = new THREE.AmbientLight(0xffffff, 0.5)
    scene.add(ambient)
    const dirLight = new THREE.DirectionalLight(0xffffff, 1)
    dirLight.position.set(5, 10, 7.5)
    scene.add(dirLight)

    const geometry = new THREE.TorusKnotGeometry(1, 0.3, 160, 20)
    const material = new THREE.MeshStandardMaterial({
      color: categoryMeta[domain].accent,
      metalness: 0.5,
      roughness: 0.3,
    })
    mesh = new THREE.Mesh(geometry, material)
    scene.add(mesh)

    const grid = new THREE.GridHelper(10, 10)
    scene.add(grid)

    const onResize = () => {
      if (!renderer || !camera) return
      const { clientWidth, clientHeight } = host
      camera.aspect = clientWidth / clientHeight
      camera.updateProjectionMatrix()
      renderer.setSize(clientWidth, clientHeight)
    }
    onResize()
    window.addEventListener('resize', onResize)

    const animate = () => {
      frame = requestAnimationFrame(animate)
      if (mesh) {
        mesh.rotation.x += 0.003
        mesh.rotation.y += 0.004
      }
      renderer?.render(scene!, camera!)
    }
    animate()

    return () => {
      window.removeEventListener('resize', onResize)
    }
  })

  onDestroy(() => {
    unsubscribe()
    if (frame) cancelAnimationFrame(frame)
    renderer?.dispose()
    mesh?.geometry.dispose()
    ;(mesh?.material as THREE.Material | undefined)?.dispose()
  })
</script>

<div class="scene" bind:this={host} aria-label="Category themed 3D scene"></div>

<style>
  .scene {
    width: 100%;
    height: 100%;
    border-radius: 1.5rem;
    background: radial-gradient(circle at top, rgba(255, 255, 255, 0.15), rgba(0, 0, 0, 0.85));
    overflow: hidden;
    position: relative;
  }

  :global(canvas) {
    width: 100% !important;
    height: 100% !important;
  }
</style>
