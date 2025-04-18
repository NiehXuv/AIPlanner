// API configuration and endpoints

// Base URL for the backend API
export const API_BASE_URL = 'http://localhost:8000';

// API endpoints
export const ENDPOINTS = {
  // Plan endpoints
  GENERATE_PLAN: '/generate-plan',
  GET_PLAN: '/get-plan',
  EDIT_PLAN: '/edit-plan',
  
  // Hotel endpoints
  SEARCH_HOTELS: '/hotels/search',
  
  // Health check
  HEALTH: '/health'
};

// API request timeout in milliseconds
export const REQUEST_TIMEOUT = 30000;
