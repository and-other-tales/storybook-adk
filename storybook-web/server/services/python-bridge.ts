/**
 * Python Bridge Service
 *
 * Bridges Node.js/TypeScript backend with Python CLI application
 * Executes Python CLI commands and manages subprocess communication
 */

import { spawn, ChildProcess } from 'child_process';
import { EventEmitter } from 'events';
import path from 'path';
import { Project, Character, PlotEvent, ManuscriptMetadata } from '../types';

interface PythonCommand {
  module: string;
  function: string;
  args: any[];
}

interface PythonResponse {
  success: boolean;
  data?: any;
  error?: string;
}

export class PythonBridge extends EventEmitter {
  private pythonPath: string;
  private projectRoot: string;
  private activeSessions: Map<string, ChildProcess>;

  constructor() {
    super();
    this.projectRoot = path.join(__dirname, '../../../');
    this.pythonPath = path.join(this.projectRoot, '.venv/bin/python');
    this.activeSessions = new Map();
  }

  /**
   * Execute a Python function and return the result
   */
  async execute<T = any>(command: PythonCommand): Promise<T> {
    return new Promise((resolve, reject) => {
      const scriptPath = path.join(this.projectRoot, 'storybook-web/server/services/python_runner.py');

      const pythonProcess = spawn(this.pythonPath, [
        scriptPath,
        JSON.stringify(command)
      ]);

      let stdout = '';
      let stderr = '';

      pythonProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`Python process exited with code ${code}: ${stderr}`));
          return;
        }

        try {
          const response: PythonResponse = JSON.parse(stdout);
          if (response.success) {
            resolve(response.data as T);
          } else {
            reject(new Error(response.error || 'Unknown Python error'));
          }
        } catch (err) {
          reject(new Error(`Failed to parse Python response: ${stdout}`));
        }
      });

      pythonProcess.on('error', (err) => {
        reject(new Error(`Failed to start Python process: ${err.message}`));
      });
    });
  }

  /**
   * List all projects
   */
  async listProjects(): Promise<Project[]> {
    return this.execute<Project[]>({
      module: 'storybook.project_manager',
      function: 'list_projects',
      args: []
    });
  }

  /**
   * Get a single project by ID
   */
  async getProject(projectId: string): Promise<Project> {
    return this.execute<Project>({
      module: 'storybook.project_manager',
      function: 'load_project',
      args: [projectId]
    });
  }

  /**
   * Create a new project
   */
  async createProject(name: string, importFile?: string): Promise<Project> {
    return this.execute<Project>({
      module: 'storybook.project_manager',
      function: 'create_project',
      args: [name, importFile]
    });
  }

  /**
   * Delete a project
   */
  async deleteProject(projectId: string): Promise<void> {
    return this.execute<void>({
      module: 'storybook.project_manager',
      function: 'delete_project',
      args: [projectId]
    });
  }

  /**
   * Update project metadata
   */
  async updateMetadata(projectId: string, metadata: Partial<ManuscriptMetadata>): Promise<Project> {
    return this.execute<Project>({
      module: 'storybook.project_manager',
      function: 'update_metadata',
      args: [projectId, metadata]
    });
  }

  /**
   * Read manuscript content
   */
  async readManuscript(projectId: string): Promise<string> {
    return this.execute<string>({
      module: 'storybook.project_manager',
      function: 'read_manuscript',
      args: [projectId]
    });
  }

  /**
   * Write manuscript content
   */
  async writeManuscript(projectId: string, content: string): Promise<void> {
    return this.execute<void>({
      module: 'storybook.project_manager',
      function: 'write_manuscript',
      args: [projectId, content]
    });
  }

  /**
   * Get project characters
   */
  async getCharacters(projectId: string): Promise<Character[]> {
    const project = await this.getProject(projectId);
    return project.characters;
  }

  /**
   * Get project plot events
   */
  async getPlotEvents(projectId: string): Promise<PlotEvent[]> {
    const project = await this.getProject(projectId);
    return project.plotEvents;
  }

  /**
   * Export project to a specific format
   */
  async exportProject(projectId: string, format: 'docx' | 'pdf' | 'markdown'): Promise<string> {
    return this.execute<string>({
      module: 'storybook.project_manager',
      function: 'export_project',
      args: [projectId, format]
    });
  }

  /**
   * Import a document into a project
   */
  async importDocument(projectId: string, filePath: string): Promise<void> {
    return this.execute<void>({
      module: 'storybook.document_converter',
      function: 'import_to_project',
      args: [projectId, filePath]
    });
  }

  /**
   * Start a streaming chat session (returns session ID)
   */
  createChatSession(projectId: string, onMessage: (data: any) => void, onComplete: () => void): string {
    const sessionId = `chat_${projectId}_${Date.now()}`;
    const scriptPath = path.join(this.projectRoot, 'storybook-web/server/services/chat_bridge.py');

    const pythonProcess = spawn(this.pythonPath, [
      scriptPath,
      projectId
    ]);

    pythonProcess.stdout.on('data', (data) => {
      const lines = data.toString().split('\n').filter((line: string) => line.trim());
      lines.forEach((line: string) => {
        try {
          const event = JSON.parse(line);
          onMessage(event);
        } catch (err) {
          console.error('Failed to parse chat event:', line);
        }
      });
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Chat session error:', data.toString());
    });

    pythonProcess.on('close', () => {
      this.activeSessions.delete(sessionId);
      onComplete();
    });

    this.activeSessions.set(sessionId, pythonProcess);
    return sessionId;
  }

  /**
   * Send a message to an active chat session
   */
  async sendChatMessage(sessionId: string, message: string): Promise<void> {
    const session = this.activeSessions.get(sessionId);
    if (!session) {
      throw new Error(`Chat session ${sessionId} not found`);
    }

    return new Promise((resolve, reject) => {
      session.stdin.write(JSON.stringify({ type: 'message', content: message }) + '\n', (err) => {
        if (err) reject(err);
        else resolve();
      });
    });
  }

  /**
   * Close a chat session
   */
  closeChatSession(sessionId: string): void {
    const session = this.activeSessions.get(sessionId);
    if (session) {
      session.kill();
      this.activeSessions.delete(sessionId);
    }
  }

  /**
   * Start automated review (streaming)
   */
  createReviewSession(
    projectId: string,
    focusAreas: string[] | undefined,
    onProgress: (data: any) => void,
    onComplete: (review: any) => void
  ): string {
    const sessionId = `review_${projectId}_${Date.now()}`;
    const scriptPath = path.join(this.projectRoot, 'storybook-web/server/services/review_bridge.py');

    const pythonProcess = spawn(this.pythonPath, [
      scriptPath,
      projectId,
      JSON.stringify(focusAreas || [])
    ]);

    pythonProcess.stdout.on('data', (data) => {
      const lines = data.toString().split('\n').filter((line: string) => line.trim());
      lines.forEach((line: string) => {
        try {
          const event = JSON.parse(line);
          if (event.type === 'complete') {
            onComplete(event.data);
          } else {
            onProgress(event);
          }
        } catch (err) {
          console.error('Failed to parse review event:', line);
        }
      });
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Review session error:', data.toString());
    });

    pythonProcess.on('close', () => {
      this.activeSessions.delete(sessionId);
    });

    this.activeSessions.set(sessionId, pythonProcess);
    return sessionId;
  }

  /**
   * Cleanup all active sessions
   */
  cleanup(): void {
    this.activeSessions.forEach((session) => {
      session.kill();
    });
    this.activeSessions.clear();
  }
}

// Singleton instance
export const pythonBridge = new PythonBridge();
