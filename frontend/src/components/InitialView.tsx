import React from 'react'
import { CheckCircleIcon } from 'lucide-react'
import { ChatInput } from './ChatInput'
interface InitialViewProps {
  onSendMessage: (message: string) => void
}
export const InitialView = ({ onSendMessage }: InitialViewProps) => {
  return (
    <div className="flex-grow flex flex-col justify-center items-center p-6 md:p-8 overflow-auto">
      <h1 className="text-2xl md:text-3xl font-semibold text-[#a0a0a0] mb-8 flex items-center gap-3">
        <CheckCircleIcon className="text-[#4a90e2]" size={28} />
        <span>How can I help you today?</span>
      </h1>
      <div className="w-full max-w-[800px]">
        <ChatInput onSendMessage={onSendMessage} />
      </div>
    </div>
  )
}
