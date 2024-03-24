import React, { useEffect, useRef } from "react";
import * as THREE from "three";

const ThreeDBackground = ({ isRunning }) => {
  const mountRef = useRef(null);

  useEffect(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    mountRef.current.appendChild(renderer.domElement);

    // Cube setup
    const geometry = new THREE.BoxGeometry(10, 10, 10);
    const material = new THREE.MeshBasicMaterial({
      color: 0xff0000,
      wireframe: true,
    });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 30;

    // Animation
    const animate = () => {
      requestAnimationFrame(animate);
      const speed = isRunning ? 0.05 : 0.01;
      cube.rotation.x += speed;
      cube.rotation.y += speed;
      renderer.render(scene, camera);
    };

    animate();
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      mountRef.current.removeChild(renderer.domElement);
    };
  }, [isRunning]);

  return <div ref={mountRef} />;
};

export default ThreeDBackground;
