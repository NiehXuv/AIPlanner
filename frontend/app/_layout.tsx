import { Stack } from 'expo-router';
import { View } from 'react-native';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="create-trip" options={{ headerShown: false }} />
      <Stack.Screen name="view-plan/[planId]" options={{ headerShown: false }} />
      <Stack.Screen name="hotel-search" options={{ headerShown: false }} />
    </Stack>
  );
}