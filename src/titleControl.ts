import { Map, IControl } from 'maplibre-gl';
import MapTitle from './components/MapTitle.vue';
import { createApp } from 'vue'

export class titleControl implements IControl {
    private container: HTMLElement;
    constructor() {
        this.container = document.createElement('div');
        const titleVue = createApp(MapTitle);
        titleVue.mount(this.container);
    }

    onAdd(map: Map): HTMLElement {
        return this.container;
    }

    onRemove(map: Map): void {
    }
}
