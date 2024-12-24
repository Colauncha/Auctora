// useScreenModeStore.js

import { create } from "zustand";

const useSearchStore = create((set) => ({
  searchTerms: "",
  category: "",
  setSearchTerms: (searchTerms) => set({ searchTerms }),
  setCategory: (category) => set({ category }),
}));

export default useSearchStore;
