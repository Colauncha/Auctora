// useModeStore.js
import { create } from "zustand";
const useModeStore = create((set) => ({
  isMobile: false, // Default value
  toggleMode: () =>
    set((state) => ({
      isMobile: !state.isMobile,
    })),
  setModeBasedOnScreenSize: () =>
    set(() => ({
      isMobile: typeof window !== "undefined" && window.innerWidth <= 768,
    })),
}));

export default useModeStore;
