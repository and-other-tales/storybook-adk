export interface Character {
  name: string;
  aliases: string[];
  description: string;
  traits: string[];
  firstAppearance: string;
  notes: string;
}

export interface PlotEvent {
  id: string;
  title: string;
  description: string;
  chapterReference: string;
  charactersInvolved: string[];
  importance: 'low' | 'medium' | 'high' | 'critical';
  notes: string;
}

export interface ManuscriptMetadata {
  title: string;
  author: string;
  genre: string;
  wordCount: number;
  chapterCount: number;
  createdAt: string;
  lastEdited: string;
  notes: string;
}

export interface Project {
  id: string;
  name: string;
  createdAt: string;
  lastEdited: string;
  metadata: ManuscriptMetadata;
  characters: Character[];
  plotEvents: PlotEvent[];
  manuscriptFile: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  thinking?: string;
  toolUses?: ToolUse[];
}

export interface ToolUse {
  id: string;
  name: string;
  input: Record<string, any>;
}

export interface ReviewSuggestion {
  type: string;
  severity: 'info' | 'minor' | 'major' | 'critical';
  location: string;
  issue: string;
  suggestion: string;
  example?: string;
}

export interface EditorReview {
  timestamp: string;
  overallAssessment: string;
  strengths: string[];
  weaknesses: string[];
  suggestions: ReviewSuggestion[];
  characterNotes: Record<string, string>;
  plotNotes: string[];
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface SocketEvents {
  // Client to Server
  'chat:send': (data: { projectId: string; message: string }) => void;
  'review:start': (data: { projectId: string; focusAreas?: string[] }) => void;
  'project:subscribe': (projectId: string) => void;
  'project:unsubscribe': (projectId: string) => void;

  // Server to Client
  'chat:message': (message: ChatMessage) => void;
  'chat:thinking': (data: { content: string }) => void;
  'chat:tool': (data: { tool: string; input: any }) => void;
  'chat:complete': (data: { cost?: number; turns?: number }) => void;
  'review:progress': (data: { message: string; type: string }) => void;
  'review:complete': (review: EditorReview) => void;
  'project:updated': (project: Project) => void;
  'error': (error: { message: string; code?: string }) => void;
}
