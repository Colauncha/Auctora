// AuthStore.js
import { create } from "zustand";

const useAuthStore = create((set) => ({
  isAuthenticated: !!localStorage.getItem('userId'),
  login: (id) => {
    localStorage.setItem('userId', id);
    set({ isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem('userId');
    set({ isAuthenticated: false });
  },
}));

export default useAuthStore;
