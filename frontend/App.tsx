import React from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './src/pages/Nav/Header';
import Sidebar from './src/pages/Nav/Sidebar';
import Home from './src/pages/homePage';
import Admin from './src/pages/adminPage';
import LLMTools from './src/pages/llmTools';
import TranscriptionTools from './src/pages/transcriptionTools';
import Flow from './src/pages/flowPage';
import Draw from './src/pages/drawPage';
import DrawFile from './src/pages/Labs/DrawFile';
import Slides from './src/pages/Labs/Slides';
import NotFound from './src/pages/Nav/NotFound';
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { AuthProvider, useAuth } from './src/pages/services/userContext';

const PrivateRoute = ({ children, roles }) => {
  const { user, role } = useAuth();

  if (!user || role === null) {
    return <div>Loading...</div>;
  }

  return roles.includes(role) ? children : <Navigate to="/" />;
};

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/admin" element={<PrivateRoute roles={['admin']}><Admin /></PrivateRoute>} />
      <Route path="/llm-tools" element={<LLMTools />} />
      <Route path="/transcription-tools" element={<TranscriptionTools />} />
      <Route path="/flow" element={<Flow />} />
      <Route path="/draw" element={<Draw />} />
      <Route path="/labs/draw-file" element={<DrawFile />} />
      <Route path="/labs/slides" element={<Slides />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export function WrappedApp() {
  return (
    <AuthProvider>
      <HashRouter>
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
          <Header />
          <div style={{ display: 'flex', flexGrow: 1, overflow: 'hidden' }}>
            <Sidebar />
            <div style={{ flexGrow: 1, overflow: 'hidden' }}>
              <CopilotKit url="http://localhost:8000/llm/openai_copilot_prompt">
                <div style={{ position: 'relative', zIndex: 1000 }}>
                  <CopilotPopup
                    instructions={"Help the user manage their day."}
                    defaultOpen={false}
                    labels={{
                      title: "Classroom Copilot",
                      initial: "Hi you! 👋 I can help you manage your day.",
                    }}
                    clickOutsideToClose={true}
                  />
                </div>
                <App />
              </CopilotKit>
            </div>
          </div>
        </div>
      </HashRouter>
    </AuthProvider>
  );
}
