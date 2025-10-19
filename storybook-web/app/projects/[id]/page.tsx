'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Project } from '../../lib/types';
import { api } from '../../lib/api';
import ChatPanel from '../../components/ChatPanel';
import EditorPanel from '../../components/EditorPanel';
import CharactersPanel from '../../components/CharactersPanel';
import PlotEventsPanel from '../../components/PlotEventsPanel';
import MetadataPanel from '../../components/MetadataPanel';
import {
  MessageSquare,
  FileText,
  Users,
  BookOpen,
  Settings,
  ArrowLeft,
  Save,
  Download
} from 'lucide-react';

type Tab = 'chat' | 'editor' | 'characters' | 'plot' | 'metadata';

export default function ProjectPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('chat');
  const [manuscript, setManuscript] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadProject();
    loadManuscript();
  }, [projectId]);

  const loadProject = async () => {
    try {
      setLoading(true);
      const data = await api.getProject(projectId);
      setProject(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load project');
    } finally {
      setLoading(false);
    }
  };

  const loadManuscript = async () => {
    try {
      const content = await api.getManuscript(projectId);
      setManuscript(content);
    } catch (err: any) {
      console.error('Failed to load manuscript:', err);
    }
  };

  const handleSaveManuscript = async () => {
    try {
      setSaving(true);
      await api.updateManuscript(projectId, manuscript);
      await loadProject(); // Refresh to update word count
    } catch (err: any) {
      alert(err.message || 'Failed to save manuscript');
    } finally {
      setSaving(false);
    }
  };

  const handleExport = async (format: 'docx' | 'pdf' | 'markdown') => {
    try {
      const filePath = await api.exportProject(projectId, format);
      alert(`Exported to: ${filePath}`);
    } catch (err: any) {
      alert(err.message || 'Failed to export project');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading project...</p>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Project not found'}</p>
          <button
            onClick={() => router.push('/')}
            className="text-blue-600 hover:underline"
          >
            Back to Projects
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => router.push('/')}
                className="text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft size={24} />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
                <p className="text-sm text-gray-600">
                  {project.metadata.wordCount.toLocaleString()} words •
                  {project.characters.length} characters •
                  {project.plotEvents.length} plot events
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleSaveManuscript}
                disabled={saving}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2 disabled:opacity-50"
              >
                <Save size={18} />
                {saving ? 'Saving...' : 'Save'}
              </button>
              <div className="relative group">
                <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition flex items-center gap-2">
                  <Download size={18} />
                  Export
                </button>
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border hidden group-hover:block z-10">
                  <button
                    onClick={() => handleExport('docx')}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-50 rounded-t-lg"
                  >
                    Export as DOCX
                  </button>
                  <button
                    onClick={() => handleExport('markdown')}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-50"
                  >
                    Export as Markdown
                  </button>
                  <button
                    onClick={() => handleExport('pdf')}
                    className="block w-full text-left px-4 py-2 hover:bg-gray-50 rounded-b-lg"
                  >
                    Export as PDF
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex gap-2 mt-4 border-t pt-4">
            <TabButton
              active={activeTab === 'chat'}
              onClick={() => setActiveTab('chat')}
              icon={<MessageSquare size={18} />}
              label="Chat with AI"
            />
            <TabButton
              active={activeTab === 'editor'}
              onClick={() => setActiveTab('editor')}
              icon={<FileText size={18} />}
              label="Manuscript"
            />
            <TabButton
              active={activeTab === 'characters'}
              onClick={() => setActiveTab('characters')}
              icon={<Users size={18} />}
              label="Characters"
              badge={project.characters.length}
            />
            <TabButton
              active={activeTab === 'plot'}
              onClick={() => setActiveTab('plot')}
              icon={<BookOpen size={18} />}
              label="Plot Events"
              badge={project.plotEvents.length}
            />
            <TabButton
              active={activeTab === 'metadata'}
              onClick={() => setActiveTab('metadata')}
              icon={<Settings size={18} />}
              label="Metadata"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {activeTab === 'chat' && <ChatPanel projectId={projectId} />}
        {activeTab === 'editor' && (
          <EditorPanel
            manuscript={manuscript}
            onChange={setManuscript}
            onSave={handleSaveManuscript}
            saving={saving}
          />
        )}
        {activeTab === 'characters' && (
          <CharactersPanel characters={project.characters} />
        )}
        {activeTab === 'plot' && (
          <PlotEventsPanel plotEvents={project.plotEvents} />
        )}
        {activeTab === 'metadata' && (
          <MetadataPanel
            projectId={projectId}
            metadata={project.metadata}
            onUpdate={loadProject}
          />
        )}
      </main>
    </div>
  );
}

function TabButton({
  active,
  onClick,
  icon,
  label,
  badge,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
  badge?: number;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${
        active
          ? 'bg-blue-600 text-white'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
    >
      {icon}
      {label}
      {badge !== undefined && (
        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
          active ? 'bg-blue-500' : 'bg-gray-300'
        }`}>
          {badge}
        </span>
      )}
    </button>
  );
}
