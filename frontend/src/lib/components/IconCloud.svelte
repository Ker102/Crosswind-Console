<script lang="ts">
    import { onMount } from "svelte";
    import * as THREE from "three";
    import { RoundedBoxGeometry } from "three/examples/jsm/geometries/RoundedBoxGeometry.js";
    import { SVGLoader } from "three/examples/jsm/loaders/SVGLoader.js";
    import { FontLoader } from "three/examples/jsm/loaders/FontLoader.js";
    import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry.js";
    import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";

    let container: HTMLDivElement;
    let renderer: THREE.WebGLRenderer;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let iconGroup: THREE.Group;
    let frameId: number;
    let targetRotationY = 0;
    let targetRotationX = 0;

    // New Iridescent Icons
    const icons = [
        {
            name: "travel_1",
            type: "iridescent_tile",
            path: "M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z",
        }, // Airplane
        {
            name: "jobs_1",
            type: "iridescent_tile",
            path: "M10,2H14A2,2 0 0,1 16,4V6H20A2,2 0 0,1 22,8V19A2,2 0 0,1 20,21H4C2.89,21 2,20.1 2,19V8C2,6.89 2.89,6 4,6H8V4C8,2.89 8.89,2 10,2M14,6V4H10V6H14Z",
        }, // Briefcase
        {
            name: "trends_1",
            type: "iridescent_tile",
            path: "M16,6L18.29,8.29L13.41,13.17L9.41,9.17L2,16.59L3.41,18L9.41,12L13.41,16L19.71,9.71L22,12V6H16Z",
        }, // Trending Up
        {
            name: "travel_2",
            type: "iridescent_tile",
            path: "M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z",
        },
        {
            name: "jobs_2",
            type: "iridescent_tile",
            path: "M10,2H14A2,2 0 0,1 16,4V6H20A2,2 0 0,1 22,8V19A2,2 0 0,1 20,21H4C2.89,21 2,20.1 2,19V8C2,6.89 2.89,6 4,6H8V4C8,2.89 8.89,2 10,2M14,6V4H10V6H14Z",
        },
        {
            name: "trends_2",
            type: "iridescent_tile",
            path: "M16,6L18.29,8.29L13.41,13.17L9.41,9.17L2,16.59L3.41,18L9.41,12L13.41,16L19.71,9.71L22,12V6H16Z",
        },
    ];

    // Helper to create Iridescent Gradient Texture
    const createIridescentGradient = () => {
        const canvas = document.createElement("canvas");
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext("2d");
        if (ctx) {
            // Diagonal gradient: Brighter Purple to Blue to Pink
            const gradient = ctx.createLinearGradient(0, 0, 256, 256);
            gradient.addColorStop(0, "#4a1a6a"); // Brighter Dark Purple
            gradient.addColorStop(0.4, "#7a3a9a"); // Brighter Purple
            gradient.addColorStop(0.7, "#3388ff"); // Brighter Blue
            gradient.addColorStop(1, "#ff66ff"); // Brighter Pink
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, 256, 256);
        }
        return new THREE.CanvasTexture(canvas);
    };

    // Helper to load and extrude SVG (URL or Path String)
    const loadExtrudedSVG = (
        source: string,
        color: string | undefined,
        targetSize: number,
        isStandalone = false,
        customDepth?: number,
        isPathString = false,
    ) => {
        return new Promise<THREE.Group>((resolve, reject) => {
            const loader = new SVGLoader();

            const onLoad = (data: any) => {
                const paths = data.paths;
                const rootGroup = new THREE.Group();
                const orientGroup = new THREE.Group();
                const centerGroup = new THREE.Group();

                for (let i = 0; i < paths.length; i++) {
                    const path = paths[i];

                    // For iridescent icons, we use a special material
                    let material;
                    if (isPathString) {
                        // Metallic Symbol Material - Brighter
                        material = new THREE.MeshPhysicalMaterial({
                            color: 0xffffff, // White base for symbol
                            emissive: 0xffffff,
                            emissiveIntensity: 0.8, // Increased brightness
                            roughness: 0.1,
                            metalness: 1.0,
                            clearcoat: 1.0,
                        });
                    } else {
                        const materialColor = isStandalone
                            ? path.color || 0xffffff
                            : color
                              ? new THREE.Color(color)
                              : 0xffffff;

                        material = new THREE.MeshPhysicalMaterial({
                            color: materialColor,
                            emissive: materialColor,
                            emissiveIntensity: 0.3,
                            roughness: 0.2,
                            metalness: 0.1,
                            clearcoat: 1.0,
                            side: THREE.DoubleSide,
                        });
                    }

                    const shapes = SVGLoader.createShapes(path);

                    for (let j = 0; j < shapes.length; j++) {
                        const shape = shapes[j];
                        const geometry = new THREE.ExtrudeGeometry(shape, {
                            depth:
                                customDepth !== undefined
                                    ? customDepth
                                    : isStandalone
                                      ? 40
                                      : 10,
                            bevelEnabled: true,
                            bevelThickness: 2,
                            bevelSize: 1,
                            bevelSegments: 3,
                        });

                        const mesh = new THREE.Mesh(geometry, material);
                        centerGroup.add(mesh);
                    }
                }

                const box = new THREE.Box3().setFromObject(centerGroup);
                const size = new THREE.Vector3();
                const center = new THREE.Vector3();
                box.getSize(size);
                box.getCenter(center);

                centerGroup.position.copy(center).negate();
                orientGroup.add(centerGroup);
                orientGroup.scale.y = -1;
                rootGroup.add(orientGroup);

                const maxDim = Math.max(size.x, size.y);
                if (maxDim > 0) {
                    const scale = targetSize / maxDim;
                    rootGroup.scale.set(scale, scale, scale);
                }

                resolve(rootGroup);
            };

            if (isPathString) {
                const svgMarkup = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="${source}" fill="white"/></svg>`;
                const data = loader.parse(svgMarkup);
                onLoad(data);
            } else {
                loader.load(source, onLoad, undefined, (err) => {
                    console.warn("SVG Load Error:", err);
                    reject(err);
                });
            }
        });
    };

    onMount(() => {
        if (!container) return;

        // Scene setup
        scene = new THREE.Scene();

        // Camera setup
        const width = container.clientWidth;
        const height = container.clientHeight;
        camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
        camera.position.z = 20;

        // Renderer setup
        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        // --- ENVIRONMENT MAP (Reflections) ---
        const pmremGenerator = new THREE.PMREMGenerator(renderer);
        scene.environment = pmremGenerator.fromScene(
            new RoomEnvironment(),
            0.04,
        ).texture;

        // Lights - Updated for Iridescent Look (BRIGHTER)
        const ambientLight = new THREE.AmbientLight(0xffffff, 1.0);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 4.0);
        dirLight.position.set(5, 10, 7);
        dirLight.castShadow = true;
        scene.add(dirLight);

        // Colored Lights for Iridescence (BRIGHTER)
        const purpleLight = new THREE.PointLight(0xaa00aa, 5.0, 50);
        purpleLight.position.set(-10, 5, 10);
        scene.add(purpleLight);

        const blueLight = new THREE.PointLight(0x0088ff, 5.0, 50);
        blueLight.position.set(10, -5, 10);
        scene.add(blueLight);

        // Group to hold all icons
        iconGroup = new THREE.Group();
        scene.add(iconGroup);

        // Font Loader
        const fontLoader = new FontLoader();

        // Load Font once
        fontLoader.load(
            "https://threejs.org/examples/fonts/helvetiker_bold.typeface.json",
            (font) => {
                // Iridescent Tile Geometry (Thicker, smoother, larger)
                const iridescentTileGeometry = new RoundedBoxGeometry(
                    1.8, // Increased from 1.5
                    1.8, // Increased from 1.5
                    0.4,
                    8,
                    0.3,
                );

                icons.forEach(async (icon, i) => {
                    const group = new THREE.Group();

                    // Position: Donut Distribution (Avoid Center)
                    const angleStep = (Math.PI * 2) / icons.length;
                    const angle = i * angleStep;
                    const minRadius = 10.0; // Increased radius slightly for larger icons
                    const maxRadius = 15.0;
                    const r = minRadius + (i % 2) * (maxRadius - minRadius);
                    const x = Math.cos(angle) * r;
                    const y = Math.sin(angle) * r * 0.6; // Flattened Y
                    const z = Math.random() * 4 - 2;

                    group.position.set(x, y, z);
                    group.lookAt(camera.position);

                    // Random rotation
                    group.rotateX(Math.random() * Math.PI);
                    group.rotateY(Math.random() * Math.PI);

                    // --- TILE CREATION ---
                    let material: THREE.MeshPhysicalMaterial;

                    if (icon.type === "iridescent_tile") {
                        const gradientTexture = createIridescentGradient();
                        gradientTexture.colorSpace = THREE.SRGBColorSpace;

                        material = new THREE.MeshPhysicalMaterial({
                            map: gradientTexture,
                            color: 0xffffff,
                            metalness: 1.0, // Max metalness
                            roughness: 0.05, // Very smooth
                            iridescence: 1.0,
                            iridescenceIOR: 1.8,
                            clearcoat: 1.0,
                            clearcoatRoughness: 0.0,
                            emissive: 0x4a1a6a, // Brighter base emissive
                            emissiveIntensity: 0.6, // Increased from 0.2
                        });
                    } else {
                        // Fallback
                        const color = new THREE.Color("#ffffff");
                        material = new THREE.MeshPhysicalMaterial({ color });
                    }

                    const tile = new THREE.Mesh(
                        iridescentTileGeometry,
                        material,
                    );
                    tile.castShadow = true;
                    tile.receiveShadow = true;
                    group.add(tile);

                    // --- SYMBOL CREATION ---
                    if (icon.path) {
                        // Load from Path String
                        const svgMesh = await loadExtrudedSVG(
                            icon.path,
                            undefined,
                            1.0, // Target size increased
                            false,
                            5, // Custom depth
                            true, // isPathString
                        );

                        // Apply SAME material to symbol children
                        svgMesh.traverse((child) => {
                            if (child instanceof THREE.Mesh) {
                                child.material = material.clone(); // Clone to allow independent updates if needed
                                // Make symbol slightly brighter/different to stand out?
                                // User asked for "same materials and colors", so we stick to the clone.
                                // Maybe slightly more emissive to pop?
                                child.material.emissiveIntensity = 0.8;
                            }
                        });

                        svgMesh.position.z = 0.25; // Sit on top of 0.4 depth tile
                        group.add(svgMesh);
                    }

                    iconGroup.add(group);
                });
            },
        ); // End Font Loader

        const handleMouseMove = (event: MouseEvent) => {
            const x = (event.clientX / window.innerWidth) * 2 - 1;
            const y = -(event.clientY / window.innerHeight) * 2 + 1;
            targetRotationY = x * 0.15;
            targetRotationX = y * 0.1;
        };
        window.addEventListener("mousemove", handleMouseMove);

        const animate = () => {
            frameId = requestAnimationFrame(animate);
            if (iconGroup) {
                iconGroup.rotation.y +=
                    (targetRotationY - iconGroup.rotation.y) * 0.05;
                iconGroup.rotation.x +=
                    (targetRotationX - iconGroup.rotation.x) * 0.05;
            }
            renderer.render(scene, camera);
        };
        animate();

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
            window.removeEventListener("mousemove", handleMouseMove);
            cancelAnimationFrame(frameId);
            if (renderer) {
                renderer.dispose();
                container?.removeChild(renderer.domElement);
            }
        };
    });
</script>

<div bind:this={container} class="icon-cloud"></div>

<style>
    .icon-cloud {
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;
        pointer-events: none;
        z-index: 20; /* Layer above text */
    }
</style>
