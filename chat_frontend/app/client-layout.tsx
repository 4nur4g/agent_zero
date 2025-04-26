"use client"

import React from "react"

import {UpdatesProvider, useUpdates} from "@/context/UpdatesContext";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <UpdatesProvider>
      <LayoutContent>{children}</LayoutContent>
    </UpdatesProvider>
  );
}

function LayoutContent({ children }: { children: React.ReactNode }) {
  const { updates } = useUpdates();

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
          {updates.map((update:any, index: number) => (
            <div
              key={index}
              className="bg-muted px-3 py-2 rounded-md text-sm text-muted-foreground border border-border shadow-sm"
            >
              {update}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}