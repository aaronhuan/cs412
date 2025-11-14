/*
File: (tabs)/index.tsx
Author: Aaron Huang (ahuan@bu.edu), 11/14/2025
Description: Screen to show a random joke and image.
*/

import { Text, View, Image, Button }from 'react-native';
import { useState, useEffect } from "react";
import { styles } from '../../assets/my_styles';

export default function IndexScreen(){
  //states to keep track of joke, picture, and if the user pressed the button
  const [pressed, setPressed] = useState(0);
  const [joke, setJoke] = useState("");
  const [picture, setPicture] = useState("");

  //GET a joke
  const fetchJoke = async () =>{
    try {
      const response = await fetch(`https://cs-webapps.bu.edu/ahuan/dadjokes/api/`);
      console.log(response);
      const data = await response.json();
      setJoke(data.text);
    } catch (error) {
      console.error("Error fetching joke:", error);
    } 
  }

  //GET a picture
  const fetchPicture = async () =>{
    try{
      const response = await fetch(`https://cs-webapps.bu.edu/ahuan/dadjokes/api/random_picture`);
      const data = await response.json();

      let picture_url = "";
      if(data.image_file){
        picture_url = data.image_file
      }else if (data.image_url){
        picture_url = data.image_url
      }
      setPicture(picture_url);
    } catch (error){
      console.error("Error fetching picture:", error);
    }
  }

  //useEffect to call the functions that fetch joke and picture whenever the pressed state changes
  useEffect(() =>{
    fetchJoke()
    fetchPicture()
  },[pressed]);

  return(
    <View style={styles.container}>
      <Text style={styles.title}>Random Joke</Text>
      <View style={styles.card}>
        <Text style={styles.jokeText}>{joke}</Text>
        <Image source={{uri: picture}} style={styles.image}/>
      </View>
      <View style = {styles.buttonWrapper}>
        <Button
        title= "Press fer 'nother one"
        onPress={()=>setPressed(pressed +1)}
        />
      </View>
    </View>
  );
}