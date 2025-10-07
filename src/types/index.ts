// Sports Types
export interface Sport {
  id: string;
  name: string;
  icon: string;
  description: string;
}

// Player Types
export interface Player {
  id: string;
  name: string;
  team: string;
  position: string;
  stats?: Record<string, number>;
}

// Team Types
export interface Team {
  id: string;
  name: string;
  abbreviation: string;
  wins: number;
  losses: number;
}

// Game Types
export interface Game {
  id: string;
  homeTeam: Team;
  awayTeam: Team;
  date: string;
  status: 'scheduled' | 'live' | 'completed';
  homeScore?: number;
  awayScore?: number;
  spread?: number;
}

// Fantasy Types
export interface FantasyPlayer extends Player {
  projectedPoints: number;
  averagePoints: number;
  injuryStatus?: string;
}

// Prediction Types
export interface Prediction {
  gameId: string;
  predictedWinner: string;
  confidence: number;
  spread: number;
  total: number;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}
