/**
 * Socket.IO Handler - Real-time communication for chat and review
 */

import { Server as SocketIOServer, Socket } from 'socket.io';
import { pythonBridge } from './python-bridge';
import { ChatMessage, EditorReview } from '../types';

interface SocketData {
  projectId?: string;
  chatSessionId?: string;
  reviewSessionId?: string;
}

export function setupSocketHandlers(io: SocketIOServer) {
  io.on('connection', (socket: Socket) => {
    console.log(`🔌 Client connected: ${socket.id}`);
    const socketData: SocketData = {};

    /**
     * Subscribe to project updates
     */
    socket.on('project:subscribe', (projectId: string) => {
      socketData.projectId = projectId;
      socket.join(`project:${projectId}`);
      console.log(`📂 Client ${socket.id} subscribed to project ${projectId}`);
    });

    /**
     * Unsubscribe from project updates
     */
    socket.on('project:unsubscribe', (projectId: string) => {
      socket.leave(`project:${projectId}`);
      console.log(`📂 Client ${socket.id} unsubscribed from project ${projectId}`);
    });

    /**
     * Start a chat session and send a message
     */
    socket.on('chat:send', async (data: { projectId: string; message: string }) => {
      try {
        const { projectId, message } = data;

        if (!message || !projectId) {
          socket.emit('error', {
            message: 'Project ID and message are required',
            code: 'INVALID_INPUT'
          });
          return;
        }

        console.log(`💬 Chat message from ${socket.id} for project ${projectId}`);

        // If no active session, create one
        if (!socketData.chatSessionId) {
          socketData.chatSessionId = pythonBridge.createChatSession(
            projectId,
            (event) => {
              // Handle different event types
              switch (event.type) {
                case 'message':
                  const chatMessage: ChatMessage = {
                    id: `msg_${Date.now()}`,
                    role: event.role,
                    content: event.content,
                    timestamp: event.timestamp || new Date().toISOString()
                  };
                  socket.emit('chat:message', chatMessage);
                  break;

                case 'thinking':
                  socket.emit('chat:thinking', {
                    content: event.content
                  });
                  break;

                case 'tool':
                  socket.emit('chat:tool', {
                    tool: event.name,
                    input: event.input
                  });
                  break;

                case 'complete':
                  socket.emit('chat:complete', {
                    turns: event.turns,
                    cost: event.cost
                  });
                  break;

                case 'error':
                  socket.emit('error', {
                    message: event.message,
                    code: 'CHAT_ERROR'
                  });
                  break;
              }
            },
            () => {
              // Session completed
              console.log(`💬 Chat session ${socketData.chatSessionId} completed`);
              socketData.chatSessionId = undefined;
            }
          );

          console.log(`💬 Created chat session ${socketData.chatSessionId}`);
        }

        // Send the message to the chat session
        await pythonBridge.sendChatMessage(socketData.chatSessionId, message);

        // Echo user message back
        const userMessage: ChatMessage = {
          id: `msg_${Date.now()}`,
          role: 'user',
          content: message,
          timestamp: new Date().toISOString()
        };
        socket.emit('chat:message', userMessage);

      } catch (error: any) {
        console.error('Chat error:', error);
        socket.emit('error', {
          message: error.message || 'Failed to send chat message',
          code: 'CHAT_ERROR'
        });
      }
    });

    /**
     * Start an automated review
     */
    socket.on('review:start', async (data: { projectId: string; focusAreas?: string[] }) => {
      try {
        const { projectId, focusAreas } = data;

        if (!projectId) {
          socket.emit('error', {
            message: 'Project ID is required',
            code: 'INVALID_INPUT'
          });
          return;
        }

        console.log(`📝 Starting review for project ${projectId}`);

        // Create review session
        socketData.reviewSessionId = pythonBridge.createReviewSession(
          projectId,
          focusAreas,
          (event) => {
            // Progress event
            socket.emit('review:progress', {
              message: event.message,
              detail: event.detail,
              type: 'info'
            });
          },
          (review: EditorReview) => {
            // Review complete
            socket.emit('review:complete', review);
            console.log(`📝 Review ${socketData.reviewSessionId} completed`);
            socketData.reviewSessionId = undefined;

            // Notify project room of update
            io.to(`project:${projectId}`).emit('project:updated', {
              projectId,
              type: 'review_complete'
            });
          }
        );

        console.log(`📝 Created review session ${socketData.reviewSessionId}`);

      } catch (error: any) {
        console.error('Review error:', error);
        socket.emit('error', {
          message: error.message || 'Failed to start review',
          code: 'REVIEW_ERROR'
        });
      }
    });

    /**
     * Handle disconnection
     */
    socket.on('disconnect', () => {
      console.log(`🔌 Client disconnected: ${socket.id}`);

      // Cleanup active sessions
      if (socketData.chatSessionId) {
        pythonBridge.closeChatSession(socketData.chatSessionId);
        socketData.chatSessionId = undefined;
      }
    });

    /**
     * Handle errors
     */
    socket.on('error', (error) => {
      console.error(`Socket error from ${socket.id}:`, error);
    });
  });

  // Global error handler
  io.engine.on('connection_error', (err) => {
    console.error('Connection error:', err);
  });

  return io;
}
