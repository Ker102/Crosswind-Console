<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import * as THREE from "three";

  let container: HTMLDivElement;
  let renderer: THREE.WebGLRenderer;
  let scene: THREE.Scene;
  let camera: THREE.PerspectiveCamera;
  let blob: THREE.Mesh;
  let frameId: number;

  onMount(() => {
    if (!container) return;

    // Scene setup
    scene = new THREE.Scene();

    // Camera setup
    const width = container.clientWidth;
    const height = container.clientHeight;
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.z = 5;

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 1);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 2);
    dirLight.position.set(5, 5, 5);
    scene.add(dirLight);

    // Blob Mesh
    const geometry = new THREE.SphereGeometry(1, 64, 64);
    const material = new THREE.MeshPhysicalMaterial({
      roughness: 0,
      metalness: 0.2,
      transmission: 1,
      thickness: 1.5,
      ior: 1.5,
      clearcoat: 1,
      clearcoatRoughness: 0.1,
      color: 0xffffff,
      emissive: 0xff00ff,
      emissiveIntensity: 0.2,
      iridescence: 1,
      iridescenceIOR: 1.3,
      iridescenceThicknessRange: [100, 400],
    });
    blob = new THREE.Mesh(geometry, material);
    scene.add(blob);

    // Animation Loop
    const animate = () => {
      frameId = requestAnimationFrame(animate);
      if (blob) {
        blob.rotation.y += 0.005;
        blob.rotation.x += 0.002;
      }
      renderer.render(scene, camera);
    };
    animate();

    // Resize handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(frameId);
      if (renderer) {
        renderer.dispose();
        container?.removeChild(renderer.domElement);
      }
      geometry.dispose();
      material.dispose();
    };
  });
</script>

<div bind:this={container} style="width: 100%; height: 100%;"></div>
