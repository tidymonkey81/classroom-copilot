/* eslint-disable import/no-extraneous-dependencies */
/// <reference types="vitest" />
/// <reference types="vite/client" />

import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default ({ mode }) => {
  process.env = {...process.env, ...loadEnv(mode, process.cwd())};

  return defineConfig({
    plugins: [react()],
    server: {
      port: parseInt(process.env.VITE_FRONTEND_PORT || '8001', 10),
      host: true,
      proxy: {
        '/llm': {
          target: `http://${process.env.VITE_BACKEND_URL}:${process.env.VITE_BACKEND_PORT}`,
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/llm/, '')
        },
        '/database': {
          target: `http://${process.env.VITE_BACKEND_URL}:${process.env.VITE_BACKEND_PORT}`,
          changeOrigin: true,
          secure: false
        },
        '/transcribe': {
          target: `http://${process.env.VITE_BACKEND_URL}:${process.env.VITE_BACKEND_PORT}`,
          changeOrigin: true,
          secure: false
        }
      }
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./src/setupTests.ts'],
    },
  });
};
