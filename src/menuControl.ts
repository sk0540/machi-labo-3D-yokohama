//menuControl.ts
import { IControl } from 'maplibre-gl';
import MapGuideMenu from './components/MapGuideMenu.vue';
import MapLegendMenu from './components/MapLegendMenu.vue';
import { createApp } from 'vue'

//凡例表示ボタンとガイド表示ボタン
//VueコンポーネントをMapLibreのmenuControlに載せる手法

export class menuControl implements IControl {
    private container: HTMLElement;
    constructor(item: string) {
        this.container = document.createElement('div');
        if (item == 'guide') {
            const menuVue = createApp(MapGuideMenu);
            menuVue.mount(this.container);
        } else if (item == 'legend') {
            const menuVue = createApp(MapLegendMenu);
            menuVue.mount(this.container);
        }
    }

    onAdd(): HTMLElement {
        return this.container;
    }

    onRemove(): void {
    }
}
