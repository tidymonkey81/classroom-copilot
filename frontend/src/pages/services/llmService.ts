export async function sendPrompt(prompt: string, backendUrl: string) {
    try {
      const response = await fetch(`${backendUrl}/llm/ollama`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: prompt }),
      });
      const data = await response.json();
      console.log(data); // Log or handle the response as needed
      return data.response;
    } catch (error) {
      console.error('Error sending prompt:', error);
      alert('Failed to sendprompt!');
    }
  }
