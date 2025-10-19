/**
 * Chat Routes - REST API for chat sessions (non-realtime)
 */

import express from 'express';
import { ApiResponse } from '../types';

export const chatRoutes = express.Router();

/**
 * POST /api/chat/sessions - Create a chat session
 * Note: Realtime chat is handled via Socket.IO
 */
chatRoutes.post('/sessions', async (req, res) => {
  try {
    const { projectId } = req.body;

    if (!projectId) {
      return res.status(400).json({
        success: false,
        error: 'Project ID is required'
      });
    }

    const response: ApiResponse = {
      success: true,
      message: 'Connect to Socket.IO for realtime chat',
      data: {
        projectId,
        socketEvent: 'chat:send'
      }
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to create chat session'
    });
  }
});

/**
 * GET /api/chat/sessions/:sessionId/history - Get chat history
 */
chatRoutes.get('/sessions/:sessionId/history', async (req, res) => {
  try {
    // TODO: Implement chat history storage
    const response: ApiResponse = {
      success: true,
      data: [],
      message: 'Chat history not yet implemented'
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to get chat history'
    });
  }
});
