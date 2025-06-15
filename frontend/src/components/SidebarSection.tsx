import React, { useState } from 'react'
interface SidebarSectionProps {
  title: string
  children: React.ReactNode
  defaultOpen?: boolean
}
export const SidebarSection = ({
  title,
  children,
  defaultOpen = false,
}: SidebarSectionProps) => {
  const [isOpen, setIsOpen] = useState(defaultOpen)
  return (
    <details className="mb-4" open={isOpen}>
      <summary
        className="text-xs font-semibold text-[#a0a0a0] uppercase p-2 cursor-pointer list-none flex items-center gap-1 hover:text-[#e0e0e0]"
        onClick={(e) => {
          e.preventDefault()
          setIsOpen(!isOpen)
        }}
      >
        <span
          className="inline-block text-[8px] mr-1 transition-transform duration-200"
          style={{
            transform: isOpen ? 'rotate(90deg)' : 'none',
          }}
        >
          ►
        </span>
        {title}
      </summary>
      {children}
    </details>
  )
}
