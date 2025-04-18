import React from 'react';
import { View, Text, TextInput, FlatList, TouchableOpacity, Button } from 'react-native';
import tw from 'twrnc';
import { Calendar } from 'react-native-calendars';

interface PlanWizardStepProps {
  step: number;
  totalSteps: number;
  data: any;
  onChange: (key: string, value: any) => void;
  onNext: () => void;
  onBack: () => void;
  cities: string[];
}

const PlanWizardStep: React.FC<PlanWizardStepProps> = ({
  step,
  totalSteps,
  data,
  onChange,
  onNext,
  onBack,
  cities,
}) => {
  switch (step) {
    case 1: // Location
      return (
        <View style={tw`flex-1 p-4`}>
          <Text style={tw`text-lg font-bold mb-4`}>Choose a Destination</Text>
          <TextInput
            style={tw`border border-gray-300 rounded p-2 mb-4`}
            placeholder="Search..."
            value={data.location}
            onChangeText={(text) => onChange('location', text)}
          />
          <Text style={tw`text-gray-600 mb-2`}>Most Popular Cities</Text>
          <FlatList
            data={cities}
            keyExtractor={(item) => item}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={tw`py-2 border-b border-gray-200`}
                onPress={() => onChange('location', item)}
              >
                <Text style={tw`text-gray-800`}>{item}</Text>
              </TouchableOpacity>
            )}
          />
          <View style={tw`flex-row justify-between mt-4`}>
            <Button title="Cancel" onPress={onBack} />
            <Button title="Next" onPress={onNext} disabled={!data.location} />
          </View>
        </View>
      );

    case 2: // Start Date
      return (
        <View style={tw`flex-1 p-4`}>
          <Text style={tw`text-lg font-bold mb-4`}>Start Date</Text>
          <Text style={tw`text-gray-600 mb-4`}>Choose the start date for your trip using the calendar.</Text>
          <Calendar
            onDayPress={(day: { dateString: string }) => onChange('start_date', day.dateString)}
            markedDates={{
              [data.start_date || '']: { selected: true, selectedColor: 'blue' },
            }}
            minDate={new Date().toISOString().split('T')[0]}
            maxDate="2025-12-31"
          />
          <View style={tw`flex-row justify-between mt-4`}>
            <Button title="Back" onPress={onBack} />
            <Button title="Next" onPress={onNext} disabled={!data.start_date} />
          </View>
        </View>
      );

    case 3: // Duration
      return (
        <View style={tw`flex-1 p-4`}>
          <Text style={tw`text-lg font-bold mb-4`}>Trip Duration</Text>
          <TextInput
            style={tw`border border-gray-300 rounded p-2 mb-4`}
            placeholder="Number of days"
            keyboardType="numeric"
            value={data.days?.toString() || ''}
            onChangeText={(text) => onChange('days', parseInt(text) || 1)}
          />
          <View style={tw`flex-row justify-between mt-4`}>
            <Button title="Back" onPress={onBack} />
            <Button title="Next" onPress={onNext} disabled={!data.days || data.days < 1} />
          </View>
        </View>
      );

    case 4: // Interests
      const interests = ['Historical', 'Art & Culture', 'Nature', 'Relaxing', 'Shopping', 'Entertainment', 'Sports', 'Adventure'];
      return (
        <View style={tw`flex-1 p-4`}>
          <Text style={tw`text-lg font-bold mb-4`}>Interests</Text>
          <Text style={tw`text-gray-600 mb-4`}>Select your interests and assign a preference score (0-1).</Text>
          {interests.map((interest) => (
            <View key={interest} style={tw`flex-row items-center mb-2`}>
              <Text style={tw`flex-1`}>{interest}</Text>
              <TextInput
                style={tw`border border-gray-300 rounded p-2 w-20`}
                placeholder="0-1"
                keyboardType="numeric"
                value={data.interests?.[interest]?.toString() || ''}
                onChangeText={(text) => {
                  const score = parseFloat(text);
                  if (score >= 0 && score <= 1) {
                    onChange('interests', { ...data.interests, [interest]: score });
                  }
                }}
              />
            </View>
          ))}
          <View style={tw`flex-row justify-between mt-4`}>
            <Button title="Back" onPress={onBack} />
            <Button title="Next" onPress={onNext} disabled={Object.keys(data.interests || {}).length === 0} />
          </View>
        </View>
      );

    case 5: // Budget
      return (
        <View style={tw`flex-1 p-4`}>
          <Text style={tw`text-lg font-bold mb-4`}>Budget</Text>
          <TextInput
            style={tw`border border-gray-300 rounded p-2 mb-4`}
            placeholder="Budget in USD"
            keyboardType="numeric"
            value={data.budget?.toString() || ''}
            onChangeText={(text) => onChange('budget', parseInt(text) || 0)}
          />
          <View style={tw`flex-row justify-between mt-4`}>
            <Button title="Back" onPress={onBack} />
            <Button title="Next" onPress={onNext} disabled={!data.budget || data.budget <= 0} />
          </View>
        </View>
      );

    case 6: // Travel Type
      const travelTypes = ['Solo', 'With spouse', 'With family', 'With friends'];
      return (
        <View style={tw`flex-1 p-4`}>
          <Text style={tw`text-lg font-bold mb-4`}>Travel Type</Text>
          <FlatList
            data={travelTypes}
            keyExtractor={(item) => item}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={tw`py-2 border-b border-gray-200`}
                onPress={() => onChange('travelType', item)}
              >
                <Text style={tw`text-gray-800`}>{item}</Text>
              </TouchableOpacity>
            )}
          />
          <View style={tw`flex-row justify-between mt-4`}>
            <Button title="Back" onPress={onBack} />
            <Button title="Finish" onPress={onNext} disabled={!data.travelType} />
          </View>
        </View>
      );

    default:
      return null;
  }
};

export default PlanWizardStep;