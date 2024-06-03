import axios from 'axios';

export const sendPrompt = async (data: { model: string, prompt: string, temperature: number }, backendUrl: string) => {
  const response = await axios.post(`${backendUrl}/llm/ollama_text_prompt`, data);
  return response.data;
};

export const sendVisionPrompt = async (data: { model: string, imagePath: string, prompt: string }, backendUrl: string) => {
  const response = await axios.post(`${backendUrl}/llm/ollama_vision_prompt`, data);
  return response.data;
};
