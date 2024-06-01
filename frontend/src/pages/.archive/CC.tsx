import React, { useState, useCallback, useEffect } from 'react';
import { Tldraw } from 'tldraw';
import 'tldraw/tldraw.css';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  useReactFlow,
  ReactFlowProvider, // Import ReactFlowProvider
} from 'reactflow';
import 'reactflow/dist/style.css';

function TldrawApp({ isActive, camera, setCamera }) {
  useEffect(() => {
    if (isActive) {
      // Simulate updating Tldraw's camera/view settings
      console.log('Tldraw camera updated:', camera);
    }
  }, [isActive, camera]);

  return (
    <div style={{ width: '100%', height: '100%', display: isActive ? 'block' : 'none' }}>
      <Tldraw
        persistenceKey="cc-persistence-key"
        style={{ backgroundColor: 'transparent' }}
      />
    </div>
  );
}

function FlowApp({ isActive, camera, setCamera }) {
  const initialNodes = [
    { id: '1', position: { x: 20, y: 100 }, data: { label: '1' } },
    { id: '2', position: { x: 20, y: 200 }, data: { label: '2' } },
    { id: '3', position: { x: 20, y: 300 }, data: { label: '3' } },
    { id: '4', position: { x: 20, y: 400 }, data: { label: '4' } },
    { id: '5', position: { x: 20, y: 500 }, data: { label: '5' } },
  ];

  const initialEdges = [{ id: 'e1-2', source: '1', target: '2' }];

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const reactFlowInstance = useReactFlow();

  useEffect(() => {
    if (isActive && reactFlowInstance) {
      reactFlowInstance.setViewport(camera);
    }
  }, [isActive, camera, reactFlowInstance]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <div style={{ width: '100%', height: '100%', display: isActive ? 'block' : 'none' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
}

export default function App() {
  const [activeApp, setActiveApp] = useState('tldraw');
  const [camera, setCamera] = useState({ x: 0, y: 0, zoom: 1 });

  const toggleActiveApp = () => {
    setActiveApp(activeApp === 'tldraw' ? 'reactflow' : 'tldraw');
  };

  return (
    <div style={{ position: 'relative', height: '100%' }}>
      <button
        onClick={toggleActiveApp}
        style={{
          position: 'absolute',
          zIndex: 2,
          top: '10px',
          left: '10px',
          padding: '10px',
          background: 'white',
          border: '1px solid black',
        }}
      >
        Toggle to {activeApp === 'tldraw' ? 'React Flow' : 'Tldraw'}
      </button>
      <ReactFlowProvider> {/* Wrap the components that use React Flow with ReactFlowProvider */}
        <div style={{ position: 'absolute', width: '100%', height: '100%', zIndex: 0 }}>
          <FlowApp isActive={activeApp === 'reactflow'} camera={camera} setCamera={setCamera} />
        </div>
        <div style={{ position: 'absolute', width: '100%', height: '100%', zIndex: 1 }}>
          <TldrawApp isActive={activeApp === 'tldraw'} camera={camera} setCamera={setCamera} />
        </div>
      </ReactFlowProvider>
    </div>
  );
}
