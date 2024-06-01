import React, { useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';

export default function Flow() {

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

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <div style={{ width: '100vw', height: '100%', zIndex: 0 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <Controls />
        <MiniMap />
        <Background variant="lines" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}