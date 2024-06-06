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
    });
    map.on('load', () => {
        map.addSource('terrain', gsiTerrainSource);
        map.addSource('plateau', {
            type: 'vector',
            tiles: ['https://indigo-lab.github.io/plateau-tokyo23ku-building-mvt-2020/{z}/{x}/{y}.pbf'],
            minzoom: 10,
            maxzoom: 16,
            attribution:
                "データの出典：<a href='https://github.com/indigo-lab/plateau-tokyo23ku-building-mvt-2020'>plateau-tokyo23ku-building-mvt-2020 by indigo-lab</a> (<a href='https://www.mlit.go.jp/plateau/'>国土交通省 Project PLATEAU</a> のデータを加工して作成)",
        },);
        map.addLayer({
            id: 'bldg',
            type: 'fill-extrusion',
            source: 'plateau',
            'source-layer': 'bldg',
            minzoom: 10,
            maxzoom: 20,
            paint: {
                'fill-extrusion-color': '#797979',
                'fill-extrusion-height': ['get', 'measuredHeight'],
            },
        });

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
            paint: { 'background-color': '#fff' }
        }, 'hills');//タイルの境目に標高ノイズを発生させないための白背景

        map.setTerrain({ source: 'terrain' },);

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