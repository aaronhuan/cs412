// File: app/(tabs)/about.tsx
// created at: 11/06/2025, ahuan@bu.edu
// Description: This file contains the about screen of the app using react-native components.

import { View, ScrollView, Text, Image } from "react-native";
import { styles } from "../../assets/my_styles";
export default function AboutScreen() {
    // About screen content inside a ScrollView nested in a View, composed of an external images and text. 
    return (
        <View style={styles.screen}>
            <ScrollView contentContainerStyle={styles.content}>
                <Text style={styles.titleText}>About Screen</Text>
                <Text style={styles.bodyText}>
                    This app was created to demonstrate a simple React Native application with multiple screens, for the purpose of my CS412 class.
                    It showcases my interests in video games and provides information about them.
                </Text>
                <Text style={styles.bodyText}>Below is a gif of Pedro</Text>
                <Image 
                    source = {{uri: "https://cs-people.bu.edu/ahuan/images/pedro.webp"}}
                    style = {styles.imageStyling}
                />
                <Text style={styles.bodyText}>The viral clip shows Ginger, a baby raccoon owned by Russian TikTok user @fleksa30,
                    spinning and bobbing in a fisheye lens effect that makes her look like she’s dancing in a circle.
                    The video gained traction in mid-April 2024, especially on TikTok and meme platforms, where users synced the raccoon's
                    movements to the beat of the remix track “Pedro” by Jaxomy, Agatino Romero, and Raffaella Carrà.
                </Text>
                
            </ScrollView>
        </View>
    );
}
