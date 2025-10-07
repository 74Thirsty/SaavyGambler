import type { Game, Player, Team, FantasyPlayer, Prediction, ApiResponse } from '../types';

// Base API configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.example.com';

// Generic fetch wrapper
async function fetchAPI<T>(endpoint: string): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    const data = await response.json();
    return { data, success: true };
  } catch (error) {
    console.error('API fetch error:', error);
    return {
      data: {} as T,
      success: false,
      message: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

// Sports API Service
export const sportsAPI = {
  // Get games for a specific sport
  getGames: async (sport: string): Promise<ApiResponse<Game[]>> => {
    // TODO: Replace with actual API endpoint
    return fetchAPI<Game[]>(`/games/${sport}`);
  },

  // Get team statistics
  getTeamStats: async (sport: string, teamId: string): Promise<ApiResponse<Team>> => {
    // TODO: Replace with actual API endpoint
    return fetchAPI<Team>(`/teams/${sport}/${teamId}`);
  },

  // Get player statistics
  getPlayerStats: async (sport: string, playerId: string): Promise<ApiResponse<Player>> => {
    // TODO: Replace with actual API endpoint
    return fetchAPI<Player>(`/players/${sport}/${playerId}`);
  },

  // Get fantasy projections
  getFantasyProjections: async (sport: string): Promise<ApiResponse<FantasyPlayer[]>> => {
    // TODO: Replace with actual API endpoint
    return fetchAPI<FantasyPlayer[]>(`/fantasy/${sport}/projections`);
  },

  // Get game predictions
  getPredictions: async (sport: string, gameId: string): Promise<ApiResponse<Prediction>> => {
    // TODO: Replace with actual API endpoint
    return fetchAPI<Prediction>(`/predictions/${sport}/${gameId}`);
  },

  // Get point spreads
  getSpreads: async (sport: string): Promise<ApiResponse<Game[]>> => {
    // TODO: Replace with actual API endpoint
    return fetchAPI<Game[]>(`/spreads/${sport}`);
  }
};

// Example API endpoints to integrate:
// - ESPN API: https://site.web.api.espn.com/apis/site/v2/sports/
// - The Odds API: https://the-odds-api.com/
// - SportsData.io: https://sportsdata.io/
// - SportRadar: https://developer.sportradar.com/
