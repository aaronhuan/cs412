/*
File: (tabs)/add_joke.tsx
Author: Aaron Huang (ahuan@bu.edu), 11/14/2025
Description: Screen to add a joke, calls POST API endpoint.
*/
import { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import { styles } from "@/assets/my_styles";

export default function AddJokeScreen(){
    //states to keep track of inputs + post process 
    const [text, setText] = useState("");
    const [name, setName] = useState("");
    const [isPosting, setisPosting] = useState(false);

    //async call to POST the text and name 
    const addJoke = async () => {
        try{
            setisPosting(true);
            const response = await fetch(`https://cs-webapps.bu.edu/ahuan/dadjokes/api/jokes/`,{
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    name: name
                })
            });
            console.log("Joke added:", await response.json());
        } catch (error){
            console.error("Error adding joke:", error);
        }
        //reset the inputs and status of isposting
        setText("");
        setName("");
        setisPosting(false);
    }
    return (
        <View style={styles.container}>
            <View style={styles.card}>

                <Text style={styles.title}>Add a new joke</Text>
                <TextInput
                    placeholder= "Enter Joke"
                    value = {text}
                    onChangeText={setText}
                    multiline
                    style={styles.input}
                />
                <TextInput
                    placeholder= "Enter Your Name"
                    value = {name}
                    onChangeText={setName}
                    style={styles.input}
                />
                <Button
                    title={isPosting ? "Adding..." : "Add Joke"}
                    onPress={addJoke}
                    disabled={isPosting}
                />
            </View>
        </View>
    );
}