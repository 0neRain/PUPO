import { StyleSheet, View } from 'react-native';

import { pupoPalette } from '@/constants/Colors';
import { Text } from '@/components/Themed';

export function ProgressBar({ percent, label }: { percent: number; label?: string }) {
  const clamped = Math.max(0, Math.min(100, percent));
  return (
    <View style={styles.wrap}>
      {label ? <Text style={styles.label}>{label}</Text> : null}
      <View style={styles.track}>
        <View style={[styles.fill, { width: `${clamped}%` }]} />
      </View>
      <Text style={styles.percent}>{clamped}%</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 4 },
  label: { fontSize: 14, fontWeight: '600' },
  track: {
    height: 14,
    borderRadius: 7,
    backgroundColor: pupoPalette.navy + '22',
    overflow: 'hidden',
  },
  fill: {
    height: '100%',
    borderRadius: 7,
    backgroundColor: pupoPalette.mint,
  },
  percent: { fontSize: 12, opacity: 0.7 },
});
