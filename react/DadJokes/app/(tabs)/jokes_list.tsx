/*
File: (tabs)/jokes_list.tsx
Author: Aaron Huang (ahuan@bu.edu), 11/14/2025
Description: Screen to show all jokes.
*/
import { styles } from "@/assets/my_styles";
import { useState, useEffect } from "react";
import { View, Text, FlatList } from "react-native";

type Joke = { //type defined, used to specify the attributes of an item
    id: number;
    text: string;
    name: string;
};

export default function JokeListScreen(){
    const [jokes, setJokes] = useState<Joke[]>([]);
    const [refreshing, setRefreshing] = useState(false)

    const fetchAllJokes = async () => {
        try {
            const response = await fetch(`https://cs-webapps.bu.edu/ahuan/dadjokes/api/jokes/`);
            const data = await response.json();
            setJokes(data.results as Joke[]);
        } catch (error) {
            console.error("Error fetching jokes:", error);
        }
    }

    //use effect, fetch once when rendering 
    useEffect(() => {
        fetchAllJokes();
    }, []);
    
    //refresh by fetching again
    function handleRefresh(){
        setRefreshing(true);
        fetchAllJokes().then(() => setRefreshing(false));
    }

    return(
        <View style={styles.container}>
            <FlatList
                data={jokes}
                renderItem={({ item }: { item: Joke }) => {
                    return (
                    <View style={styles.card}>
                        <Text style={styles.jokeText}>{item.text}</Text>
                        <Text style={styles.jokeText}>-- by {item.name}</Text>
                    </View>
                    );
                }}
                ItemSeparatorComponent={() => <View style={{ height: 10 }} />}
                ListEmptyComponent={<Text style={styles.jokeText}>no Jokes</Text>}
                ListHeaderComponent={<Text style={styles.title}>All Dad Jokes</Text>}
                ListFooterComponent={<Text style={styles.jokeText}>End of Jokes</Text>}
                refreshing={refreshing}
                onRefresh = {handleRefresh}
            />
        </View>
    );
}