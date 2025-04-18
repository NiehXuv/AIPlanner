import axios from 'axios';
import { API_BASE_URL, ENDPOINTS, REQUEST_TIMEOUT } from '@/constants/Api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service for plan-related operations
interface PlanData {
    [key: string]: any; // Replace with specific fields if known
}

interface PlanResponse {
    [key: string]: any; // Replace with specific fields if known
}

export const planService = {
    // Generate a new travel plan
    generatePlan: async (planData: PlanData): Promise<PlanResponse> => {
        try {
            const response = await apiClient.post<PlanResponse>(ENDPOINTS.GENERATE_PLAN, planData);
            return response.data;
        } catch (error) {
            console.error('Error generating plan:', error);
            throw error;
        }
    },

    // Get an existing plan by ID
    getPlan: async (planId: string): Promise<PlanResponse> => {
        try {
            const response = await apiClient.get<PlanResponse>(`${ENDPOINTS.GET_PLAN}?plan_id=${planId}`);
            return response.data;
        } catch (error) {
            console.error('Error getting plan:', error);
            throw error;
        }
    },

    // Edit an existing plan
    editPlan: async (planId: string, planData: PlanData): Promise<PlanResponse> => {
        try {
            const response = await apiClient.post<PlanResponse>(`${ENDPOINTS.EDIT_PLAN}?plan_id=${planId}`, planData);
            return response.data;
        } catch (error) {
            console.error('Error editing plan:', error);
            throw error;
        }
    }
};

// API service for hotel-related operations
interface HotelSearchParams {
    location: string;
    checkin: string;
    checkout: string;
}

interface HotelSearchResponse {
    [key: string]: any; // Replace with specific fields if known
}

export const hotelService = {
    // Search for hotels
    searchHotels: async (
        location: HotelSearchParams['location'],
        checkin: HotelSearchParams['checkin'],
        checkout: HotelSearchParams['checkout']
    ): Promise<HotelSearchResponse> => {
        try {
            const response = await apiClient.get<HotelSearchResponse>(
                `${ENDPOINTS.SEARCH_HOTELS}?location=${location}&checkin=${checkin}&checkout=${checkout}`
            );
            return response.data;
        } catch (error) {
            console.error('Error searching hotels:', error);
            throw error;
        }
    }
};

// Health check service
export const healthService = {
  checkHealth: async () => {
    try {
      const response = await apiClient.get(ENDPOINTS.HEALTH);
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
};

export default {
  planService,
  hotelService,
  healthService
};
