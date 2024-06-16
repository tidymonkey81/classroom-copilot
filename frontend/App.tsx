import React, { useState } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './src/pages/Nav/Header';
import Sidebar from './src/pages/Nav/Sidebar';
import Login from './src/pages/loginPage';
import Home from './src/pages/homePage';
import Admin from './src/pages/adminPage';
import LLMTools from './src/pages/llmTools';
import TranscriptionTools from './src/pages/transcriptionTools';
import Flow from './src/pages/flowPage';
import Draw from './src/pages/drawPage';
import TranscriptionClient from './src/pages/testPage';
import LabsPage from './src/pages/labsPage';
import NotFound from './src/pages/Nav/NotFound';
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { AuthProvider, useAuth } from './src/pages/services/userContext';

const PrivateRoute = ({ children, roles = [] }) => {
  const { user, role } = useAuth();

  if (!user) {
    return <Navigate to="/" />;
  }

  if (role === null) {
    return <div>Loading...</div>;
  }

  return roles.length && !roles.includes(role) ? <Navigate to="/home" /> : children;
};

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<PrivateRoute><Home /></PrivateRoute>} />
      <Route path="/admin" element={<PrivateRoute roles={['admin']}><Admin /></PrivateRoute>} />
      <Route path="/llm-tools" element={<PrivateRoute roles={['admin', 'superuser']}><LLMTools /></PrivateRoute>} />
      <Route path="/transcription-tools" element={<PrivateRoute roles={['admin', 'superuser']}><TranscriptionTools /></PrivateRoute>} />
      <Route path="/flow" element={<PrivateRoute roles={['admin', 'superuser', 'teacher']}><Flow /></PrivateRoute>} />
      <Route path="/draw" element={<PrivateRoute roles={['admin', 'superuser', 'teacher']}><Draw /></PrivateRoute>} />
      <Route path="/test" element={<PrivateRoute roles={['admin', 'superuser', 'teacher']}><TranscriptionClient host="192.168.0.20" port={9090} /></PrivateRoute>} />
      <Route path="*" element={<NotFound />} />
      <Route path="/labs/" element={<PrivateRoute roles={['admin', 'superuser', 'teacher']}><LabsPage /></PrivateRoute>} />
    </Routes>
  );
}

export function WrappedApp() {
  const [isOpen, setIsOpen] = useState(true);
  return (
    <AuthProvider>
      <HashRouter>
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
          <Header />
          <div style={{ display: 'flex', flexGrow: 1, overflow: 'hidden' }}>
            <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />
            <div style={{ flexGrow: 1, transition: 'margin-left .5s', marginLeft: isOpen ? '0px' : '0px', width: isOpen ? 'calc(100% - 256px)' : '100%' }}>
              <CopilotKit url="http://192.168.0.20:9500/llm/openai_copilot_prompt">
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
