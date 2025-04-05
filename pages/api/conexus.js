export default async function handler(req, res) {
    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'Method not allowed' });
    }
  
    const { messages } = req.body;
  
    //log incoming request from frontend
    console.log("Incoming messages:", messages);
  
    try {
      const apiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'gpt-4o',
          temperature: 0.8,
          messages: [
            {
              role: 'system',
              content:
                "You are Conexus, a friendly, approachable tutor with a passion for academics and a knack for drawing creative, relatable metaphors from any interest the user chooses. Always use a warm tone, clear language, and end each reply with a follow-up question.",
            },
            ...messages,
          ],
        }),
      });
  
      const data = await apiResponse.json();
  
      //log raw response from OpenAI
      console.log("gpt response:", JSON.stringify(data, null, 2));
  
      //handle API errors or missing fields
      if (!data.choices || !data.choices[0] || !data.choices[0].message) {
        return res.status(500).json({
          reply: 'gpt response missing or malformed. see console for details.',
        });
      }
  
      const reply = data.choices[0].message.content;
      res.status(200).json({ reply });
    } catch (err) {
      console.error('API call failed:', err);
      res.status(500).json({ error: 'Failed to connect to gpt' });
    }
  }
  
