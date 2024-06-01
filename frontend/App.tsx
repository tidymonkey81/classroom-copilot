import React from 'react'; // Add this line
import { HashRouter, Routes, Route } from 'react-router-dom';
import Header from './src/pages/Nav/Header';
import Sidebar from './src/pages/Nav/Sidebar';
import Home from './src/pages/homePage';
import Admin from './src/pages/adminPage';
import Tools from './src/pages/toolsPage';
import Flow from './src/pages/flowPage';
import Draw from './src/pages/drawPage';
import DrawFile from './src/pages/Labs/DrawFile';
import Slides from './src/pages/Labs/Slides';
// import Propagator from './src/pages/Labs/Propagator';
import NotFound from './src/pages/Nav/NotFound';
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/admin" element={<Admin />} />
      <Route path="/tools" element={<Tools />} />
      <Route path="/flow" element={<Flow />} />
      <Route path="/draw" element={<Draw />} />
      <Route path="/labs/draw-file" element={<DrawFile />} />
      {/* <Route path="/labs/propagator" element={<Propagator />} /> */}
      <Route path="/labs/slides" element={<Slides />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export function WrappedApp() {
  return (
    <HashRouter>
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        <Header />
        <div style={{ display: 'flex', flexGrow: 1, overflow: 'hidden' }}>
          <Sidebar />
          <div style={{ flexGrow: 1, overflow: 'hidden' }}>
            <CopilotKit publicApiKey="your_api_key_here">
              <div style={{ position: 'relative', zIndex: 1000 }}>
                <CopilotPopup />
              </div>
              <App />
            </CopilotKit>
          </div>
        </div>
      </div>
    </HashRouter>
  );
}
