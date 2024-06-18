<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css'
import maplibreGl, { Map } from 'maplibre-gl'
import { onMounted } from 'vue'
import { useGsiTerrainSource } from 'maplibre-gl-gsi-terrain';
onMounted(() => {
    const gsiTerrainSource = useGsiTerrainSource(maplibreGl.addProtocol);

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
                            attribution: '国土地理院',
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
        center: [139.767125, 35.681236],
        zoom: 11,
        maxPitch: 68,
        minZoom: 9,
        maxZoom: 17.999
    });
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
        map.addSource('mvt', {
            type: 'vector',
            tiles: ['http://localhost:5173//mvt/{z}/{x}/{y}.pbf'],
            minzoom: 12,
            maxzoom: 16
        });
        map.addSource('test', {
            type: 'geojson',
            data: 'urf_6697_op.geojson'
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
            id: 'mvt',
            type: 'fill-extrusion',
            source: 'mvt',
            'source-layer': 'bldg',
            paint: {
                'fill-extrusion-color': [
                    'match',
                    ['get', 'function'],
                    1, '#57ae4c',
                    2, '#6ad08e',
                    3, '#8dcb49',
                    4, '#b1b700',
                    5, '#d8cb57',
                    6, '#ddb696',
                    7, '#db9b61',
                    9, '#d093ba',
                    10, '#e27096',
                    11, '#a5a5de',
                    12, '#5ecccc',
                    13, '#6296dd',
                    23, '#999999',
                    /* default color if 'function' value doesn't match any of the above */
                    '#cccccc'
                ],
                'fill-extrusion-height': ['get', 'measuredHeight'],
            },
        });
        map.addLayer({
            id: 'test',
            type: 'fill',
            source: 'test',
            'paint': {
                'fill-color': [
                    'match',
                    ['get', 'function'],
                    1, '#57ae4c',
                    2, '#6ad08e',
                    3, '#8dcb49',
                    4, '#b1b700',
                    5, '#d8cb57',
                    6, '#ddb696',
                    7, '#db9b61',
                    9, '#d093ba',
                    10, '#e27096',
                    11, '#a5a5de',
                    12, '#5ecccc',
                    13, '#6296dd',
                    23, '#999999',
                    /* default color if 'function' value doesn't match any of the above */
                    '#cccccc'
                ],
                'fill-opacity': 0.1,
            }
        });
        map.setTerrain({ source: 'terrain' });

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