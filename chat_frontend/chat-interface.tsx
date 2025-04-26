"use client"

import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"
import dayjs from "dayjs"
import { parseBackendData } from "@/utility/jsonDataParser";
import { useUpdates } from "@/context/UpdatesContext";

interface Message {
  role: "agent" | "user"
  content: string
  timestamp: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const { setUpdates } = useUpdates();
  const [input, setInput] = useState('');
  const [streamedContent, setStreamedContent] = useState('');

  const socketRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef(null);

  // Connect to WebSocket server
  useEffect(() => {
    // Create WebSocket connection
    socketRef.current = new WebSocket('ws://localhost:3006/ws/1');

    // Connection opened
    socketRef.current.addEventListener('open', (event: any) => {
      console.log('Connected to WebSocket server');
    });

    // Listen for messages
    socketRef.current.addEventListener('message', (event: any) => {
      try {
        // const data = JSON.parse(event.data);
        const data = event.data;
        console.log(' data --> ', data)
        const parsedData = parseBackendData(data);
        if(parsedData.type === 'agent_zero_updates') {
          setUpdates(prev => [...prev, parsedData.content]);
        }
        if (parsedData.response_metadata && parsedData.response_metadata?.finish_reason === "stop") {
          setMessages(prev => [
            ...prev,
            {
              role: parsedData.role || "agent",
              content: parsedData.content,
              timestamp: dayjs().format("YYYY-MM-DD HH:mm:ss"),
            },
          ]);
          setStreamedContent("");
        } else {
          setStreamedContent(prev => prev + parsedData.content);
        }
      } catch (error) {
        console.error("Invalid JSON stream message:", event.data);
      }
    });

    // Connection closed
    socketRef.current.addEventListener('close', (event) => {
      console.log('Disconnected from WebSocket server');
    });

    // Connection error
    socketRef.current.addEventListener('error', () => {
      console.log('WebSocket connection error - server might not be running');
    });

    // Clean up on unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if(messagesEndRef.current) {
      messagesEndRef.current?.scrollIntoView({behavior: 'smooth'});
    }
  }, [messages, streamedContent]);

  // Send a message
  const sendMessage = () => {
    if (!input.trim()) return;

    const newMessage = {
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };

    // Add message to state
    setMessages(prevMessages => [...prevMessages, newMessage]);

    // Send to server
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ message: input }));
    }

    // Clear input
    setInput('');
  };

  // Handle key press
  const handleKeyPress = (e: any) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
      <div className="h-full flex flex-col overflow-hidden">
        <ScrollArea className="flex-1 overflow-y-auto p-4">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div key={index} className={cn("flex gap-2", message.role === "user" ? "justify-end" : "justify-start")}>
                {message.role === "agent" && <div className="h-8 w-8 rounded-full bg-primary flex-shrink-0" />}
                <div className="space-y-2 max-w-[80%] break-words">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium">{message.role === "agent" ? "Generative Agent" : "G5"}</span>
                  </div>
                  <div className="p-3 bg-muted/50 rounded-lg">
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">{dayjs(message.timestamp).format('YYYY-MM-DD HH:mm:ss')}</span>
                  </div>
                </div>
              </div>
            ))}

            {/* Streamed message (live response) */}
            {streamedContent && (
              <div className="flex gap-2 justify-start">
                <div className="h-8 w-8 rounded-full bg-primary flex-shrink-0" />
                <div className="space-y-2 max-w-[80%] break-words">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium">GenerativeAgent</span>
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
            <div className="flex-1 flex items-center relative">
              <Textarea
                placeholder="Type a message as a customer"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="min-h-[44px] max-h-32 pl-10"
                onKeyDown={handleKeyPress}
              />
            </div>
            <Button className="px-8" onClick={sendMessage} >Send</Button>
          </div>
        </div>
      </div>
  )
}
