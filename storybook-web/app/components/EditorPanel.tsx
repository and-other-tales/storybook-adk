'use client';

import { FileText } from 'lucide-react';

interface EditorPanelProps {
  manuscript: string;
  onChange: (content: string) => void;
  onSave: () => void;
  saving: boolean;
}

export default function EditorPanel({ manuscript, onChange, onSave, saving }: EditorPanelProps) {
  const wordCount = manuscript.split(/\s+/).filter(word => word.length > 0).length;
  const charCount = manuscript.length;

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Editor Stats */}
      <div className="px-6 py-3 border-b bg-gray-50 flex items-center justify-between">
        <div className="flex items-center gap-6 text-sm text-gray-600">
          <span>{wordCount.toLocaleString()} words</span>
          <span>{charCount.toLocaleString()} characters</span>
        </div>
        <button
          onClick={onSave}
          disabled={saving}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium disabled:opacity-50"
        >
          {saving ? 'Saving...' : 'Save changes'}
        </button>
      </div>

      {/* Editor */}
      <div className="flex-1 p-6 overflow-y-auto">
        {manuscript.length === 0 ? (
          <div className="text-center py-12">
            <FileText size={48} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Empty Manuscript</h3>
            <p className="text-gray-600">Start writing your story here</p>
          </div>
        ) : (
          <textarea
            value={manuscript}
            onChange={(e) => onChange(e.target.value)}
            className="w-full h-full min-h-[600px] px-4 py-3 font-mono text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Write your manuscript here..."
            spellCheck={true}
          />
        )}
      </div>
    </div>
  );
}
