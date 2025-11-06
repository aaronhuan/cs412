import { View, ScrollView, Text, Image } from "react-native";
import { styles } from "../../assets/my_styles";
export default function DetailScreen() {
    return (
        <View style={styles.screen}>
            <ScrollView contentContainerStyle={styles.content}>
                <Text style={styles.titleText}>Details</Text>
                <Text style={styles.bodyText}>One interest of mine is playing video games</Text>
                <Text style={styles.bodyText}>Stardew Valley</Text>
                <Image 
                    source={{ uri: "https://wallpapers.com/images/hd/2d-stardew-valley-game-logo-poster-twhcnbrs001ypbap.jpg" }}
                    style ={styles.imageStyling}
                />
                <Text style={styles.bodyText}>Stardew Valley is a charming farming simulation game that invites players to
                     build a thriving homestead while exploring a richly detailed world.
                      Beyond planting crops and raising animals, you can fish in rivers,
                     dive into mines for resources, and form meaningful relationships
                    with the quirky townspeople. Its blend of relaxing gameplay and open-ended 
                    exploration makes it a cozy escape with endless possibilities.
                </Text>

                <Text style={styles.bodyText}>Marvel Rivals</Text>
                <Image 
                    source={{ uri: "https://insider-gaming.com/wp-content/uploads/2024/12/marvel-rivals-top-numbers.jpg" }}
                    style ={styles.imageStyling}
                />
                <Text style={styles.bodyText}>Marvel Rivals is an action-packed mobile game that brings together a roster
                    of iconic Marvel superheroes and villains for thrilling battles.
                    Players can collect and upgrade their favorite characters, each with unique abilities 
                    and playstyles, to form powerful teams. The game features fast-paced combat,
                    strategic team-building, and a variety of game modes, including PvP battles and cooperative missions.
                    With its vibrant graphics and engaging gameplay, Marvel Rivals offers fans an exciting way to experience 
                    the Marvel Universe on the go.</Text>

                <Text style={styles.bodyText}>Minecraft</Text>
                <Image 
                    source = {{uri: "https://tse2.mm.bing.net/th/id/OIP.2M4fgHS0qstJAwCRRsR-sAHaEK?rs=1&pid=ImgDetMain&o=7&rm=3"}} 
                    style ={styles.imageStyling}/>
                <Text style={styles.bodyText}>Minecraft is a sandbox video game that allows players to explore, build, and survive in a blocky, procedurally generated 3D world.
                    Players can gather resources, craft tools and items, and construct elaborate structures or entire cities.
                    The game features various modes, including Survival, where players must manage health and hunger, and Creative, which provides unlimited resources for building.
                    Minecraft's open-ended gameplay encourages creativity and exploration, making it a beloved title for players of all ages.</Text>
            </ScrollView>
        </View>
    );
}
