import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        "Hi there! I'm Conexus — your personal tutor! What topic would you like to explore today, and what are your interests so I can tailor the explanation just for you?",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    const res = await fetch('/api/conexus', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: newMessages }),
    });

    const data = await res.json();
    setMessages([...newMessages, { role: 'assistant', content: data.reply }]);
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="h-[500px] overflow-y-scroll border rounded p-4 bg-gray-50 mb-4 shadow">
        {messages.map((msg, i) => (
          <div key={i} className="mb-4">
            <p className={`text-sm ${msg.role === 'user' ? 'text-blue-600' : 'text-green-700'}`}>
              <strong>{msg.role === 'user' ? 'You' : 'Conexus'}:</strong> {msg.content}
            </p>
          </div>
        ))}
        {loading && <p className="text-green-700 italic">Conexus is thinking...</p>}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          className="border p-2 flex-1 rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about any topic — and share your interests!"
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}
