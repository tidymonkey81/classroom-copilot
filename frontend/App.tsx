import React from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './src/pages/Nav/Header';
import Sidebar from './src/pages/Nav/Sidebar';
import Home from './src/pages/homePage';
import Admin from './src/pages/adminPage';
import Tools from './src/pages/toolsPage';
import Flow from './src/pages/flowPage';
import Draw from './src/pages/drawPage';
import DrawFile from './src/pages/Labs/DrawFile';
import Slides from './src/pages/Labs/Slides';
import NotFound from './src/pages/Nav/NotFound';
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { fetchAndDecodeChatCompletion } from "./src/pages/services/utils/fetchChatCompletions";
import { useFetchChatCompletion } from './src/pages/services/utils/useFetchChatCompletion';
import { AuthProvider, useAuth } from './src/pages/services/userContext';

const PrivateRoute = ({ children, roles }) => {
  const { user } = useAuth();
  return user && roles.includes(user.role) ? children : <Navigate to="/" />;
};

export function App() {
  return (
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<PrivateRoute roles={['admin']}><Admin /></PrivateRoute>} />
        <Route path="/tools" element={<Tools />} />
        <Route path="/flow" element={<Flow />} />
        <Route path="/draw" element={<Draw />} />
        <Route path="/labs/draw-file" element={<DrawFile />} />
        <Route path="/labs/slides" element={<Slides />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
  );
}

export function WrappedApp() {
  const copilotConfig = { url: "http://localhost:8000/llm/openai_copilot_prompt", body: { model: "gpt-4", options: {} }};
  const { fetchChatCompletion } = useFetchChatCompletion(copilotConfig);

  return (
    <AuthProvider>
      <HashRouter>
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
          <Header />
          <div style={{ display: 'flex', flexGrow: 1, overflow: 'hidden' }}>
            <Sidebar />
            <div style={{ flexGrow: 1, overflow: 'hidden' }}>
              <CopilotKit
                url="http://localhost:8000/llm/openai_copilot_prompt"
                fetchChatCompletion={fetchChatCompletion}
              >
                <div style={{ position: 'relative', zIndex: 1000 }}>
                  <CopilotPopup
                    instructions={"Help the user manage their day."}
                    defaultOpen={true}
                    labels={{
                      title: "Classroom Copilot",
                      initial: "Hi you! 👋 I can help you manage your day.",
                    }}
                    clickOutsideToClose={false}
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
