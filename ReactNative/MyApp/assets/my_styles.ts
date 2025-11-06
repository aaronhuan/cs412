import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: '#f7f7f9',
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
        lineHeight: 22,
    },
    imageStyling: {
        width: 240,
        height: 240,
        borderRadius: 12,
        alignSelf: 'center',
    },
})
