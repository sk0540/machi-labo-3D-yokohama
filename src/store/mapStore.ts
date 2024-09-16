import { defineStore } from 'pinia';

export const useMapStore = defineStore('map', {
    state: () => ({
        mode: 'menu',
    }),
    actions: {
        toggleMode(newMode: string) {
            this.mode = newMode;
        },
    },
});