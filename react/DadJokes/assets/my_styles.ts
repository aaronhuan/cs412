import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingTop:40,
        paddingHorizontal:20,
        alignItems: 'center',
        backgroundColor: '#d7e4f3ed',
    },
    title: {
        fontSize:25,
        fontWeight:'bold',
        marginBottom:20,
        textAlign:'center',
    },
    card: {
        width:"100%",
        alignItems: 'center',
        borderRadius: 10,
        backgroundColor: '#9dc3b6ff',
        elevation: 3,
        marginHorizontal:20,
        marginVertical:10,
        padding:15,
    },
    jokeText: {
        fontSize:20,
        textAlign:'center',
        padding:5,
    },
    image:{
        width: 300,
        height: 300,
        borderRadius: 10,
        marginVertical: 15,
    },
    buttonWrapper:{
        marginTop:20,
        width:'60%',
        alignSelf:'center',
    },
    input: {
        width: "95%",
        backgroundColor: "white",
        borderRadius: 8,
        paddingHorizontal: 10,
        paddingVertical: 8,
        marginVertical: 8,
        fontSize: 16,
    },
});