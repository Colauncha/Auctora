// useScreenModeStore.js
import { create } from "zustand";

const useScreenModeStore = create((set) => ({
  isMobile: window.innerWidth <= 768, // Determine initial mode based on screen size
  setMode: (isMobile) => set(() => ({ isMobile })),
}));

export default useScreenModeStore;
