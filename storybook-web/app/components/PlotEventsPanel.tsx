'use client';

import { PlotEvent } from '../lib/types';
import { BookOpen, Calendar } from 'lucide-react';

interface PlotEventsPanelProps {
  plotEvents: PlotEvent[];
}

const importanceColors = {
  low: 'bg-gray-100 text-gray-700',
  medium: 'bg-blue-100 text-blue-700',
  high: 'bg-orange-100 text-orange-700',
  critical: 'bg-red-100 text-red-700',
};

export default function PlotEventsPanel({ plotEvents }: PlotEventsPanelProps) {
  const sortedEvents = [...plotEvents].sort((a, b) => {
    const importanceOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    return importanceOrder[a.importance] - importanceOrder[b.importance];
  });

  return (
    <div className="h-full bg-white overflow-y-auto p-6">
      {plotEvents.length === 0 ? (
        <div className="text-center py-12">
          <BookOpen size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Plot Events Yet</h3>
          <p className="text-gray-600">
            Plot events will be tracked here as the AI analyzes your manuscript
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Plot Events ({plotEvents.length})
          </h2>
          <div className="space-y-4">
            {sortedEvents.map((event) => (
              <div
                key={event.id}
                className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{event.title}</h3>
                    <p className="text-sm text-gray-600">{event.description}</p>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      importanceColors[event.importance]
                    }`}
                  >
                    {event.importance}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  {event.chapterReference && (
                    <div>
                      <p className="font-medium text-gray-700 mb-1 flex items-center gap-1">
                        <Calendar size={14} />
                        Chapter
                      </p>
                      <p className="text-gray-600">{event.chapterReference}</p>
                    </div>
                  )}

                  {event.charactersInvolved.length > 0 && (
                    <div>
                      <p className="font-medium text-gray-700 mb-1">Characters Involved</p>
                      <p className="text-gray-600">{event.charactersInvolved.join(', ')}</p>
                    </div>
                  )}
                </div>

                {event.notes && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-sm font-medium text-gray-700 mb-1">Notes</p>
                    <p className="text-sm text-gray-600">{event.notes}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
