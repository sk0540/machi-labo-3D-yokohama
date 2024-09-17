import { defineStore } from 'pinia';

export const useMapStore = defineStore('map', {
    state: () => ({
        mode: 'guide',//初期モード
    }),
    actions: {
        toggleMode(newMode: string) {
            this.mode = newMode;
        },
    },
});