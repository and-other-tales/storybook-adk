/**
 * Projects Routes - REST API for project management
 */

import express from 'express';
import { pythonBridge } from '../services/python-bridge';
import { ApiResponse, Project, ManuscriptMetadata } from '../types';

export const projectRoutes = express.Router();

/**
 * GET /api/projects - List all projects
 */
projectRoutes.get('/', async (req, res) => {
  try {
    const projects = await pythonBridge.listProjects();
    const response: ApiResponse<Project[]> = {
      success: true,
      data: projects
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to list projects'
    });
  }
});

/**
 * GET /api/projects/:id - Get a single project
 */
projectRoutes.get('/:id', async (req, res) => {
  try {
    const project = await pythonBridge.getProject(req.params.id);
    const response: ApiResponse<Project> = {
      success: true,
      data: project
    };
    res.json(response);
  } catch (error: any) {
    res.status(404).json({
      success: false,
      error: error.message || 'Project not found'
    });
  }
});

/**
 * POST /api/projects - Create a new project
 */
projectRoutes.post('/', async (req, res) => {
  try {
    const { name, importFile } = req.body;

    if (!name) {
      return res.status(400).json({
        success: false,
        error: 'Project name is required'
      });
    }

    const project = await pythonBridge.createProject(name, importFile);
    const response: ApiResponse<Project> = {
      success: true,
      data: project,
      message: 'Project created successfully'
    };
    res.status(201).json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to create project'
    });
  }
});

/**
 * PUT /api/projects/:id/metadata - Update project metadata
 */
projectRoutes.put('/:id/metadata', async (req, res) => {
  try {
    const metadata: Partial<ManuscriptMetadata> = req.body;
    const project = await pythonBridge.updateMetadata(req.params.id, metadata);

    const response: ApiResponse<Project> = {
      success: true,
      data: project,
      message: 'Metadata updated successfully'
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to update metadata'
    });
  }
});

/**
 * DELETE /api/projects/:id - Delete a project
 */
projectRoutes.delete('/:id', async (req, res) => {
  try {
    await pythonBridge.deleteProject(req.params.id);
    const response: ApiResponse = {
      success: true,
      message: 'Project deleted successfully'
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to delete project'
    });
  }
});

/**
 * GET /api/projects/:id/manuscript - Get manuscript content
 */
projectRoutes.get('/:id/manuscript', async (req, res) => {
  try {
    const content = await pythonBridge.readManuscript(req.params.id);
    const response: ApiResponse<string> = {
      success: true,
      data: content
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to read manuscript'
    });
  }
});

/**
 * PUT /api/projects/:id/manuscript - Update manuscript content
 */
projectRoutes.put('/:id/manuscript', async (req, res) => {
  try {
    const { content } = req.body;

    if (typeof content !== 'string') {
      return res.status(400).json({
        success: false,
        error: 'Manuscript content must be a string'
      });
    }

    await pythonBridge.writeManuscript(req.params.id, content);

    const response: ApiResponse = {
      success: true,
      message: 'Manuscript updated successfully'
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to update manuscript'
    });
  }
});

/**
 * GET /api/projects/:id/characters - Get all characters
 */
projectRoutes.get('/:id/characters', async (req, res) => {
  try {
    const characters = await pythonBridge.getCharacters(req.params.id);
    const response: ApiResponse = {
      success: true,
      data: characters
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to get characters'
    });
  }
});

/**
 * GET /api/projects/:id/plot-events - Get all plot events
 */
projectRoutes.get('/:id/plot-events', async (req, res) => {
  try {
    const plotEvents = await pythonBridge.getPlotEvents(req.params.id);
    const response: ApiResponse = {
      success: true,
      data: plotEvents
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to get plot events'
    });
  }
});

/**
 * POST /api/projects/:id/export - Export project
 */
projectRoutes.post('/:id/export', async (req, res) => {
  try {
    const { format } = req.body;

    if (!['docx', 'pdf', 'markdown'].includes(format)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid export format. Must be docx, pdf, or markdown'
      });
    }

    const filePath = await pythonBridge.exportProject(req.params.id, format);

    const response: ApiResponse<string> = {
      success: true,
      data: filePath,
      message: `Project exported as ${format}`
    };
    res.json(response);
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to export project'
    });
  }
});
