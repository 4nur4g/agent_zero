// context/UpdatesContext.tsx
"use client"

import React, { createContext, useContext, useState, ReactNode } from "react";

type UpdatesContextType = {
  updates: string[];
  setUpdates: React.Dispatch<React.SetStateAction<string[]>>;
};

const UpdatesContext = createContext<UpdatesContextType | undefined>(undefined);

export const useUpdates = () => {
  const context = useContext(UpdatesContext);
  if (!context) throw new Error("useUpdates must be used within an UpdatesProvider");
  return context;
};

export const UpdatesProvider = ({ children }: { children: ReactNode }) => {
  const [updates, setUpdates] = useState<string[]>([]);
  return (
    <UpdatesContext.Provider value={{ updates, setUpdates }}>
      {children}
    </UpdatesContext.Provider>
  );
};
