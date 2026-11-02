# threejs.md

- Stack: three, @react-three/fiber, @react-three/drei, gsap + ScrollTrigger, lenis. Check docs for the installed versions.
- One `<Canvas>` per page. Lazy-load it (`next/dynamic`, `ssr: false`).
- Use instancing for repeated meshes, shared geometries and materials, `dpr={[1, 2]}`.
- No allocations inside `useFrame`; reuse vectors. Dispose of textures and geometries on unmount.
- Drive scroll animation from one source (Lenis -> ScrollTrigger), not several.
- Pause rendering when the tab is hidden. Provide a static fallback for `prefers-reduced-motion` and low-power devices.
- Compress textures (KTX2/WebP) and models (Draco/meshopt).
