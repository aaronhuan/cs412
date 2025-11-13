import { Text, View, Image }from 'react-native';
import { useState, useEffect } from "react";
export default function index(){
  const [joke, setJoke] = useState("");
  const [picture, setPicture] = useState("");

  const fetchJoke = async () =>{
    try {
      const response = await fetch(`http://127.0.0.1:8000/dadjokes/api/`);
      console.log(response);
      const data = await response.json();
      setJoke(data.text);
    } catch (error) {
      console.error("Error fetching joke:", error);
    } 
  }

  const fetchPicture = async () =>{
    try{
      const response = await fetch(`http://127.0.0.1:8000/dadjokes/api/random_picture`);
      const data = await response.json();
      setPicture(data.picture);
    } catch (error){
      console.error("Error fetching picture:", error);
    }
  }

  useEffect(() =>{
    fetchJoke()
    fetchPicture()
  }, []);

  return(
    <View>
      <Text>Random Joke</Text>
      <Text>{joke}</Text>
      <Image source={{uri: picture}} style={{width: 200, height: 200}}/>
    </View>
  );
}