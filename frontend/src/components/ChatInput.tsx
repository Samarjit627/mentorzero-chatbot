import React, { useEffect, useState, useRef } from 'react'
import { PlusIcon, SendIcon, ChevronDownIcon } from 'lucide-react'
interface ChatInputProps {
  onSendMessage: (message: string) => void
}
export const ChatInput = ({ onSendMessage }: ChatInputProps) => {
  const [message, setMessage] = useState('')
  const [isButtonDisabled, setIsButtonDisabled] = useState(true)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const autoResizeTextarea = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = `${Math.min(textarea.scrollHeight, 250)}px`
    }
  }
  useEffect(() => {
    setIsButtonDisabled(message.trim().length === 0)
  }, [message])
  useEffect(() => {
    autoResizeTextarea()
  }, [message])
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (!isButtonDisabled) {
        sendMessage()
      }
    }
  }
  const sendMessage = () => {
    if (message.trim()) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }
  return (
    <div className="w-full max-w-[800px] mx-auto">
      <div className="bg-[#2d2d2d] border border-[#444444] rounded-2xl p-3">
        <div className="flex items-start gap-3">
          <button
            className="mt-1.5 text-[#888888] p-2 rounded-lg hover:bg-[#3a3a3a] hover:text-[#e0e0e0] transition-colors"
            title="Attach file"
          >
            <PlusIcon size={20} />
          </button>
          <textarea
            ref={textareaRef}
            className="flex-grow min-h-[24px] max-h-[250px] overflow-y-auto text-base leading-relaxed py-2 bg-transparent focus:outline-none placeholder:text-[#666666]"
            placeholder="Ask me anything..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          <button
            className={`rounded-full w-10 h-10 flex items-center justify-center mt-1 transition-all ${!isButtonDisabled ? 'bg-[#4a90e2] hover:bg-[#3a7bc2] text-white' : 'bg-[#3a3a3a] text-[#666666] cursor-not-allowed'}`}
            title="Send message"
            disabled={isButtonDisabled}
            onClick={sendMessage}
          >
            <SendIcon size={18} />
          </button>
        </div>
        <div className="flex justify-end items-center mt-2 gap-3 pl-12">
          <div className="model-selector">
            <button className="text-xs text-[#888888] bg-[#3a3a3a] py-1.5 px-3 rounded-lg flex items-center gap-2 hover:bg-[#444444] transition-colors">
              <span>Default Model</span>
              <ChevronDownIcon size={12} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
