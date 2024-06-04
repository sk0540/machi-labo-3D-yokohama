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