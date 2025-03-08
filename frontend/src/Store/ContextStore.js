import { create } from "zustand";

const ctaContext = create((set) => ({
  useCta: true,
  turnOff: () => set(() => ({useCta: false})),
  turnOn: () => set(() => ({useCta: true})),
}))

export { 
  ctaContext
}