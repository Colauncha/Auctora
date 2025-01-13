// useModeStore.js
import { create } from "zustand";

const useModeStore = create((set) => ({
  isMobile: window.innerWidth <= 768, // Initial mode based on window size
  toggleMode: () =>
    set((state) => ({
      isMobile: !state.isMobile,
    })),
  setModeBasedOnScreenSize: () =>
    set(() => ({
      isMobile: window.innerWidth <= 768,
    })),
}));

export default useModeStore;
