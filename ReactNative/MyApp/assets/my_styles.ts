// File: assets/my_styles.ts
// created at: 11/06/2025, ahuan@bu.edu
// Description: This file contains the styles used in the DetailScreen component.
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: '#c4e8f4ff',
        padding:60,
    },
    content: {
        padding: 16,
        gap: 12,
    },
    titleText: {
        fontSize: 22,
        fontWeight: '600',
        textAlign: 'center',
        marginBottom: 8,
    },
    bodyText: {
        fontSize: 16,
        lineHeight: 30,
    },
    imageStyling: {
        width: 240,
        height: 240,
        borderRadius: 12,
        alignSelf: 'center',
    },
    subtitleText: {
        fontSize: 20,
        fontWeight: '500',
        marginTop: 12,
        marginBottom: 6,
        alignSelf: 'center',
    },
    
})
