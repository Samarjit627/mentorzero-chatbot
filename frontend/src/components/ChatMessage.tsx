import React from 'react'
import type { Message } from '../App'
import { UserIcon, BrainCircuitIcon } from 'lucide-react'
interface ChatMessageProps {
  message: Message
}
export const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === 'user';
  // Icons for metadata
  const ClockIcon = () => (
    <svg className="inline-block mr-1" width="14" height="14" fill="none" stroke="#888" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
  );
  const TokenIcon = () => (
    <svg className="inline-block mr-1" width="14" height="14" fill="none" stroke="#888" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/></svg>
  );
  const DollarIcon = () => (
    <svg className="inline-block mr-1" width="14" height="14" fill="none" stroke="#888" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 3v18"/><path d="M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 1 1 0 7H6"/></svg>
  );
  const YoutubeIcon = () => (
    <svg className="inline-block mr-1" width="15" height="15" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a2.994 2.994 0 0 0-2.108-2.12C19.218 3.5 12 3.5 12 3.5s-7.218 0-9.39.566A2.994 2.994 0 0 0 .502 6.186C0 8.36 0 12 0 12s0 3.64.502 5.814a2.994 2.994 0 0 0 2.108 2.12C4.782 20.5 12 20.5 12 20.5s7.218 0 9.39-.566a2.994 2.994 0 0 0 2.108-2.12C24 15.64 24 12 24 12s0-3.64-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
  );
  const ArticleIcon = () => (
    <svg className="inline-block mr-1" width="15" height="15" fill="currentColor" viewBox="0 0 24 24"><path d="M19 2H8c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 18H8V4h11v16zM6 6H4v2h2V6zm0 4H4v2h2v-2zm0 4H4v2h2v-2zm0 4H4v2h2v-2z"/></svg>
  );

  return (
    <div className={`flex gap-6 mb-8 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div
        className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-[#4a90e2] text-white shadow-sm' : 'bg-[#2d2d2d] text-[#e0e0e0] border border-[#444444]'}`}
      >
        {isUser ? <UserIcon size={20} /> : <BrainCircuitIcon size={20} />}
      </div>
      <div
        className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[80%]`}
      >
        <div
          className={`px-4 py-2.5 rounded-xl ${isUser ? 'bg-[#1a1a1a] text-[#e0e0e0] border border-[#383838]' : 'bg-[#1a1a1a] border border-[#383838]'}`}
        >
          <p className="whitespace-pre-wrap leading-relaxed font-[450] text-[15px]">
            {message.content}
          </p>
        </div>
        {/* Metadata bubble for assistant */}
        {!isUser && (message.responseTime || message.tokens || message.cost || message.sourceType) && (
          <div className="flex items-center gap-2 mt-2 px-2">
            {/* Response time */}
            {typeof message.responseTime === 'number' && (
              <span className="flex items-center bg-[#232323] text-[#a0a0a0] text-xs rounded px-2 py-0.5 mr-1">
                <ClockIcon />
                {message.responseTime}s
              </span>
            )}
            {/* Tokens */}
            {typeof message.tokens === 'number' && (
              <span className="flex items-center bg-[#232323] text-[#a0a0a0] text-xs rounded px-2 py-0.5 mr-1">
                <TokenIcon />
                {message.tokens}
              </span>
            )}
            {/* Cost */}
            {typeof message.cost === 'number' && (
              <span className="flex items-center bg-[#232323] text-[#a0a0a0] text-xs rounded px-2 py-0.5 mr-1">
                <DollarIcon />
                ${message.cost.toFixed(5)}
              </span>
            )}
            {/* Source icon with tooltip */}
            {message.sourceType && message.sourceTitle && (
              <span className="flex items-center bg-[#232323] text-[#a0a0a0] text-xs rounded px-2 py-0.5 mr-1 cursor-pointer group relative" title={message.sourceTitle}>
                {message.sourceType === 'youtube' ? <YoutubeIcon /> : <ArticleIcon />}
                <span className="sr-only">{message.sourceTitle}</span>
                {/* Tooltip */}
                <span className="hidden group-hover:block absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 bg-[#333] text-xs text-white rounded shadow-lg whitespace-nowrap z-10">
                  {message.sourceTitle}
                </span>
              </span>
            )}
          </div>
        )}
        <span className="text-xs text-[#888888] mt-2 px-2">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>
    </div>
  );
}
