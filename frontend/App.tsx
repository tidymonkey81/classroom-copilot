import React from 'react'; // Add this line
import { HashRouter, Routes, Route } from 'react-router-dom';
import Home from './src/pages/Nav/Home';
import CCAdmin from './src/pages/Admin/CCAdmin';
import SchoolAdmin from './src/pages/Admin/SchoolAdmin';
import Flow from './src/pages/Flow/Flow';
import Draw from './src/pages/Draw/Draw';
import DrawFile from './src/pages/Draw/DrawFile';
import Slides from './src/pages/Draw/Slides';
import FlowDraw from './src/pages/CC/FlowDraw';
import CC from './src/pages/CC/CC';
import Propagator from './src/pages/Draw/Propagator';
import NotFound from './src/pages/Nav/NotFound';
import MenuBar from './src/pages/Nav/MenuBar';
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/cc-admin" element={<CCAdmin />} />
      <Route path="/school-admin" element={<SchoolAdmin />} />
      <Route path="/draw" element={<Draw />} />
      <Route path="/draw-file" element={<DrawFile />} />
      <Route path="/slides" element={<Slides />} />
      <Route path="/flow" element={<Flow />} />
      <Route path="/flow-draw" element={<FlowDraw />} />
      <Route path="/cc" element={<CC />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export function WrappedApp() {
  return (
    <HashRouter>
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        <MenuBar />
        <div style={{ flexGrow: 1, overflowY: 'auto', height: 'calc(100vh - 75px)' }}>
          <CopilotKit publicApiKey="your_api_key_here">
            <div style={{ position: 'relative', zIndex: 1000 }}>
              <CopilotPopup />
            </div>
            <App />
          </CopilotKit>
        </div>
      </div>
    </HashRouter>
  );
}