import { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';
import { appWindow } from '@tauri-apps/api/window';
import { 
  ChatBubbleLeftIcon, 
  PaperAirplaneIcon,
  AcademicCapIcon,
  CalculatorIcon,
  DocumentTextIcon,
  CameraIcon,
  BeakerIcon,
  BookOpenIcon,
  PhotoIcon,
  CodeBracketIcon,
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
  const [activeTab, setActiveTab] = useState('chat');
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [ocrText, setOcrText] = useState('');
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

  // OCR logic
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleOcr = async () => {
    if (!selectedImage) return;
    setOcrText('');
    setIsProcessing(true);
    const reader = new FileReader();
    reader.onload = async (e) => {
      const imageData = e.target.result;
      try {
        const response = await fetch('http://localhost:8000/api/ocr', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_data: imageData })
        });
        const data = await response.json();
        setOcrText(data.text || data.error || 'No text found.');
      } catch (error) {
        setOcrText('OCR failed.');
      } finally {
        setIsProcessing(false);
      }
    };
    reader.readAsDataURL(selectedImage);
  };

  // Minimal UI for glass mode
  if (glassMode) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-transparent" style={{height:'100vh',backdropFilter:'blur(0px)'}}>
        <div className="flex items-center justify-between w-full px-2 py-1">
          <button onClick={()=>setGlassMode(false)} className="text-gray-500 hover:text-indigo-600"><EyeSlashIcon className="h-5 w-5"/></button>
          <span className="text-lg font-bold text-indigo-700">Veswo Bot</span>
          <button onClick={()=>setDarkMode(!darkMode)} className="focus:outline-none">{darkMode ? <SunIcon className="h-5 w-5 text-yellow-400" /> : <MoonIcon className="h-5 w-5 text-gray-600" />}</button>
        </div>
        <form onSubmit={handleSubmit} className="flex items-center space-x-2 w-full px-2 mt-2">
          <input
            type="text"
            className="flex-1 rounded-lg border px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-900 dark:text-white"
            placeholder="Type..."
            value={input}
            onChange={e=>setInput(e.target.value)}
            disabled={isProcessing}
            style={{minWidth:0}}
          />
          <button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-2 py-1" disabled={isProcessing}>
            <PaperAirplaneIcon className="h-4 w-4" />
          </button>
          <label className="cursor-pointer ml-1">
            <CameraIcon className="h-5 w-5 text-gray-500 hover:text-indigo-600" />
            <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
          </label>
        </form>
        {imagePreview && <img src={imagePreview} alt="Preview" className="max-h-16 mt-1 rounded shadow" />}
        {ocrText && <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-2 w-full text-xs whitespace-pre-wrap mt-1">{ocrText}</div>}
        <div className="flex-1 w-full overflow-y-auto mt-2" ref={chatContainerRef} style={{maxHeight:80}}>
          {messages.slice(-3).map((msg, i) => (
            <div key={i} className={`flex ${msg.role==='user'?'justify-end':'justify-start'} mb-1`}>
              <div className={`rounded-lg px-2 py-1 max-w-[90%] text-xs ${msg.role==='user'?'bg-indigo-100 text-indigo-900':'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
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
    <div className={`min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900`} style={{height: '100vh'}}>
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
      {/* Tabs */}
      <nav className="flex space-x-4 px-6 py-2 bg-white dark:bg-gray-800 border-b">
        <button className={activeTab==='chat'? 'font-bold text-indigo-600':'text-gray-600 dark:text-gray-300'} onClick={()=>setActiveTab('chat')}><ChatBubbleLeftIcon className="inline h-5 w-5 mr-1"/>Chat</button>
        <button className={activeTab==='math'? 'font-bold text-indigo-600':'text-gray-600 dark:text-gray-300'} onClick={()=>setActiveTab('math')}><CalculatorIcon className="inline h-5 w-5 mr-1"/>Math Solver</button>
        <button className={activeTab==='essay'? 'font-bold text-indigo-600':'text-gray-600 dark:text-gray-300'} onClick={()=>setActiveTab('essay')}><DocumentTextIcon className="inline h-5 w-5 mr-1"/>Essay Writer</button>
        <button className={activeTab==='science'? 'font-bold text-indigo-600':'text-gray-600 dark:text-gray-300'} onClick={()=>setActiveTab('science')}><BeakerIcon className="inline h-5 w-5 mr-1"/>Science Helper</button>
        <button className={activeTab==='ocr'? 'font-bold text-indigo-600':'text-gray-600 dark:text-gray-300'} onClick={()=>setActiveTab('ocr')}><CameraIcon className="inline h-5 w-5 mr-1"/>Image Analysis</button>
        <button className={activeTab==='code'? 'font-bold text-indigo-600':'text-gray-600 dark:text-gray-300'} onClick={()=>setActiveTab('code')}><CodeBracketIcon className="inline h-5 w-5 mr-1"/>Code Helper</button>
      </nav>
      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-2" style={{minHeight:0}}>
        {/* Chat area */}
        {(activeTab==='chat'||activeTab==='math'||activeTab==='essay'||activeTab==='science'||activeTab==='code') && (
          <div className="flex flex-col w-full max-w-2xl flex-1 h-full" style={{height:'100%', minHeight:0}}>
            <div ref={chatContainerRef} className="flex-1 overflow-y-auto bg-white dark:bg-gray-800 rounded-lg p-4 mb-2" style={{minHeight:0}}>
              {messages.length === 0 ? (
                <div className="text-center text-gray-400 py-12">No messages yet<br/>Start a conversation, upload an image, or use one of the tools below.</div>
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
        )}
        {/* OCR Tab */}
        {activeTab==='ocr' && (
          <div className="w-full max-w-2xl flex flex-col items-center">
            <div className="mb-4">
              <input type="file" accept="image/*" onChange={handleImageUpload} />
              {imagePreview && <img src={imagePreview} alt="Preview" className="max-h-48 mt-2 rounded shadow" />}
            </div>
            <button onClick={handleOcr} className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg px-4 py-2 mb-2" disabled={isProcessing || !selectedImage}>Extract Text</button>
            {ocrText && <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 w-full whitespace-pre-wrap mt-2">{ocrText}</div>}
          </div>
        )}
      </main>
      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-2 bg-white dark:bg-gray-900 border-t">
        Powered by Gemma AI
      </footer>
    </div>
  );
}

export default App; 