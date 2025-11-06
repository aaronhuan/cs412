// File: app/(tabs)/index.tsx
// created at: 11/06/2025, ahuan@bu.edu
// Description: This file contains the index screen of the app using react-native components.


import { View, Text, Image, ScrollView } from "react-native";
import { styles } from "../../assets/my_styles";

export default function IndexScreen() {
    // About screen content inside a ScrollView nested in a View, composed of static image and text. 
  const teletubbyimg = require('../../assets/images/teletubby.jpg');
    return (
        <View style={styles.screen}>
            <ScrollView contentContainerStyle={styles.content}>
                <Text style={styles.titleText}>Index Screen</Text>
                <Image source={teletubbyimg} style={styles.imageStyling} />
                <Text style={styles.bodyText}>
                  Hello, this is the index screen. Above is a random picture of a teletubby I already have
                  on my laptop from my mini instagram app study for cs412. The picture is stored in the assets folder.
                </Text>
            </ScrollView>
        </View>
    );
}
