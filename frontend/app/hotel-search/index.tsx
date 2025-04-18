import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList, ActivityIndicator, Alert, TouchableOpacity } from 'react-native';
import tw from 'twrnc';
import { router } from 'expo-router';
import { useApi } from '../../hooks/useApi';
import HotelCard from '../../components/HotelCard';

export default function HotelSearchScreen() {
  const { searchHotels, loading, error } = useApi();
  const [formData, setFormData] = useState({
    location: '',
    checkin: '',
    checkout: '',
  });
  const [hotels, setHotels] = useState<any[]>([]);

  const handleChange = (key: string, value: string) => {
    setFormData({ ...formData, [key]: value });
  };

  const handleSearch = async () => {
    try {
      const data = await searchHotels(formData.location, formData.checkin, formData.checkout);
      setHotels(data);
    } catch (err) {
      Alert.alert('Error', error || 'Failed to search hotels');
    }
  };

  return (
    <View style={tw`flex-1 bg-white p-4`}>
      <TouchableOpacity onPress={() => router.back()} style={tw`mb-4`}>
        <Text style={tw`text-blue-500`}>Back</Text>
      </TouchableOpacity>
      <Text style={tw`text-lg font-bold mb-4`}>Search Hotels</Text>
      <TextInput
        style={tw`border border-gray-300 rounded p-2 mb-4`}
        placeholder="Location"
        value={formData.location}
        onChangeText={(text) => handleChange('location', text)}
      />
      <TextInput
        style={tw`border border-gray-300 rounded p-2 mb-4`}
        placeholder="Check-in Date (YYYY-MM-DD)"
        value={formData.checkin}
        onChangeText={(text) => handleChange('checkin', text)}
      />
      <TextInput
        style={tw`border border-gray-300 rounded p-2 mb-4`}
        placeholder="Check-out Date (YYYY-MM-DD)"
        value={formData.checkout}
        onChangeText={(text) => handleChange('checkout', text)}
      />
      <Button title="Search" onPress={handleSearch} disabled={loading} />
      {loading && <ActivityIndicator size="large" color="#0000ff" style={tw`mt-4`} />}
      <FlatList
        data={hotels}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => <HotelCard hotel={item} />}
        contentContainerStyle={tw`mt-4`}
      />
    </View>
  );
}