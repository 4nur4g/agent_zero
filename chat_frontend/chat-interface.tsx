"use client"

import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"
import dayjs from "dayjs"
import { parseBackendData } from "@/utility/jsonDataParser";
import { useUpdates } from "@/context/UpdatesContext";
import { UpdateEmitter } from "@/utility/UpdateEmitter";

interface Message {
  role: "agent" | "user"; // Who sent the message
  type:
    | "agent_zero_updates"   // System/agent update
    | "from_agent_zero"      // Message from agent
    | "to_agent_zero"        // Message to agent
    | "from_human"           // From human user
    | "from_ai";             // From AI agent (if different from agent_zero)
  message: string;           // Actual message content
  timestamp: string;         // ISO string (recommended for date formatting)
}


export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('');
  const [streamedContent, setStreamedContent] = useState('');
  const socketRef = useRef<WebSocket | null>(null);
  const bufferRef = useRef<string>('');              // <-- buffer for accumulating chunks
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Connect to WebSocket server
  useEffect(() => {
    socketRef.current = new WebSocket('ws://localhost:3006/ws/1');

    socketRef.current.addEventListener('open', () => {
      console.log('Connected to WebSocket server');
    });

    socketRef.current.addEventListener('message', (event: MessageEvent) => {
      let parsed;
      try {
        parsed = parseBackendData(event.data);
        console.log("Parsed: 📷", parsed)
      } catch {
        console.error("Invalid JSON stream message:", event.data);
        return;
      }

      // handle zero-updates type
      if (parsed.type === 'agent_zero_updates') {
        UpdateEmitter.emit('new-update', parsed.message);
        return;
      }

      const chunk = parsed.message.text || '';

      // always append the new chunk to our ref buffer, then mirror to state so UI updates
      bufferRef.current += chunk;
      setStreamedContent(bufferRef.current);

      // if this is the last chunk, flush into messages and reset
      const finish = parsed.response_metadata?.finish_reason === "stop";
      if (finish) {
        setMessages(prev => [
          ...prev,
          {
            role: "agent",
            type: parsed.type,
            message: bufferRef.current,
            timestamp: dayjs().format("YYYY-MM-DD HH:mm:ss"),
          },
        ]);
        bufferRef.current = '';
        setStreamedContent('');
      }
    });

    socketRef.current.addEventListener('close', () => {
      console.log('Disconnected from WebSocket server');
    });

    socketRef.current.addEventListener('error', () => {
      console.log('WebSocket connection error - server might not be running');
    });

    return () => {
      socketRef.current?.close();
    };
  }, []);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamedContent]);

  const sendMessage = () => {
    if (!input.trim()) return;

    const newMsg: Message = {
      role: "user",
      message: input,
      type: messages.length > 0 ? messages[messages.length - 1].type === 'from_agent_zero' ? 'to_agent_zero' : 'from_human' : 'from_human',
      timestamp: dayjs().toISOString(),
    };

    setMessages(prev => [...prev, newMsg]);
    socketRef.current?.send(JSON.stringify({ message: input }));
    setInput('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <ScrollArea className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={cn("flex gap-2", msg.role === "user" ? "justify-end" : "justify-start")}
            >
              {msg.role === "agent" && <div className="h-8 w-8 rounded-full bg-primary flex-shrink-0" />}
              <div className="space-y-2 max-w-[80%] break-words">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">
                    {msg.role === "agent" ? "Generative Agent" : "You"}
                  </span>
                </div>
                <div className="p-3 bg-muted/50 rounded-lg">
                  <p className="text-sm whitespace-pre-wrap">{msg.message}</p>
                </div>
                <div>
                  <span className="text-sm text-muted-foreground">
                    {dayjs(msg.timestamp).format('YYYY-MM-DD HH:mm:ss')}
                  </span>
                </div>
              </div>
            </div>
          ))}

          {streamedContent && (
            <div className="flex gap-2 justify-start">
              <div className="h-8 w-8 rounded-full bg-primary flex-shrink-0" />
              <div className="space-y-2 max-w-[80%] break-words">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">Generative Agent</span>
                </div>
                <div className="p-3 bg-muted/50 rounded-lg">
                  <p className="text-sm whitespace-pre-wrap">{streamedContent}</p>
                </div>
              </div>
            </div>
          )}
        </div>
        <div ref={messagesEndRef} />
      </ScrollArea>

      <div className="p-4 border-t">
        <div className="flex gap-2">
          <Textarea
            placeholder="Type a message as a customer"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            className="flex-1 min-h-[44px] max-h-32"
          />
          <Button onClick={sendMessage} className="px-8">Send</Button>
        </div>
      </div>
    </div>
  )
}