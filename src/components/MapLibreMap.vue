<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css'
import maplibreGl, { Map, Popup, DataDrivenPropertyValueSpecification, addProtocol, AttributionControl } from 'maplibre-gl'
import { PMTiles, Protocol } from "pmtiles";
import { onMounted, createApp, App } from 'vue';
import MapZoneDesc from './MapZoneDesc.vue';
import { useGsiTerrainSource } from 'maplibre-gl-gsi-terrain';
import { menuControl } from '../menuControl';
import { titleControl } from '../titleControl';
import { zoneColors } from '../data/zoneData';

onMounted(() => {
    const gsiTerrainSource = useGsiTerrainSource(addProtocol);
    const protocol = new Protocol();
    addProtocol("pmtiles", protocol.tile);


    const map = new Map({
        container: 'map',
        style: 'https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/pale.json',
        /*
                {
                    version: 8,
                    sources: {
                        gsipale: {
                            type: 'raster',
                            tiles: [
                                'https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
                            ],
                            attribution: '地理院地図Vector（仮称）',
                        },
                        gsidem: gsiTerrainSource,
                    },
                    layers: [
                        {
                            id: 'gsipale',
                            type: 'raster',
                            source: 'gsipale',
                        },
                    ],
                    terrain: {
                        source: 'gsidem',
                        exaggeration: 1.2,
                    },
                },*/
        center: [139.62, 35.43],
        zoom: 12.3,
        pitch: 43,
        maxPitch: 68,
        maxBounds: [[136, 33], [143, 37]],
        minZoom: 9,
        maxZoom: 17.999,

    });

    const paintStatus: DataDrivenPropertyValueSpecification<string> = [
        'match',
        ['get', 'function'],
        1, zoneColors[1],
        2, zoneColors[2],
        3, zoneColors[3],
        4, zoneColors[4],
        5, zoneColors[5],
        6, zoneColors[6],
        7, zoneColors[7],
        9, zoneColors[9],
        10, zoneColors[10],
        11, zoneColors[11],
        12, zoneColors[12],
        13, zoneColors[13],
        23, zoneColors[23],
        zoneColors[0]
    ];


    map.on('load', () => {
        map.addSource('terrain', gsiTerrainSource);
        /*map.addSource('plateau', {
            type: 'vector',
            tiles: ['https://indigo-lab.github.io/plateau-tokyo23ku-building-mvt-2020/{z}/{x}/{y}.pbf'],
            minzoom: 10,
            maxzoom: 16,
            attribution:
                "データの出典：<a href='https://github.com/indigo-lab/plateau-tokyo23ku-building-mvt-2020'>plateau-tokyo23ku-building-mvt-2020 by indigo-lab</a> (<a href='https://www.mlit.go.jp/plateau/'>国土交通省 Project PLATEAU</a> のデータを加工して作成)",
        },);*/


        map.addSource('yokohama_urf', {
            type: 'vector',
            url: 'pmtiles://yokohama_urf.pmtiles',
            attribution: "<a href='https://www.mlit.go.jp/plateau/'>国土交通省 Project PLATEAU</a> のデータを加工して作成",
            minzoom: 10,
            maxzoom: 14,
        });
        /*map.addLayer({
            id: 'bldg',
            type: 'fill-extrusion',
            source: 'plateau',
            'source-layer': 'bldg',
            minzoom: 10,
            maxzoom: 18,
            paint: {
                'fill-extrusion-color': '#797979',
                'fill-extrusion-height': ['get', 'measuredHeight'],
            },
        });*/

        map.addLayer({
            id: 'hills',
            type: 'hillshade',
            source: 'terrain',
        },
            'gsibv-vectortile-layer-1539'//国土地理院タイルの最背面レイヤの更に背面に追加
        );
        map.addLayer({
            id: 'background',
            type: 'background',
            minzoom: 9,
            maxzoom: 18,
            paint: { 'background-color': '#fff' }
        }, 'hills');//タイルの境目に標高ノイズを発生させないための白背景
        map.addLayer({
            id: 'buildings',
            type: 'fill-extrusion',
            source: 'yokohama_urf',
            'source-layer': 'bldg',
            paint: {
                'fill-extrusion-color': paintStatus,
                'fill-extrusion-height':
                    ['get', 'measuredHeight']
                ,
            },
        }, 'gsibv-vectortile-layer-2035'//国土地理院タイルの地図記号のすぐ下bの重なり位置に)
        );
        map.addLayer({
            id: 'zones',
            type: 'fill',
            source: 'yokohama_urf',
            'source-layer': 'urf_6697_op',
            'paint': {
                'fill-color': paintStatus,
                'fill-opacity': [
                    "step",
                    ["zoom"],
                    0.3,
                    12,
                    0.2,
                    14,
                    0.1
                ],
            }
        }, 'gsibv-vectortile-layer-1604');
        map.setTerrain({ source: 'terrain' });

        //地理院paleスタイルの調整
        map.setLayoutProperty('gsibv-vectortile-layer-2037', "text-size", { "stops": [[9, 14], [11, 17]] });
        map.setPaintProperty('gsibv-vectortile-layer-2037', 'text-halo-width', 2);
        map.setPaintProperty('gsibv-vectortile-layer-2203', 'text-halo-width', 1.5);
        map.setPaintProperty('gsibv-vectortile-layer-2273', 'text-halo-width', 1.5);
        map.setPaintProperty('gsibv-vectortile-layer-2278', 'text-halo-width', 2);

        //追加するポップアップを宣言
        const hoverPopup = new Popup({
            closeButton: false,
            closeOnClick: false
        });
        let hoverPopupVue: App;
        let zoneNum: number;
        map.on('mousemove', 'zones', (e) => {
            if (e.features) {
                if (zoneNum != e.features[0].properties.function) {
                    if (hoverPopupVue) {
                        hoverPopupVue.unmount();
                    }
                    zoneNum = e.features[0].properties.function;
                    const popupNode = document.createElement('div');
                    hoverPopupVue = createApp(MapZoneDesc, {
                        num: zoneNum, display: 'title'
                    });
                    hoverPopupVue.mount(popupNode);
                    hoverPopup.setDOMContent(popupNode);
                    map.getCanvas().style.cursor = 'pointer';
                }
                hoverPopup.setLngLat(e.lngLat).addTo(map);
            }
        });

        map.on('mouseleave', 'zones', () => {
            map.getCanvas().style.cursor = '';
            hoverPopup.remove();
            hoverPopupVue.unmount();
            zoneNum = 0;
        });
        const clickPopup = new Popup({ closeOnClick: false });
        let clickPopupVue: App;
        map.on('click', 'zones', (e) => {
            if (clickPopupVue) {
                clickPopupVue.unmount();
            }
            if (e.features) {
                const zoneNum = e.features[0].properties.function;
                const popupNode = document.createElement('div');
                clickPopupVue = createApp(MapZoneDesc, {
                    num: zoneNum, display: 'detail'
                });
                clickPopupVue.mount(popupNode);
                clickPopup.setDOMContent(popupNode);
                map.getCanvas().style.cursor = 'pointer';
                clickPopup.setLngLat(e.lngLat).addTo(map);
            }
        });


        map.addControl(new maplibreGl.NavigationControl());
        map.addControl(new maplibreGl.ScaleControl());
        map.addControl(new titleControl(), 'top-left');
        map.addControl(new menuControl(), 'top-left');
        //map.addControl(new legendControl(), 'top-left');
        /*map.addControl(
            new maplibreGl.TerrainControl({
                source: 'terrain'
            })
        );*/


    });
});

</script>
<template>
    <div id="map"></div>
</template>
<style scoped>
#map {
    height: 100vh;
}
</style>