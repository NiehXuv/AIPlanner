import axios from 'axios';
import { useState } from 'react';
import Constants from 'expo-constants';

const BASE_URL = Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8000';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generatePlan = async (planData: {
    location: string;
    start_date: string;
    days: number;
    interests: { [key: string]: number };
    budget: number;
  }) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${BASE_URL}/generate-plan`, planData);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate plan');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getPlan = async (planId: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${BASE_URL}/get-plan?plan_id=${planId}`);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch plan');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const searchHotels = async (location: string, checkin: string, checkout: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(
        `${BASE_URL}/hotels/search?location=${location}&checkin=${checkin}&checkout=${checkout}`
      );
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to search hotels');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { generatePlan, getPlan, searchHotels, loading, error };
};