import React, { useState } from 'react';
import { StyleSheet, ScrollView, TextInput, TouchableOpacity, Alert, ActivityIndicator } from 'react-native';
import { router } from 'expo-router';
import DatePicker from 'react-native-date-picker';

import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';
import { planService } from '@/services/ApiService';

const interests = [
  'History', 'Art', 'Food', 'Nature', 'Adventure', 
  'Shopping', 'Nightlife', 'Culture', 'Architecture', 'Music'
];

export default function CreatePlanScreen() {
  const colorScheme = useColorScheme();
  const [location, setLocation] = useState('');
  const [startDate, setStartDate] = useState(new Date());
  const [days, setDays] = useState('3');
  const [budget, setBudget] = useState('medium');
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [datePickerOpen, setDatePickerOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

interface InterestToggleProps {
    interest: string;
}

const handleInterestToggle = (interest: InterestToggleProps['interest']): void => {
    if (selectedInterests.includes(interest)) {
        setSelectedInterests(selectedInterests.filter((item: string) => item !== interest));
    } else {
        setSelectedInterests([...selectedInterests, interest]);
    }
};

  const handleCreatePlan = async () => {
    if (!location) {
      Alert.alert('Error', 'Please enter a location');
      return;
    }

    if (selectedInterests.length === 0) {
      Alert.alert('Error', 'Please select at least one interest');
      return;
    }

    setIsLoading(true);

    try {
      // Prepare request data
      const planRequest = {
        location,
        start_date: startDate.toISOString().split('T')[0],
        days: parseInt(days),
        budget,
        interests: selectedInterests
      };

      // Call API to generate plan
      const response = await planService.generatePlan(planRequest);
      
      // Navigate to plan view screen with the plan ID
      router.push({
        pathname: '/plan-view',
        params: { planId: response.plan_id }
      });
    } catch (error) {
      console.error('Error creating plan:', error);
      
      // Show error message
      const errorMessage = 
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 
        'Failed to create plan. Please try again.';
      Alert.alert(
        'Error',
        errorMessage,
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <ThemedText type="title" style={styles.title}>Create Your Trip Plan</ThemedText>
        
        <ThemedText type="subtitle" style={styles.label}>Destination</ThemedText>
        <TextInput
          style={[
            styles.input,
            { backgroundColor: Colors[colorScheme ?? 'light'].background }
          ]}
          placeholder="Enter city (e.g., Paris, Tokyo)"
          placeholderTextColor={Colors[colorScheme ?? 'light'].text}
          value={location}
          onChangeText={setLocation}
          editable={!isLoading}
        />
        
        <ThemedText type="subtitle" style={styles.label}>Start Date</ThemedText>
        <TouchableOpacity 
          style={[
            styles.input, 
            styles.dateInput,
            { backgroundColor: Colors[colorScheme ?? 'light'].background }
          ]}
          onPress={() => setDatePickerOpen(true)}
          disabled={isLoading}
        >
          <ThemedText>{startDate.toISOString().split('T')[0]}</ThemedText>
        </TouchableOpacity>
        
        <DatePicker
          modal
          open={datePickerOpen}
          date={startDate}
          mode="date"
          minimumDate={new Date()}
          onConfirm={(date) => {
            setDatePickerOpen(false);
            setStartDate(date);
          }}
          onCancel={() => {
            setDatePickerOpen(false);
          }}
        />
        
        <ThemedText type="subtitle" style={styles.label}>Number of Days</ThemedText>
        <TextInput
          style={[
            styles.input,
            { backgroundColor: Colors[colorScheme ?? 'light'].background }
          ]}
          placeholder="Number of days"
          placeholderTextColor={Colors[colorScheme ?? 'light'].text}
          value={days}
          onChangeText={setDays}
          keyboardType="numeric"
          editable={!isLoading}
        />
        
        <ThemedText type="subtitle" style={styles.label}>Budget</ThemedText>
        <ThemedView style={styles.budgetContainer}>
          {['low', 'medium', 'high'].map((item) => (
            <TouchableOpacity
              key={item}
              style={[
                styles.budgetButton,
                budget === item && styles.selectedBudget,
                budget === item && { backgroundColor: Colors[colorScheme ?? 'light'].tint }
              ]}
              onPress={() => setBudget(item)}
              disabled={isLoading}
            >
              <ThemedText 
                style={[
                  budget === item && styles.selectedBudgetText,
                  budget === item && { color: '#fff' }
                ]}
              >
                {item.charAt(0).toUpperCase() + item.slice(1)}
              </ThemedText>
            </TouchableOpacity>
          ))}
        </ThemedView>
        
        <ThemedText type="subtitle" style={styles.label}>Interests</ThemedText>
        <ThemedView style={styles.interestsContainer}>
          {interests.map((interest) => (
            <TouchableOpacity
              key={interest}
              style={[
                styles.interestButton,
                selectedInterests.includes(interest) && styles.selectedInterest,
                selectedInterests.includes(interest) && { backgroundColor: Colors[colorScheme ?? 'light'].tint }
              ]}
              onPress={() => handleInterestToggle(interest)}
              disabled={isLoading}
            >
              <ThemedText 
                style={[
                  selectedInterests.includes(interest) && styles.selectedInterestText,
                  selectedInterests.includes(interest) && { color: '#fff' }
                ]}
              >
                {interest}
              </ThemedText>
            </TouchableOpacity>
          ))}
        </ThemedView>
        
        <TouchableOpacity 
          style={[
            styles.createButton,
            { backgroundColor: Colors[colorScheme ?? 'light'].tint },
            isLoading && styles.disabledButton
          ]}
          onPress={handleCreatePlan}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <ThemedText style={styles.createButtonText}>Create Plan</ThemedText>
          )}
        </TouchableOpacity>
      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  scrollView: {
    flex: 1,
  },
  title: {
    marginTop: 60,
    marginBottom: 24,
    textAlign: 'center',
  },
  label: {
    marginTop: 16,
    marginBottom: 8,
  },
  input: {
    height: 50,
    borderRadius: 8,
    paddingHorizontal: 16,
    marginBottom: 8,
  },
  dateInput: {
    justifyContent: 'center',
  },
  budgetContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  budgetButton: {
    flex: 1,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 8,
    marginHorizontal: 4,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  selectedBudget: {
    borderWidth: 0,
  },
  selectedBudgetText: {
    fontWeight: 'bold',
  },
  interestsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 24,
  },
  interestButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    margin: 4,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  selectedInterest: {
    borderWidth: 0,
  },
  selectedInterestText: {
    fontWeight: 'bold',
  },
  createButton: {
    height: 50,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 32,
  },
  createButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  disabledButton: {
    opacity: 0.7,
  },
});
