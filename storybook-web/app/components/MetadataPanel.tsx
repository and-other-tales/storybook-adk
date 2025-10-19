'use client';

import { useState } from 'react';
import { ManuscriptMetadata } from '../lib/types';
import { api } from '../lib/api';
import { Save, Edit2 } from 'lucide-react';

interface MetadataPanelProps {
  projectId: string;
  metadata: ManuscriptMetadata;
  onUpdate: () => void;
}

export default function MetadataPanel({ projectId, metadata, onUpdate }: MetadataPanelProps) {
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    title: metadata.title,
    author: metadata.author,
    genre: metadata.genre,
    notes: metadata.notes,
  });

  const handleSave = async () => {
    try {
      setSaving(true);
      await api.updateMetadata(projectId, formData);
      await onUpdate();
      setEditing(false);
    } catch (err: any) {
      alert(err.message || 'Failed to update metadata');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      title: metadata.title,
      author: metadata.author,
      genre: metadata.genre,
      notes: metadata.notes,
    });
    setEditing(false);
  };

  return (
    <div className="h-full bg-white overflow-y-auto p-6">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Manuscript Metadata</h2>
          {!editing && (
            <button
              onClick={() => setEditing(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
            >
              <Edit2 size={18} />
              Edit
            </button>
          )}
        </div>

        <div className="space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title
            </label>
            {editing ? (
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter manuscript title"
              />
            ) : (
              <p className="text-gray-900">{metadata.title || 'Not set'}</p>
            )}
          </div>

          {/* Author */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Author
            </label>
            {editing ? (
              <input
                type="text"
                value={formData.author}
                onChange={(e) => setFormData({ ...formData, author: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter author name"
              />
            ) : (
              <p className="text-gray-900">{metadata.author || 'Not set'}</p>
            )}
          </div>

          {/* Genre */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Genre
            </label>
            {editing ? (
              <input
                type="text"
                value={formData.genre}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Fantasy, Mystery, Romance"
              />
            ) : (
              <p className="text-gray-900">{metadata.genre || 'Not set'}</p>
            )}
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notes
            </label>
            {editing ? (
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder="Additional notes about your manuscript"
              />
            ) : (
              <p className="text-gray-900 whitespace-pre-wrap">{metadata.notes || 'No notes'}</p>
            )}
          </div>

          {/* Stats (Read-only) */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Statistics</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-700">Word Count</p>
                <p className="text-2xl font-bold text-gray-900">{metadata.wordCount.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Chapters</p>
                <p className="text-2xl font-bold text-gray-900">{metadata.chapterCount}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Created</p>
                <p className="text-gray-900">{new Date(metadata.createdAt).toLocaleDateString()}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Last Edited</p>
                <p className="text-gray-900">{new Date(metadata.lastEdited).toLocaleDateString()}</p>
              </div>
            </div>
          </div>

          {/* Save/Cancel Buttons */}
          {editing && (
            <div className="flex gap-3 pt-4">
              <button
                onClick={handleSave}
                disabled={saving}
                className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <Save size={18} />
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                onClick={handleCancel}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
