import React from 'react';
import { View, Text } from 'react-native';
import tw from 'twrnc';

interface HotelCardProps {
  hotel: {
    name: string;
    price: string;
    rating: string;
  };
}

const HotelCard: React.FC<HotelCardProps> = ({ hotel }) => {
  return (
    <View style={tw`p-4 bg-white rounded-lg shadow mb-4`}>
      <Text style={tw`text-lg font-bold`}>{hotel.name}</Text>
      <Text style={tw`text-gray-600`}>Price: {hotel.price}</Text>
      <Text style={tw`text-gray-600`}>Rating: {hotel.rating}</Text>
    </View>
  );
};

export default HotelCard;