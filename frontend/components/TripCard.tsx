import React from 'react';
import { View, Text, ImageBackground, TouchableOpacity } from 'react-native';
import tw from 'twrnc';

interface TripCardProps {
  trip: {
    plan_id: string;
    location: string;
    start_date: string;
    days: number;
    travelType: string;
    image: string;
  };
  onPress: (planId: string) => void;
}

const TripCard: React.FC<TripCardProps> = ({ trip, onPress }) => {
  const startDate = new Date(trip.start_date);
  const endDate = new Date(startDate);
  endDate.setDate(startDate.getDate() + trip.days - 1);

  const formatDateRange = () => {
    const start = startDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    const end = endDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    return `${start} - ${end}`;
  };

  return (
    <TouchableOpacity onPress={() => onPress(trip.plan_id)}>
      <ImageBackground
        source={{ uri: trip.image }}
        style={tw`w-full h-40 rounded-lg overflow-hidden`}
        imageStyle={tw`opacity-80`}
      >
        <View style={tw`p-4 flex-1 justify-between`}>
          <Text style={tw`text-white text-sm`}>{formatDateRange()}</Text>
          <Text style={tw`text-white text-xl font-bold`}>{trip.location}</Text>
        </View>
      </ImageBackground>
      <View style={tw`flex-row justify-between items-center p-4 bg-white rounded-b-lg shadow`}>
        <View style={tw`flex-row items-center`}>
          <View style={tw`flex-row mr-2`}>
            <View style={tw`w-6 h-6 bg-gray-300 rounded-full`} />
            <View style={tw`w-6 h-6 bg-gray-300 rounded-full -ml-2`} />
          </View>
          <View>
            <Text style={tw`text-gray-800 font-semibold`}>{trip.location}</Text>
            <Text style={tw`text-gray-600 text-sm`}>
              {startDate.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })}
            </Text>
            <Text style={tw`text-gray-500 text-xs`}>{trip.travelType.toLowerCase()}</Text>
          </View>
        </View>
        <TouchableOpacity
          style={tw`bg-blue-500 px-4 py-2 rounded-full`}
          onPress={() => onPress(trip.plan_id)}
        >
          <Text style={tw`text-white font-semibold`}>See Your Plan</Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );
};

export default TripCard;