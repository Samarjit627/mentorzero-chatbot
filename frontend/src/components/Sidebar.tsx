import React, { useState } from 'react';
import { PlusIcon } from 'lucide-react';
import { SidebarSection } from './SidebarSection';
import { UserProfile } from './UserProfile';
import type { Project, ChatHistoryItem } from '../App';

type SidebarProps = {
  projects: Project[];
  onAddProject: (name: string) => void;
  chatHistory: ChatHistoryItem[];
  onSelectChat: (id: string) => void;
  onNewChat: () => void;
};

export const Sidebar: React.FC<SidebarProps> = ({
  projects,
  onAddProject,
  chatHistory,
  onSelectChat,
  onNewChat,
}) => {
  const [addingProject, setAddingProject] = useState(false);
  const [projectName, setProjectName] = useState('');

  const handleAddProject = () => {
    if (projectName.trim()) {
      onAddProject(projectName.trim());
      setProjectName('');
      setAddingProject(false);
    }
  };

  return (
    <aside className="w-[260px] flex-shrink-0 bg-[#1f1f1f] flex flex-col border-r border-[#444444]">
      <div className="p-4 flex items-center gap-2 flex-shrink-0">
        <span className="w-6 h-6 bg-[#4a90e2] rounded flex items-center justify-center font-bold text-white">
          MZ
        </span>
        <span className="flex flex-col"><span className="text-base font-semibold">MentorZero</span><span className="text-xs italic lowercase text-[#a0a0a0]">ai assistant for startups</span></span>
      </div>
      <button
  className="flex items-center gap-2 bg-[#4a90e2] text-white py-2 px-3 mx-4 mb-4 rounded-md font-medium text-left transition-colors hover:bg-[#3a7bc2]"
  onClick={onNewChat}
>
  <PlusIcon size={16} />
  New Chat
</button>
      <nav className="flex-grow overflow-y-auto px-2 pb-4">
        <SidebarSection title="Projects" defaultOpen={true}>
  <ul>
    {projects.map((proj) => (
      <li key={proj.id}>
        <span className="block p-2 mb-1 rounded text-sm truncate bg-[#232323] text-[#e0e0e0]">
          {proj.name}
        </span>
      </li>
    ))}
  </ul>
  {addingProject ? (
    <div className="flex gap-1 mt-1">
      <input
        className="flex-1 rounded bg-[#232323] text-[#e0e0e0] px-2 py-1 text-sm border border-[#444]"
        autoFocus
        value={projectName}
        onChange={e => setProjectName(e.target.value)}
        onKeyDown={e => { if (e.key === 'Enter') handleAddProject(); if (e.key === 'Escape') setAddingProject(false); }}
        placeholder="Project name"
      />
      <button className="px-2 py-1 rounded bg-[#4a90e2] text-white text-xs" onClick={handleAddProject}>Add</button>
      <button className="px-2 py-1 rounded bg-[#444] text-[#ccc] text-xs" onClick={() => setAddingProject(false)}>Cancel</button>
    </div>
  ) : (
    <button
      className="w-full flex items-center gap-2 bg-[#222] text-[#a0a0a0] hover:bg-[#333] py-2 px-3 mb-2 rounded-md text-sm font-medium transition-colors"
      onClick={() => setAddingProject(true)}
    >
      <PlusIcon size={16} />
      Add Project
    </button>
  )}
</SidebarSection>
        <SidebarSection title="Chat History" defaultOpen={true}>
  <ul>
    {chatHistory.length === 0 && (
      <li className="text-xs text-[#888] px-2 py-1">No saved chats.</li>
    )}
    {chatHistory.map(chat => (
      <li key={chat.id}>
        <button
          className="block w-full text-left p-2 mb-1 rounded text-sm truncate bg-[#232323] hover:bg-[#333]"
          onClick={() => onSelectChat(chat.id)}
        >
          Saved chat at {chat.savedAt.toLocaleTimeString()}
        </button>
      </li>
    ))}
  </ul>
</SidebarSection>
        
      </nav>
      <UserProfile />
    </aside>
  )
}
