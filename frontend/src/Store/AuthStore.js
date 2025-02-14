// AuthStore.js
import { create } from "zustand";

const useAuthStore = create((set) => ({
  isAuthenticated: false,
  login: () => set({ isAuthenticated: false }),
  logout: () => set({ isAuthenticated: false }),
}));

export default useAuthStore;
