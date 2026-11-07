import { useState } from 'react';
import { FlatList, Pressable, StyleSheet, TextInput, View } from 'react-native';

import { pupoPalette } from '@/constants/Colors';
import { Text } from '@/components/Themed';

export interface ChatMessage {
  role: 'student' | 'pupo';
  text: string;
}

export function Chat({
  placeholder,
  onSend,
}: {
  placeholder: string;
  onSend: (text: string) => Promise<string>;
}) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = async () => {
    const text = input.trim();
    if (!text || sending) return;
    setInput('');
    setError(null);
    setMessages((m) => [...m, { role: 'student', text }]);
    setSending(true);
    try {
      const reply = await onSend(text);
      setMessages((m) => [...m, { role: 'pupo', text: reply }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Errore');
    } finally {
      setSending(false);
    }
  };

  return (
    <View style={styles.wrap}>
      <FlatList
        data={messages}
        keyExtractor={(_, i) => String(i)}
        renderItem={({ item }) => (
          <View style={[styles.bubble, item.role === 'student' ? styles.studentBubble : styles.pupoBubble]}>
            <Text style={styles.bubbleText}>{item.text}</Text>
          </View>
        )}
        style={styles.list}
        contentContainerStyle={{ gap: 8, paddingVertical: 8 }}
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder={placeholder}
          value={input}
          onChangeText={setInput}
          onSubmitEditing={send}
          editable={!sending}
          multiline
        />
        <Pressable style={styles.sendButton} onPress={send} disabled={sending}>
          <Text style={styles.sendText}>{sending ? '...' : 'Invia'}</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, gap: 8 },
  list: { flex: 1 },
  bubble: { maxWidth: '85%', padding: 10, borderRadius: 12 },
  studentBubble: { alignSelf: 'flex-end', backgroundColor: pupoPalette.purple + '22' },
  pupoBubble: { alignSelf: 'flex-start', backgroundColor: pupoPalette.yellow + '22' },
  bubbleText: { fontSize: 15 },
  error: { color: pupoPalette.coral, fontSize: 13 },
  inputRow: { flexDirection: 'row', gap: 8, alignItems: 'flex-end' },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: pupoPalette.navy + '33',
    borderRadius: 10,
    padding: 10,
    minHeight: 40,
    maxHeight: 120,
  },
  sendButton: {
    backgroundColor: pupoPalette.purple,
    borderRadius: 10,
    paddingHorizontal: 16,
    paddingVertical: 10,
  },
  sendText: { color: '#fff', fontWeight: '600' },
});
