import { View, ScrollView, Text, Image } from "react-native";
import { styles } from "../../assets/my_styles";
export default function AboutScreen() {
    return (
        <View style={styles.screen}>
            <ScrollView contentContainerStyle={styles.content}>
                <Text style={styles.titleText}>About</Text>
                <Text style={styles.bodyText}>
                    This app was created to demonstrate a simple React Native application with multiple screens, for the purpose of my CS412 class.
                    It showcases my interests in video games and provides information about them.
                </Text>
                <Text style={styles.bodyText}>Below is a gif of Pedro</Text>
                <Image 
                    source = {{uri: "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXpmaW1jZHcyc3ZsdGZicDNwdXBpYnNjdGJtejd2dmhncjFxZHY2cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/7CjEqtZUm2OBmJ9eha/giphy.gif"}}
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
