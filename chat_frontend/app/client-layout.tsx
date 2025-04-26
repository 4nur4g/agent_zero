"use client"

import React, { useEffect } from "react"

import {UpdatesProvider, useUpdates} from "@/context/UpdatesContext";
  import { UpdateEmitter } from "@/utility/UpdateEmitter";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <UpdatesProvider>
      <LayoutContent>{children}</LayoutContent>
    </UpdatesProvider>
  );
}

function LayoutContent({ children }: { children: React.ReactNode }) {
  let { updates, setUpdates } = useUpdates();

  useEffect(() => {
    const handler = (msg: string) => {
      setUpdates(prev => [...prev, msg]);
    };

    UpdateEmitter.on('new-update', handler);

    return () => {
      UpdateEmitter.off('new-update', handler);
    };
  }, []);

  return (
    <div className="flex h-screen w-screen bg-background">
      <div className="w-4/5 flex flex-col border-r">
        <header className="px-6 py-4 border-b">
          <h1 className="text-lg font-semibold">Chat with PbPartners Agent</h1>
        </header>
        <div className="flex-1 overflow-hidden">{children}</div>
      </div>

      <div className="w-1/5 h-full overflow-y-auto p-4 bg-muted/10 border-l border-border">
        <h2 className="font-semibold text-lg text-muted-foreground mb-4">Real Time Updates</h2>
        <div className="space-y-3 text-sm">
            {updates.map((update: string, index: number) => {
              const match = update.match(/\*\*Thoughts:\*\*\s*(\{.*\})/);
              let thoughtsObject = null;
              if (match && match[1]) {
                try {
                  thoughtsObject = JSON.parse(match[1]);
                } catch (err) {
                  console.error('Failed to parse JSON:', err);
                }
              }
              return (
                <div
                  key={index}
                  className="bg-muted px-3 py-2 rounded-md text-sm text-muted-foreground border border-border shadow-sm"
                >
                  <p className="font-medium">Thoughts:</p>
                  {thoughtsObject ? (
                    <ul className="list-disc pl-5 mt-1 space-y-1">
                      {Object.entries(thoughtsObject).map(([key, value]) => (
                        <li key={key}>
                          <strong>{key}:</strong> {String(value)}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <pre className="whitespace-pre-wrap">{update}</pre>
                  )}
                </div>
              );
            })}

        </div>
      </div>
    </div>
  );
}