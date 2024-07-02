import { Map, IControl } from 'maplibre-gl';
import MapMenu from './components/MapMenu.vue';
import { createApp } from 'vue'

export class menuControl implements IControl {
    private container: HTMLElement;
    constructor() {
        this.container = document.createElement('div');
        const menuVue = createApp(MapMenu);
        menuVue.mount(this.container);
    }

    onAdd(map: Map): HTMLElement {
        return this.container;
    }

    onRemove(map: Map): void {
    }
}
