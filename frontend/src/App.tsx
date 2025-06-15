import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { InitialView } from './components/InitialView';
import { ChatView } from './components/ChatView';
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
    <div className="flex w-full h-screen bg-[#2b2b2b] text-[#e0e0e0]">
      <Sidebar
        projects={projects}
        onAddProject={handleAddProject}
        chatHistory={chatHistory}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
      />
      <main className="flex-grow flex flex-col h-screen overflow-hidden">
        {messages.length === 0 ? (
          <InitialView onSendMessage={handleSendMessage} />
        ) : (
          <ChatView
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            onSaveChat={messages.length > 0 && !chatHistory.some(h => h.messages.length === messages.length && h.messages.every((m, i) => m.content === messages[i].content && m.role === messages[i].role)) ? handleSaveChat : undefined}
          />
        )}
      </main>
    </div>
  );
}
