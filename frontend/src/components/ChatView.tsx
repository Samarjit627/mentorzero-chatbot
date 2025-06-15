import React, { useEffect, useRef } from 'react'
import { ChatInput } from './ChatInput'
import { ChatMessage } from './ChatMessage'
import type { Message } from '../App'
interface ChatViewProps {
  messages: Message[];
  isLoading: boolean;
  onSendMessage: (message: string) => void;
  onSaveChat?: () => void;
}
export const ChatView = ({
  messages,
  isLoading,
  onSendMessage,
  onSaveChat,
}: ChatViewProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    })
  }
  useEffect(() => {
    scrollToBottom()
  }, [messages])
  return (
    <div className="flex flex-col h-full bg-[#2b2b2b]">
      <div className="flex justify-end items-center px-6 pt-4">
        {onSaveChat && (
          <button
            className="bg-[#4a90e2] hover:bg-[#3a7bc2] text-white text-xs px-4 py-1 rounded transition-colors"
            onClick={onSaveChat}
          >
            Save Chat
          </button>
        )}
      </div>
      <div
        className="flex-grow overflow-y-auto p-6 md:p-8"
        style={{
          backgroundImage:
            'radial-gradient(circle at center, #2f2f2f 0%, #2b2b2b 100%)',
        }}
      >
        <div className="max-w-[800px] mx-auto">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="flex items-center gap-2 p-4 ml-16">
              <div className="flex space-x-2">
                <div
                  className="w-2.5 h-2.5 bg-[#4a90e2] rounded-full animate-bounce"
                  style={{
                    animationDelay: '0ms',
                    animationDuration: '600ms',
                  }}
                />
                <div
                  className="w-2.5 h-2.5 bg-[#4a90e2] rounded-full animate-bounce"
                  style={{
                    animationDelay: '200ms',
                    animationDuration: '600ms',
                  }}
                />
                <div
                  className="w-2.5 h-2.5 bg-[#4a90e2] rounded-full animate-bounce"
                  style={{
                    animationDelay: '400ms',
                    animationDuration: '600ms',
                  }}
                />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="p-4 md:p-6 bg-[#2b2b2b] border-t border-[#444444]">
        <ChatInput onSendMessage={onSendMessage} />
      </div>
    </div>
  )
}
