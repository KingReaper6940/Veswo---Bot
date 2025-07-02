import { useState, useEffect } from 'react';
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
  SunIcon
} from '@heroicons/react/24/outline';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [problemInput, setProblemInput] = useState('');
  const [essayTopic, setEssayTopic] = useState('');
  const [essayLength, setEssayLength] = useState('medium');
  const [essayType, setEssayType] = useState('analytical');
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [llamaStatus, setLlamaStatus] = useState({ ready: false, loading: true, error: null });
  const [codeInput, setCodeInput] = useState('');
  const [codeQuestion, setCodeQuestion] = useState('');
  const [scienceSubject, setScienceSubject] = useState('physics');
  const [scienceQuestion, setScienceQuestion] = useState('');
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    // Listen for global shortcut
    const unlisten = listen('tauri://global-shortcut', (event) => {
      if (event.payload === 'CommandOrControl+Shift+A') {
        appWindow.show();
        appWindow.setFocus();
      }
    });

    return () => {
      unlisten.then(fn => fn());
    };
  }, []);

  // Check Llama status on component mount
  useEffect(() => {
    checkLlamaStatus();
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const checkLlamaStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/status');
      const data = await response.json();
      
      if (data.llama_ready) {
        setLlamaStatus({ ready: true, loading: false, error: null });
      } else {
        setLlamaStatus({ ready: false, loading: true, error: data.error });
        // Retry after 2 seconds
        setTimeout(checkLlamaStatus, 2000);
      }
    } catch (error) {
      setLlamaStatus({ ready: false, loading: true, error: 'Cannot connect to backend' });
      // Retry after 2 seconds
      setTimeout(checkLlamaStatus, 2000);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userMessage = input.trim();
    setInput('');
    setIsProcessing(true);

    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      // Send message to backend
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();
      const assistantMessage = { role: 'assistant', content: data.response, method: data.method };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleProblemSolve = async () => {
    if (!problemInput.trim() || isProcessing) return;
    
    setIsProcessing(true);
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: `Solve this problem: ${problemInput}` })
      });

      const data = await response.json();
      setMessages(prev => [...prev, 
        { role: 'user', content: `Problem: ${problemInput}` },
        { role: 'assistant', content: data.response, method: data.method }
      ]);
      setProblemInput('');
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error solving the problem.' 
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleEssayWrite = async () => {
    if (!essayTopic.trim() || isProcessing) return;
    
    setIsProcessing(true);
    try {
      const response = await fetch('http://localhost:8000/api/write/essay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: essayTopic,
          essay_type: essayType,
          length: essayLength
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, 
        { role: 'user', content: `Write essay about: ${essayTopic}` },
        { role: 'assistant', content: data.response, method: data.method }
      ]);
      setEssayTopic('');
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error writing the essay.' 
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

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

  const handleScreenshot = async () => {
    try {
      // This will be implemented in the Tauri backend
      const response = await invoke('take_screenshot');
      if (response.success) {
        setImagePreview(response.imageData);
        setSelectedImage({ name: 'screenshot.png', type: 'image/png' });
      }
    } catch (error) {
      console.error('Screenshot error:', error);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage || isProcessing) return;
    
    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      
      const response = await fetch('http://localhost:8000/api/analyze/image', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      setMessages(prev => [...prev, 
        { role: 'user', content: `[Image Analysis] ${input || "What's in this image?"}` },
        { role: 'assistant', content: data.response, method: data.method }
      ]);
      setInput('');
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error analyzing the image.' 
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const helpWithCode = async () => {
    if (!codeQuestion.trim() || isProcessing) return;

    setIsProcessing(true);
    try {
      const response = await fetch('http://localhost:8000/api/help/code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: codeInput,
          question: codeQuestion
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'user', content: `Code: ${codeInput}\nQuestion: ${codeQuestion}` }, { role: 'assistant', content: data.response, method: data.method }]);
      setCodeInput('');
      setCodeQuestion('');
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error helping with code. Please try again.' }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const helpWithScience = async () => {
    if (!scienceQuestion.trim() || isProcessing) return;

    setIsProcessing(true);
    try {
      const response = await fetch('http://localhost:8000/api/help/science', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject: scienceSubject,
          question: scienceQuestion
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'user', content: `Subject: ${scienceSubject}\nQuestion: ${scienceQuestion}` }, { role: 'assistant', content: data.response, method: data.method }]);
      setScienceQuestion('');
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error helping with science. Please try again.' }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const tabs = [
    { id: 'chat', name: 'Chat', icon: ChatBubbleLeftIcon },
    { id: 'math', name: 'Math Solver', icon: CalculatorIcon },
    { id: 'essay', name: 'Essay Writer', icon: DocumentTextIcon },
    { id: 'science', name: 'Science Helper', icon: BeakerIcon },
    { id: 'image', name: 'Image Analysis', icon: PhotoIcon },
    { id: 'code', name: 'Code Helper', icon: CodeBracketIcon },
  ];

  // Loading screen while Llama initializes
  if (llamaStatus.loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
                      <h2 className="text-2xl font-bold text-gray-800 mb-2">Initializing veswo1-bot</h2>
          <p className="text-gray-600 mb-4">Loading Llama AI model...</p>
          {llamaStatus.error && (
            <p className="text-red-500 text-sm">Error: {llamaStatus.error}</p>
          )}
          <div className="mt-4">
            <div className="flex space-x-2 justify-center">
              <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-4">This may take a few minutes on first run</p>
        </div>
      </div>
    );
  }

  // Error screen if Llama failed to initialize
  if (!llamaStatus.ready && llamaStatus.error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Initialization Failed</h2>
          <p className="text-gray-600 mb-4">Llama model could not be loaded</p>
          <p className="text-red-500 text-sm mb-4">{llamaStatus.error}</p>
          <button 
            onClick={checkLlamaStatus}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={darkMode ? 'dark' : ''}>
      {/* Header */}
      <div className="bg-white dark:bg-gray-900 shadow-lg border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <AcademicCapIcon className="h-8 w-8 text-indigo-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">veswo1-bot</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">Your AI Study Companion</p>
            </div>
          </div>
          <button
            onClick={() => setDarkMode((d) => !d)}
            className="ml-4 p-2 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700 transition-colors"
            title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {darkMode ? (
              <SunIcon className="h-6 w-6 text-yellow-400" />
            ) : (
              <MoonIcon className="h-6 w-6 text-gray-700" />
            )}
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Left Panel - Chat History */}
        <div className="flex-1 flex flex-col">
          {/* Chat messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <ChatBubbleLeftIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No messages yet</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Start a conversation, upload an image, or use one of the tools below.
                </p>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-lg rounded-lg px-4 py-3 shadow-sm flex items-end space-x-2 ${
                      message.role === 'user'
                        ? 'bg-indigo-600 text-white flex-row-reverse'
                        : 'bg-white text-gray-900 border border-gray-200'
                    }`}
                  >
                    {message.role === 'assistant' && (
                      <span className="inline-block align-bottom text-2xl mr-2">🤖</span>
                    )}
                    <div className="text-sm">{message.content}</div>
                  </div>
                </div>
              ))
            )}
            {isProcessing && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-900 border border-gray-200 rounded-lg px-4 py-3 shadow-sm flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-600"></div>
                  <span className="text-sm">Processing...</span>
                </div>
              </div>
            )}
          </div>

          {/* Input form */}
          <form onSubmit={handleSubmit} className="border-t bg-white p-4">
            <div className="flex space-x-4">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 transition-colors"
                disabled={isProcessing}
              />
              <button
                type="submit"
                disabled={isProcessing}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <PaperAirplaneIcon className="h-5 w-5" />
              </button>
            </div>
          </form>
        </div>

        {/* Right Panel - Tools */}
        <div className="w-80 bg-white border-l border-gray-200 p-6">
          {activeTab === 'math' && (
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <CalculatorIcon className="h-6 w-6 text-indigo-600" />
                <h2 className="text-lg font-semibold text-gray-900">Math Problem Solver</h2>
              </div>
              <p className="text-sm text-gray-600">
                Enter a math problem and I'll help you solve it step by step.
              </p>
              <textarea
                value={problemInput}
                onChange={(e) => setProblemInput(e.target.value)}
                placeholder="Enter your math problem here..."
                className="w-full h-32 rounded-lg border border-gray-300 px-3 py-2 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 resize-none"
                disabled={isProcessing}
              />
              <button
                onClick={handleProblemSolve}
                disabled={isProcessing || !problemInput.trim()}
                className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <CalculatorIcon className="h-5 w-5 mr-2" />
                Solve Problem
              </button>
            </div>
          )}

          {activeTab === 'essay' && (
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <DocumentTextIcon className="h-6 w-6 text-indigo-600" />
                <h2 className="text-lg font-semibold text-gray-900">Essay Writer</h2>
              </div>
              <p className="text-sm text-gray-600">
                Generate well-structured essays on any topic.
              </p>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Topic</label>
                <input
                  type="text"
                  value={essayTopic}
                  onChange={(e) => setEssayTopic(e.target.value)}
                  placeholder="Enter essay topic..."
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                  disabled={isProcessing}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Essay Type</label>
                <select
                  value={essayType}
                  onChange={(e) => setEssayType(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                  disabled={isProcessing}
                >
                  <option value="analytical">Analytical</option>
                  <option value="persuasive">Persuasive</option>
                  <option value="descriptive">Descriptive</option>
                  <option value="narrative">Narrative</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Length</label>
                <select
                  value={essayLength}
                  onChange={(e) => setEssayLength(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200"
                  disabled={isProcessing}
                >
                  <option value="short">Short</option>
                  <option value="medium">Medium</option>
                  <option value="long">Long</option>
                </select>
              </div>

              <button
                onClick={handleEssayWrite}
                disabled={isProcessing || !essayTopic.trim()}
                className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <DocumentTextIcon className="h-5 w-5 mr-2" />
                Write Essay
              </button>
            </div>
          )}

          {activeTab === 'image' && (
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <PhotoIcon className="h-6 w-6 text-indigo-600" />
                <h2 className="text-lg font-semibold text-gray-900">Image Analysis</h2>
              </div>
              <p className="text-sm text-gray-600">
                Upload an image or take a screenshot to analyze math problems, code, or anything else.
              </p>
              
              {/* Image Preview */}
              {imagePreview && (
                <div className="border border-gray-200 rounded-lg p-2">
                  <img 
                    src={imagePreview} 
                    alt="Preview" 
                    className="w-full h-32 object-contain rounded"
                  />
                </div>
              )}
              
              {/* Upload Buttons */}
              <div className="space-y-2">
                <button
                  onClick={handleScreenshot}
                  disabled={isProcessing}
                  className="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <CameraIcon className="h-5 w-5 mr-2" />
                  Take Screenshot
                </button>
                
                <label className="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer transition-colors">
                  <PhotoIcon className="h-5 w-5 mr-2" />
                  Upload Image
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                    disabled={isProcessing}
                  />
                </label>
              </div>
              
              <button
                onClick={analyzeImage}
                disabled={isProcessing || !selectedImage}
                className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-orange-600 hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <PhotoIcon className="h-5 w-5 mr-2" />
                Analyze Image
              </button>
            </div>
          )}

          {activeTab === 'code' && (
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <CodeBracketIcon className="h-6 w-6 text-indigo-600" />
                <h2 className="text-lg font-semibold text-gray-900">Code Helper</h2>
              </div>
              <p className="text-sm text-gray-600">
                Get help with programming, debugging, and code explanations.
              </p>
              
              <div className="space-y-3">
                <button
                  onClick={() => setInput('Explain this Python code: def hello(): print("Hello World")')}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Code Explanation</div>
                  <div className="text-sm text-gray-500">Understand what code does</div>
                </button>
                
                <button
                  onClick={() => setInput('Debug this JavaScript: for(let i=0; i<10; i++) { console.log(i) }')}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Code Debugging</div>
                  <div className="text-sm text-gray-500">Find and fix bugs</div>
                </button>
                
                <button
                  onClick={() => setInput('Write a function to calculate factorial in Python')}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Code Generation</div>
                  <div className="text-sm text-gray-500">Generate code examples</div>
                </button>
              </div>
            </div>
          )}

          {activeTab === 'science' && (
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <BeakerIcon className="h-6 w-6 text-indigo-600" />
                <h2 className="text-lg font-semibold text-gray-900">Science Helper</h2>
              </div>
              <p className="text-sm text-gray-600">
                Get help with physics, chemistry, and other science problems.
              </p>
              
              <div className="space-y-3">
                <button
                  onClick={() => setInput('Explain Newton\'s laws of motion')}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Physics Help</div>
                  <div className="text-sm text-gray-500">Laws, formulas, and concepts</div>
                </button>
                
                <button
                  onClick={() => setInput('Explain chemical reactions')}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Chemistry Help</div>
                  <div className="text-sm text-gray-500">Reactions, elements, and compounds</div>
                </button>
                
                <button
                  onClick={() => setInput('Explain cell biology')}
                  className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Biology Help</div>
                  <div className="text-sm text-gray-500">Cells, organisms, and systems</div>
                </button>
              </div>
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="space-y-4 text-center">
              <ChatBubbleLeftIcon className="mx-auto h-10 w-10 text-indigo-400" />
              <h2 className="text-lg font-semibold text-gray-900">Welcome to veswo1-bot</h2>
              <p className="text-sm text-gray-600">Start chatting or select a tool to get started!</p>
            </div>
          )}
        </div>
      </div>
      {/* Footer */}
      <footer className="w-full text-center py-2 text-xs text-gray-400 dark:text-gray-500 bg-white dark:bg-gray-900 border-t border-gray-100 dark:border-gray-800">
        Powered by Llama 3 7B
      </footer>
    </div>
  );
}

export default App; 