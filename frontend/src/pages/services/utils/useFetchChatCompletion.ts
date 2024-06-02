import { useState } from 'react';

export const useFetchChatCompletion = (copilotConfig: any) => {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchChatCompletion = async (messages: any, tools: any, headers: any, signal: any) => {
    setIsLoading(true);
    const payload = {
      model: copilotConfig.body.model,
      messages: messages.map((msg: any) => ({ role: msg.role, content: msg.content })),
      options: copilotConfig.body.options,
    };

    try {
      const response = await fetch(copilotConfig.url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...headers,
        },
        body: JSON.stringify(payload),
        signal,
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch chat completion: ${response.statusText}`);
      }

      const data = await response.json();
      setData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return { fetchChatCompletion, isLoading, data, error };
};
