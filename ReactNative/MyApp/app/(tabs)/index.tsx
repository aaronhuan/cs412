import { View, Text, Image, ScrollView } from "react-native";
import { styles } from "../../assets/my_styles";

export default function IndexScreen() {
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
