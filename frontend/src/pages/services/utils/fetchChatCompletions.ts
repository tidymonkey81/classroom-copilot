// utils/fetchChatCompletion.ts
export const fetchAndDecodeChatCompletion = async ({
    copilotConfig,
    messages,
    tools,
    headers,
    signal,
  }: {
    copilotConfig: any;
    messages: any;
    tools: any;
    headers: any;
    signal: any;
  }): Promise<any> => {
    const payload = {
      model: copilotConfig.body.model,
      messages: messages.map((msg: any) => ({ role: msg.role, content: msg.content })),
      options: copilotConfig.body.options,
    };
  
    console.log("Sending payload:", payload);
  
    const response = await fetch(copilotConfig.url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
      body: JSON.stringify(payload),
      signal,
    });
  
    console.log("Response status:", response.status);
    console.log("Response text:", await response.text());
  
    if (!response.ok) {
      throw new Error(`Failed to fetch chat completion: ${response.statusText}`);
    }
  
    const data = await response.json();
    return data;
  };
  