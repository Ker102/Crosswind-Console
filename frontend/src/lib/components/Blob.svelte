<script lang="ts">
  import { T, useFrame } from '@threlte/core'
  import { MeshPhysicalMaterial, SphereGeometry } from 'three'

  let rotation = 0

  useFrame((state, delta) => {
    rotation += delta * 0.5
  })
</script>

<T.Mesh rotation.y={rotation} rotation.x={rotation * 0.5}>
  <T.SphereGeometry args={[1, 64, 64]} />
  <T.MeshPhysicalMaterial
    roughness={0}
    metalness={0.2}
    transmission={1}
    thickness={1.5}
    ior={1.5}
    clearcoat={1}
    clearcoatRoughness={0.1}
    color="#ffffff"
    emissive="#ff00ff"
    emissiveIntensity={0.2}
    iridescence={1}
    iridescenceIOR={1.3}
    iridescenceThicknessRange={[100, 400]}
  />
</T.Mesh>
