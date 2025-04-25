"use client"

import type React from "react"

export default function ClientLayout({ children }: { children: React.ReactNode }) {

  return (
    <div className="flex h-screen bg-background">
      <div className="flex-1 flex items-center justify-center">
        {children}
      </div> 
      {/* Real Time Updates Panel */}
      <div className="absolute right-0 w-80 h-64 border-l border-t bg-muted/10 p-4 overflow-y-auto">
        <h2 className="font-medium mb-2">Real Time Updates</h2>
        <div className="space-y-2">
          {/* Example updates */}
          <div className="text-sm">User: Hello, how are you?</div>
          <div className="text-sm">Bot: I'm good, thank you! How can I assist you today?</div>
        </div>
      </div>
    </div>
  )
}
