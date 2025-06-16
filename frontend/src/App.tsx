import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { InitialView } from './components/InitialView';
import { ChatView } from './components/ChatView';
import { Sun, Moon } from 'lucide-react'; // Add icons for toggle

// Helper to swap CSS files
function setThemeCss(theme: 'light' | 'dark') {
  const darkHref = '/chatbot_style.css';
  const lightHref = '/chatbot_style_light.css';
  let link = document.getElementById('theme-style') as HTMLLinkElement | null;
  if (!link) {
    link = document.createElement('link');
    link.rel = 'stylesheet';
    link.id = 'theme-style';
    document.head.appendChild(link);
  }
  link.href = theme === 'dark' ? darkHref : lightHref;
}

export type Message = {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  // Metadata for assistant replies
  responseTime?: number; // seconds
  tokens?: number;
  cost?: number;
  sourceType?: 'youtube' | 'article';
  sourceTitle?: string;
};
export type ChatHistoryItem = { id: string; messages: Message[]; savedAt: Date };
export type Project = { id: string; name: string };
export function App() {
  // Theme state
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    return (localStorage.getItem('theme') as 'light' | 'dark') || 'dark';
  });

  useEffect(() => {
    setThemeCss(theme);
    document.body.classList.remove('theme-dark', 'theme-light');
    document.body.classList.add(`theme-${theme}`);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [chatHistory, setChatHistory] = useState<ChatHistoryItem[]>([]);
  const [activeProject, setActiveProject] = useState<string | null>(null);

  // Send message handler
  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    try {
      const resp = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: content,
          project_context: '',
          history: messages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });
      const data = await resp.json();
      const aiResponse = data.reply || '[No response from backend]';
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        role: 'assistant',
        timestamp: new Date(),
        responseTime: data.response_time,
        tokens: data.tokens,
        cost: data.cost,
        sourceType: data.source_type,
        sourceTitle: data.source_title,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 2).toString(),
          content: '[Backend error: ' + (err instanceof Error ? err.message : String(err)) + ']',
          role: 'assistant',
          timestamp: new Date(),
        },
      ]);
    }
    setIsLoading(false);
  };

  // New Chat handler
  const handleNewChat = () => {
    setMessages([]);
  };

  // Add Project handler
  const handleAddProject = (name: string) => {
    const id = Date.now().toString();
    setProjects((prev) => [...prev, { id, name }]);
    setActiveProject(id);
  };

  // Save Chat to history
  const handleSaveChat = () => {
    if (messages.length === 0) return;
    // Prevent duplicate saves of the same chat
    const alreadySaved = chatHistory.some(h => h.messages.length === messages.length && h.messages.every((m, i) => m.content === messages[i].content && m.role === messages[i].role));
    if (alreadySaved) return;
    setChatHistory((prev) => [
      ...prev,
      { id: Date.now().toString(), messages: [...messages], savedAt: new Date() },
    ]);
    setMessages([]); // Clear chat after saving
    alert('Chat saved to history!');
  };


  // Select chat from history
  const handleSelectChat = (id: string) => {
    const chat = chatHistory.find((c) => c.id === id);
    if (chat) setMessages(chat.messages);
  };

  return (
    <div className={`flex w-full h-screen theme-${theme}`}>
      <Sidebar
        projects={projects}
        onAddProject={handleAddProject}
        chatHistory={chatHistory}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
      />
      <main className="flex-grow flex flex-col h-screen overflow-hidden">
        {/* Top bar for theme toggle and Save Chat */}
        <div className="flex justify-end items-center gap-2 px-6 pt-4">
          {messages.length > 0 && !chatHistory.some(h => h.messages.length === messages.length && h.messages.every((m, i) => m.content === messages[i].content && m.role === messages[i].role)) && (
            <button
              className="bg-[#4a90e2] hover:bg-[#3a7bc2] text-white text-xs px-4 py-1 rounded transition-colors"
              onClick={handleSaveChat}
            >
              Save Chat
            </button>
          )}
          <button
            aria-label="Toggle theme"
            className="ml-2 rounded-full p-2 shadow hover:scale-105 transition"
            onClick={() => {
              const newTheme = theme === 'dark' ? 'light' : 'dark';
              console.log('Theme toggle clicked. Setting theme to', newTheme);
              setTheme(newTheme);
            }}
            style={{ border: '1px solid #ccc' }}
          >
            {theme === 'dark' ? <Sun size={20} color="#222" /> : <Moon size={20} color="#4a90e2" />}
          </button>
        </div>
        {messages.length === 0 ? (
          <InitialView onSendMessage={handleSendMessage} />
        ) : (
          <ChatView
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            // Remove Save Chat from ChatView, now handled in top bar
          />
        )}
      </main>
    </div>
  );
}

