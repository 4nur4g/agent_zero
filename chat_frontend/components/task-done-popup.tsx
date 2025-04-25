"use client"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { X, Check, ImageIcon } from "lucide-react"

interface TaskDonePopupProps {
  isOpen: boolean
  onClose: () => void
}

export default function TaskDonePopup({ isOpen, onClose }: TaskDonePopupProps) {
  if (!isOpen) return null

  const actions = [
    "Verified customer identity",
    "Checked billing information",
    "Provided payment options",
    "Scheduled follow-up call",
    "Updated customer notes",
  ]

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-background rounded-lg shadow-lg w-[calc(100%-32px)] max-w-3xl" style={{ height: "60vh" }}>
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="font-medium text-lg">Task Completion Summary</h2>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        <ScrollArea className="h-[calc(60vh-64px)]">
          <div className="p-4 space-y-6">
            <div>
              <h3 className="font-medium mb-2">Actions Completed</h3>
              <div className="space-y-2">
                {actions.map((action, index) => (
                  <div key={index} className="flex items-center gap-2 p-2 bg-muted/50 rounded-md">
                    <div className="h-6 w-6 rounded-full bg-green-100 flex items-center justify-center">
                      <Check className="h-4 w-4 text-green-600" />
                    </div>
                    <span>{action}</span>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Screenshots</h3>
              <div className="grid grid-cols-2 gap-4">
                {[1, 2, 3, 4].map((item) => (
                  <div
                    key={item}
                    className="border rounded-md p-2 aspect-video bg-muted/30 flex flex-col items-center justify-center"
                  >
                    <ImageIcon className="h-8 w-8 text-muted-foreground mb-2" />
                    <span className="text-sm text-muted-foreground">Screenshot {item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </ScrollArea>
      </div>
    </div>
  )
}
