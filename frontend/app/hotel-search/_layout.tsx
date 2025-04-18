import { Stack } from 'expo-router';

export default function HotelSearchLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ headerShown: false }} />
    </Stack>
  );
}