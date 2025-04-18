import { View, Text } from 'react-native';
import tw from 'twrnc';

export default function InboxScreen() {
  return (
    <View style={tw`flex-1 justify-center items-center`}>
      <Text style={tw`text-lg`}>Inbox Screen</Text>
    </View>
  );
}