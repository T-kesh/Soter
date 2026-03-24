import React, { useMemo } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/types';
import { useTheme } from '../theme/ThemeContext';
import { AppColors } from '../theme/useAppTheme';

type Props = NativeStackScreenProps<RootStackParamList, 'AidDetails'>;

export const AidDetailsScreen: React.FC<Props> = ({ route }) => {
  const { aidId } = route.params;
  const { colors } = useTheme();
  const styles = useMemo(() => makeStyles(colors), [colors]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Aid Details</Text>
      <Text style={styles.subtitle}>ID: {aidId}</Text>
      <Text style={styles.subtitle}>Coming Soon in a future wave</Text>
    </View>
  );
};

const makeStyles = (colors: AppColors) =>
  StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: colors.background,
    },
    title: {
      fontSize: 24,
      fontWeight: '700',
      color: colors.textPrimary,
    },
    subtitle: {
      fontSize: 16,
      color: colors.textSecondary,
      marginTop: 8,
    },
  });
