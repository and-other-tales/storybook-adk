'use client';

import { useEffect, useState, useRef } from 'react';
import { socketClient } from '../lib/socket';
import { ChatMessage, EditorReview } from '../lib/types';
import { Send, Loader2, Sparkles, Wrench, Brain } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function ChatPanel({ projectId }: { projectId: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [thinking, setThinking] = useState<string | null>(null);
  const [currentTool, setCurrentTool] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Connect to WebSocket
    const socket = socketClient.connect({
      onChatMessage: (message) => {
        setMessages((prev) => [...prev, message]);
        setIsSending(false);
        setThinking(null);
        setCurrentTool(null);
      },
      onChatThinking: (content) => {
        setThinking(content);
      },
      onChatTool: (tool, input) => {
        setCurrentTool(tool);
      },
      onChatComplete: (data) => {
        setIsSending(false);
        setThinking(null);
        setCurrentTool(null);
      },
      onError: (error) => {
        console.error('Chat error:', error);
        setIsSending(false);
      },
    });

    socket.on('connect', () => setIsConnected(true));
    socket.on('disconnect', () => setIsConnected(false));

    socketClient.subscribeToProject(projectId);

    return () => {
      socketClient.unsubscribeFromProject(projectId);
      socketClient.disconnect();
    };
  }, [projectId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, thinking]);

  const handleSend = () => {
    if (!input.trim() || isSending) return;

    setIsSending(true);
    socketClient.sendChatMessage(projectId, input);
    setInput('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Connection Status */}
      <div className={`px-4 py-2 text-sm ${isConnected ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
        {isConnected ? '✓ Connected to AI' : '⚠ Disconnected'}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <Sparkles size={48} className="mx-auto text-blue-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Chat with Your AI Editor
            </h3>
            <p className="text-gray-600">
              Ask questions, request edits, or get feedback on your manuscript
            </p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3xl rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              {message.role === 'assistant' ? (
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              ) : (
                <p className="whitespace-pre-wrap">{message.content}</p>
              )}
              {message.thinking && (
                <div className="mt-2 pt-2 border-t border-gray-300 text-sm opacity-70">
                  <div className="flex items-center gap-2 mb-1">
                    <Brain size={14} />
                    <span className="font-medium">Thinking:</span>
                  </div>
                  <p className="text-xs">{message.thinking}</p>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Thinking Indicator */}
        {thinking && (
          <div className="flex justify-start">
            <div className="max-w-3xl rounded-lg px-4 py-3 bg-blue-50 border border-blue-200">
              <div className="flex items-center gap-2 text-blue-700">
                <Brain size={16} className="animate-pulse" />
                <span className="text-sm font-medium">Thinking...</span>
              </div>
              <p className="text-sm text-blue-600 mt-1">{thinking}</p>
            </div>
          </div>
        )}

        {/* Tool Indicator */}
        {currentTool && (
          <div className="flex justify-start">
            <div className="max-w-3xl rounded-lg px-4 py-3 bg-purple-50 border border-purple-200">
              <div className="flex items-center gap-2 text-purple-700">
                <Wrench size={16} className="animate-pulse" />
                <span className="text-sm font-medium">Using tool: {currentTool}</span>
              </div>
            </div>
          </div>
        )}

        {/* Sending Indicator */}
        {isSending && !thinking && !currentTool && (
          <div className="flex justify-start">
            <div className="rounded-lg px-4 py-3 bg-gray-100">
              <Loader2 size={20} className="animate-spin text-gray-600" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t bg-gray-50 p-4">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about your manuscript, request edits, or get feedback..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={3}
            disabled={!isConnected || isSending}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || !isConnected || isSending}
            className="px-6 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isSending ? <Loader2 size={20} className="animate-spin" /> : <Send size={20} />}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Press Enter to send, Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}
