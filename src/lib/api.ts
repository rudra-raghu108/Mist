// API Configuration for SRM Guide Bot
const DEFAULT_API_BASE_URL = 'http://localhost:8000';

export const API_BASE_URL =
  import.meta.env?.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL;

export const api = {
  // Health check
  health: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  },

  // Chat endpoints
  chat: {
    send: async (message: string, user_id: string = "anonymous") => {
      try {
        console.log('API: Making request to:', `${API_BASE_URL}/api/chat`);
        console.log('API: Request body:', { message, user_id });
        
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message, user_id }),
        });
        
        console.log('API: Response status:', response.status);
        console.log('API: Response headers:', response.headers);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('API: Response data:', data);
        return data;
      } catch (error) {
        console.error('API: Request failed:', error);
        throw error;
      }
    },

    // Get chat history
    getHistory: async (user_id: string = "anonymous", limit: number = 50) => {
      const response = await fetch(`${API_BASE_URL}/api/chat/history?user_id=${user_id}&limit=${limit}`);
      return response.json();
    },
  },

  // AI Training endpoint
  aiTraining: {
    train: async (training_data: any) => {
      const response = await fetch(`${API_BASE_URL}/api/ai-training`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(training_data),
      });
      return response.json();
    },

    // Enhance AI knowledge with scraped data
    enhance: async () => {
      const response = await fetch(`${API_BASE_URL}/api/ai/enhance`, {
        method: 'POST',
      });
      return response.json();
    },
  },

  // Analytics endpoint
  analytics: async () => {
    const response = await fetch(`${API_BASE_URL}/api/analytics`);
    return response.json();
  },

  // User management
  users: {
    create: async (user_data: any) => {
      const response = await fetch(`${API_BASE_URL}/api/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(user_data),
      });
      return response.json();
    },
  },

  // Root endpoint
  root: async () => {
    const response = await fetch(`${API_BASE_URL}/`);
    return response.json();
  },

  // Web Scraping endpoints
  scraping: {
    // Start scraping all sources
    start: async () => {
      const response = await fetch(`${API_BASE_URL}/api/scraping/start`, {
        method: 'POST',
      });
      return response.json();
    },

    // Get scraping status
    status: async () => {
      const response = await fetch(`${API_BASE_URL}/api/scraping/status`);
      return response.json();
    },

    // Get data from specific source
    getData: async (sourceId: string) => {
      const response = await fetch(`${API_BASE_URL}/api/scraping/data/${sourceId}`);
      return response.json();
    },

    // Scrape specific source
    scrapeSource: async (sourceId: string) => {
      const response = await fetch(`${API_BASE_URL}/api/scraping/source/${sourceId}`, {
        method: 'POST',
      });
      return response.json();
    },
  },
};
