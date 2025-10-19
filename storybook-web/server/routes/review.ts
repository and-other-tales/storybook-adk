/**
 * Review Routes - REST API for automated reviews
 */

import express from 'express';
import { ApiResponse } from '../types';

export const reviewRoutes = express.Router();

/**
 * POST /api/review/start - Start automated review
 * Note: Realtime review progress is handled via Socket.IO
 */
reviewRoutes.post('/start', async (req, res) => {
  try {
    const { projectId, focusAreas } = req.body;

    if (!projectId) {
      return res.status(400).json({
        success: false,
        error: 'Project ID is required'
      });
    }

    const response: ApiResponse = {
      success: true,
      message: 'Connect to Socket.IO for realtime review',
      data: {
        projectId,
        focusAreas: focusAreas || [],
        socketEvent: 'review:start'
      }
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to start review'
    });
  }
});

/**
 * GET /api/review/:projectId/latest - Get latest review
 */
reviewRoutes.get('/:projectId/latest', async (req, res) => {
  try {
    // TODO: Implement review history storage
    const response: ApiResponse = {
      success: true,
      data: null,
      message: 'Review history not yet implemented'
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to get review'
    });
  }
});
