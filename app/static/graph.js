import { UnrealBloomPass } from '//unpkg.com/three/examples/jsm/postprocessing/UnrealBloomPass.js';

document.addEventListener("DOMContentLoaded", () => {
    const infoBox = document.getElementById('node-info-box');
    const infoContent = document.getElementById('node-info-content');

    // Set up bloom effect
    const bloomEffect = new UnrealBloomPass();
    bloomEffect.strength = 0.5;
    bloomEffect.radius = 0.2;
    bloomEffect.threshold = 0;

    // Initialize graph
    const Graph = new ForceGraph3D(document.getElementById("3d-graph"), { controlType: 'orbit' })
        .enableNodeDrag(true)
        .backgroundColor('#000003')
        .nodeColor(node => node.color)
        .linkColor(link => link.color)
        .linkOpacity(0.1)
        .linkWidth(2)
        .linkCurvature('curvature')
        .linkDirectionalParticles("particles")
        .linkDirectionalParticleSpeed(d => d.particles * 0.001)
        .onNodeClick(node => {
            infoContent.innerHTML = `
                <strong>Name:</strong> ${node.name}<br>
            `;

            if (node.image) {
                infoContent.innerHTML += `
                    <strong>Image:</strong> ${node.image}<br>
                `;
            } else if (node.build) {
                infoContent.innerHTML += `
                    <strong>Build:</strong> ${node.build}<br>
                `;
            }
            
            infoBox.classList.remove('hidden');

            const distance = 40;
            const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

            const newPos = node.x || node.y || node.z
                ? { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }
                : { x: 0, y: 0, z: distance };

            Graph.cameraPosition(newPos, node, 3000);
        });

    // Adjust sizing
    const width = Graph.width();
    Graph.showNavInfo(false);
    Graph.width(width - (width > 1000 ? 220 : 20));
    Graph.height(Graph.height() - 100);

    Graph.postProcessingComposer().addPass(bloomEffect);

    // Use passed-in graph data instead of fetching
    Graph.graphData(GRAPH_DATA);
});
