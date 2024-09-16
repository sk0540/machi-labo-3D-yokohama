<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css'
import maplibreGl, { Map, Popup, DataDrivenPropertyValueSpecification, addProtocol } from 'maplibre-gl'

import { useGsiTerrainSource } from 'maplibre-gl-gsi-terrain';
import { Protocol } from "pmtiles";

import { onMounted, createApp, App } from 'vue';

import MapZoneDesc from './MapZoneDesc.vue';
import MapGuide from './MapGuide.vue';
import MapTitle from './MapTitle.vue';
import MapSearch from './MapSearch.vue';

import { menuControl } from '../menuControl';
import { zoneColors } from '../data/zoneData';
import { useMapStore } from '../store/mapStore';

const store = useMapStore();//Piniaデータストア
let map: Map;//場所検索からEmitで呼び出すため変数として定義

onMounted(() => {
    //maplibre-gl-gsi-terrainライブラリによる変換プロトコル
    const gsiTerrainSource = useGsiTerrainSource(addProtocol);

    //pmtilesライブラリによる変換プロトコル
    const protocol = new Protocol();
    addProtocol("pmtiles", protocol.tile);




    map = new Map({
        container: 'map',
        style: 'https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/pale.json', // 地理院paleベクトルタイル
        center: [139.625, 35.433], // 初期：横浜中心市街を写す
        zoom: 12.3, // 初期：建物ポリゴン（z12~）が映る最小ズーム
        pitch: 43,  // 初期：3Dとして見せる
        maxPitch: 68, //遠くの地物が空白で映らないのを傾き制限で見せなくする
        maxBounds: [[136, 33], [143, 37]], // 横浜から離れすぎないよう制限
        minZoom: 9,      // 横浜全体が映るズームレベル
        maxZoom: 17.999, // z18以上は地理院地図が映らなくなるので制限

    });

    //建物ポリゴンの色を取得しておく
    const paintStatus: DataDrivenPropertyValueSpecification<string> = [
        'match',
        ['get', 'function'], //建物ポリゴンのfunctionプロパティ
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
        //標高DEM
        map.addSource('terrain', gsiTerrainSource);

        //建物ポリゴンと用途地域領域ポリゴンをまとめたPMTiles
        map.addSource('yokohama_urf', {
            type: 'vector',
            url: 'pmtiles://yokohama_urf.pmtiles',
            attribution: "<a href='https://www.mlit.go.jp/plateau/'>国土交通省 Project PLATEAU</a> のデータを加工して作成",
            minzoom: 10,
            maxzoom: 14,//PMTilesはz15~の収録がなく非表示になるのを回避
        });

        map.addLayer({
            id: 'hills',
            type: 'hillshade',//3D起伏
            source: 'terrain',
        },
            'gsibv-vectortile-layer-1539'//国土地理院タイルの最背面レイヤの更に背面に追加
        );

        //タイルの境目に標高ノイズを発生させないための白背景
        map.addLayer({
            id: 'background',
            type: 'background',
            minzoom: 9,
            maxzoom: 18,
            paint: { 'background-color': '#fff' }
        }, 'hills');
        map.addLayer({
            id: 'buildings',
            type: 'fill-extrusion',//建物を押し出し3Dで表示
            source: 'yokohama_urf',
            'source-layer': 'bldg',
            paint: {
                'fill-extrusion-color': paintStatus,
                'fill-extrusion-height':
                    ['get', 'measuredHeight']
                ,
            },
        }, 'gsibv-vectortile-layer-2035'//国土地理院タイルの地図記号のすぐ下の重なり位置に
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
                    0.1//ズームレベルで透明度を変化させて自然な表示に
                ],
            }
        }, 'gsibv-vectortile-layer-1604'//国土地理院タイルの水域のすぐ上の重なり位置に
        );
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
        let hoverPopupVue: App;//VueAppの変数
        let zoneNum: number;
        map.on('mousemove', 'zones', (e) => {
            if (e.features) {
                if (zoneNum != e.features[0].properties.function) {
                    //VueAppが無限増殖するのを防ぐ
                    if (hoverPopupVue) {
                        hoverPopupVue.unmount();
                    }
                    zoneNum = e.features[0].properties.function;//マウス位置の用途地域タイプを取得
                    const popupNode = document.createElement('div');
                    hoverPopupVue = createApp(MapZoneDesc, {
                        num: zoneNum, display: 'title',//用途地域名だけの表示
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
            if (hoverPopupVue) {
                hoverPopup.remove();
                hoverPopupVue.unmount();
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

        //コントロールボタンの追加
        map.addControl(new maplibreGl.ScaleControl(),);
        map.addControl(new maplibreGl.NavigationControl(), 'bottom-right');
        // map.addControl(new maplibreGl.GeolocateControl({}), 'bottom-right');
        map.addControl(new menuControl('guide'), 'bottom-left');
        map.addControl(new menuControl('legend'), 'bottom-left');
    });


});
const moveToResult = (coord: number[]) => {
    map.jumpTo({ center: [coord[0], coord[1]], zoom: 16 });
    store.mode = 'menu';
};
</script>
<template>
    <div id="map"></div>
    <div class="title-container">
        <MapTitle />
        <MapSearch @moveto="moveToResult" />
    </div>
    <MapGuide />
</template>
<style scoped>
#map {
    height: 100vh;
    height: 100dvh;
}

.title-container {
    position: fixed;
    top: 10px;
    left: 10px;
    width: 18rem;
    z-index: 9999;
}


@media screen and (max-width: 600px) {
    .title-container {

        left: -9rem;
        transform: translate(50vw, 0);
    }
}
</style>