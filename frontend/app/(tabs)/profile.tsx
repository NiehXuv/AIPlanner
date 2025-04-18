import { View, Text } from 'react-native';
import tw from 'twrnc';

export default function ProfileScreen() {
  return (
    <View style={tw`flex-1 justify-center items-center`}>
      <Text style={tw`text-lg`}>Profile Screen</Text>
    </View>
  );
}