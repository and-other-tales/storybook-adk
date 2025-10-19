'use client';

import { Character } from '../lib/types';
import { Users, User } from 'lucide-react';

interface CharactersPanelProps {
  characters: Character[];
}

export default function CharactersPanel({ characters }: CharactersPanelProps) {
  return (
    <div className="h-full bg-white overflow-y-auto p-6">
      {characters.length === 0 ? (
        <div className="text-center py-12">
          <Users size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Characters Yet</h3>
          <p className="text-gray-600">
            Characters will appear here as they are mentioned in your manuscript and tracked by the AI
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Characters ({characters.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {characters.map((character, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition"
              >
                <div className="flex items-start gap-3 mb-3">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <User size={20} className="text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">{character.name}</h3>
                    {character.aliases.length > 0 && (
                      <p className="text-sm text-gray-500">
                        Also known as: {character.aliases.join(', ')}
                      </p>
                    )}
                  </div>
                </div>

                {character.description && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">Description</p>
                    <p className="text-sm text-gray-600">{character.description}</p>
                  </div>
                )}

                {character.traits.length > 0 && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">Traits</p>
                    <div className="flex flex-wrap gap-2">
                      {character.traits.map((trait, i) => (
                        <span
                          key={i}
                          className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full"
                        >
                          {trait}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {character.firstAppearance && (
                  <div className="mb-3">
                    <p className="text-sm font-medium text-gray-700 mb-1">First Appearance</p>
                    <p className="text-sm text-gray-600">{character.firstAppearance}</p>
                  </div>
                )}

                {character.notes && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-1">Notes</p>
                    <p className="text-sm text-gray-600">{character.notes}</p>
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
