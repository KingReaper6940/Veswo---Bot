import { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';
import { appWindow } from '@tauri-apps/api/window';
import { 
  ChatBubbleLeftIcon, 
  PaperAirplaneIcon,
  AcademicCapIcon,
  MoonIcon,
  SunIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

function VeswoMessage({ content }) {
  // Try to render LaTeX if present, fallback to plain text
  // Render $$...$$ as block, $...$ as inline
  if (content.includes('$$')) {
    // Split by $$ and alternate between text and math
    const parts = content.split(/(\$\$.*?\$\$)/g);
    return (
      <div>
        {parts.map((part, i) => {
          if (part.startsWith('$$') && part.endsWith('$$')) {
            return <BlockMath key={i}>{part.slice(2, -2)}</BlockMath>;
          } else {
            return <span key={i}>{part}</span>;
          }
        })}
      </div>
    );
  } else if (content.includes('$')) {
    // Split by $ and alternate between text and inline math
    const parts = content.split(/(\$.*?\$)/g);
    return (
      <span>
        {parts.map((part, i) => {
          if (part.startsWith('$') && part.endsWith('$')) {
            return <InlineMath key={i}>{part.slice(1, -1)}</InlineMath>;
          } else {
            return <span key={i}>{part}</span>;
          }
        })}
      </span>
    );
  } else {
    return <span>{content}</span>;
  }
}

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [gemmaStatus, setGemmaStatus] = useState({ ready: false, loading: true, error: null });
  const [darkMode, setDarkMode] = useState(false);
  const [glassMode, setGlassMode] = useState(false);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    // Listen for global shortcut
    const unlisten = listen('tauri://global-shortcut', (event) => {
      if (event.payload === 'CommandOrControl+Shift+A') {
        appWindow.show();
        appWindow.setFocus();
      }
    });
    return () => { unlisten.then(fn => fn()); };
  }, []);

  useEffect(() => { checkGemmaStatus(); }, []);
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);
  useEffect(() => {
    // Call Tauri to set glass mode
    invoke('set_glass_mode', { enable: glassMode });
  }, [glassMode]);

  const checkGemmaStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/status');
      const data = await response.json();
      if (data.gemma_ready) {
        setGemmaStatus({ ready: true, loading: false, error: null });
      } else {
        setGemmaStatus({ ready: false, loading: true, error: data.error });
        setTimeout(checkGemmaStatus, 2000);
      }
    } catch (error) {
      setGemmaStatus({ ready: false, loading: true, error: 'Cannot connect to backend' });
      setTimeout(checkGemmaStatus, 2000);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;
    const userMessage = input.trim();
    setInput('');
    setIsProcessing(true);
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response, method: data.method }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setIsProcessing(false);
    }
  };

  // Minimal UI for glass mode
  if (glassMode) {
    return (
      <div 
        className="flex flex-col items-center justify-center min-h-screen bg-transparent" 
        style={{
          height:'100vh',
          backdropFilter:'blur(8px)',
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          WebkitAppRegion: 'drag', // Makes the window draggable
          cursor: 'move'
        }}
      >
        <div className="flex items-center justify-between w-full px-2 py-1" style={{WebkitAppRegion: 'no-drag'}}>
          <button onClick={()=>setGlassMode(false)} className="text-gray-500 hover:text-indigo-600"><EyeSlashIcon className="h-5 w-5"/></button>
          <span className="text-lg font-bold text-indigo-700">Veswo Bot</span>
          <button onClick={()=>setDarkMode(!darkMode)} className="focus:outline-none">{darkMode ? <SunIcon className="h-5 w-5 text-yellow-400" /> : <MoonIcon className="h-5 w-5 text-gray-600" />}</button>
        </div>
        <form onSubmit={handleSubmit} className="flex items-center space-x-2 w-full px-2 mt-2" style={{WebkitAppRegion: 'no-drag'}}>
          <input
            type="text"
            className="flex-1 rounded-lg border px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-900 dark:text-white bg-white/90"
            placeholder="Type..."
            value={input}
            onChange={e=>setInput(e.target.value)}
            disabled={isProcessing}
            style={{minWidth:0}}
          />
          <button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-2 py-1" disabled={isProcessing}>
            <PaperAirplaneIcon className="h-4 w-4" />
          </button>
        </form>
        <div className="flex-1 w-full overflow-y-auto mt-2" ref={chatContainerRef} style={{maxHeight:80, WebkitAppRegion: 'no-drag'}}>
          {messages.slice(-3).map((msg, i) => (
            <div key={i} className={`flex ${msg.role==='user'?'justify-end':'justify-start'} mb-1`}>
              <div className={`rounded-lg px-2 py-1 max-w-[90%] text-xs ${msg.role==='user'?'bg-indigo-100/90 text-indigo-900':'bg-gray-100/90 dark:bg-gray-700/90 text-gray-900 dark:text-gray-100'}`}>
                <VeswoMessage content={msg.content} />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Normal UI rendering
  return (
    <div className={`min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900`} style={{height: '100vh', backgroundColor: darkMode ? '#18181b' : '#f9fafb'}}>
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b bg-white dark:bg-gray-800">
        <div className="flex items-center space-x-2">
          <AcademicCapIcon className="h-7 w-7 text-indigo-600" />
          <span className="text-2xl font-bold text-gray-900 dark:text-white">Veswo Bot</span>
          <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">Your AI Study Companion</span>
        </div>
        <div className="flex items-center space-x-4">
          <button onClick={() => setGlassMode(!glassMode)} className="focus:outline-none" title="Toggle Glass Mode">
            {glassMode ? <EyeSlashIcon className="h-6 w-6 text-indigo-600" /> : <EyeIcon className="h-6 w-6 text-indigo-600" />}
          </button>
          <button onClick={() => setDarkMode(!darkMode)} className="focus:outline-none">
            {darkMode ? <SunIcon className="h-6 w-6 text-yellow-400" /> : <MoonIcon className="h-6 w-6 text-gray-600" />}
          </button>
        </div>
      </header>
      {/* Simple header - no tabs needed */}
      <div className="px-6 py-2 bg-white dark:bg-gray-800 border-b">
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600 dark:text-gray-300">All features available in chat</span>
        </div>
      </div>
      {/* Main Content - Simplified Chat Only */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-2" style={{minHeight:0}}>
        <div className="flex flex-col w-full max-w-2xl flex-1 h-full" style={{height:'100%', minHeight:0}}>
          <div ref={chatContainerRef} className="flex-1 overflow-y-auto bg-white dark:bg-gray-800 rounded-lg p-4 mb-2" style={{minHeight:0}}>
            {messages.length === 0 ? (
              <div className="text-center text-gray-400 py-12">
                No messages yet<br/>
                Start a conversation or ask me anything!
              </div>
            ) : (
              messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role==='user'?'justify-end':'justify-start'} mb-2`}>
                  <div className={`rounded-lg px-4 py-2 max-w-[80%] ${msg.role==='user'?'bg-indigo-100 text-indigo-900':'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
                    <VeswoMessage content={msg.content} />
                  </div>
                </div>
              ))
            )}
          </div>
          <form onSubmit={handleSubmit} className="flex items-center space-x-2 mt-auto">
            <input
              type="text"
              className="flex-1 rounded-lg border px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-900 dark:text-white"
              placeholder="Type your message..."
              value={input}
              onChange={e=>setInput(e.target.value)}
              disabled={isProcessing}
            />
            <button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2" disabled={isProcessing}>
              <PaperAirplaneIcon className="h-5 w-5" />
            </button>
          </form>
        </div>
      </main>
      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-2 bg-white dark:bg-gray-900 border-t">
        Powered by Gemma AI
      </footer>
    </div>
  );
}

export default App; 