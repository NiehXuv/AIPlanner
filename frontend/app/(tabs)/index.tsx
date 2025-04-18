import React, { useState, useEffect } from 'react';
import { View, FlatList, TouchableOpacity, Text } from 'react-native';
import { router } from 'expo-router';
import tw from 'twrnc';
import TripCard from '../../components/TripCard';

export default function TripsScreen() {
  const [trips, setTrips] = useState<any[]>([]);

  useEffect(() => {
    // Mocked trips data (replace with API call to fetch plans)
    const mockTrips = [
      {
        plan_id: '1',
        location: 'Abu Dhabi, United Arab Emirates',
        start_date: '2025-04-08',
        days: 3,
        travelType: 'Solo',
        image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1470&auto=format&fit=crop',
      },
      {
        plan_id: '2',
        location: 'Hanoi, Vietnam',
        start_date: '2025-04-07',
        days: 2,
        travelType: 'With spouse',
        image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1470&auto=format&fit=crop',
      },
    ];
    setTrips(mockTrips);
  }, []);

  return (
    <View style={tw`flex-1 bg-gray-100`}>
      <View style={tw`flex-row justify-between items-center p-4`}>
        <Text style={tw`text-2xl font-bold`}>Trips</Text>
        <TouchableOpacity
          style={tw`bg-blue-500 w-10 h-10 rounded-full flex items-center justify-center`}
          onPress={() => router.push('./create-trip')}
        >
          <Text style={tw`text-white text-xl`}>+</Text>
        </TouchableOpacity>
      </View>
      <FlatList
        data={trips}
        keyExtractor={(item) => item.plan_id}
        renderItem={({ item }) => (
          <TripCard
            trip={item}
            onPress={(planId: string) => router.push(`./view-plan/${planId}`)}
          />
        )}
        contentContainerStyle={tw`pb-20`}
      />
    </View>
  );
}