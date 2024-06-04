<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css'
import maplibreGl, { Map } from 'maplibre-gl'
import { onMounted } from 'vue'
import { useGsiTerrainSource } from 'maplibre-gl-gsi-terrain';
onMounted(() => {
    const gsiTerrainSource = useGsiTerrainSource(maplibreGl.addProtocol);

    new Map({
        container: 'map',
        maxPitch: 67,
        style: {
            version: 8,
            sources: {
                gsipale: {
                    type: 'raster',
                    tiles: [
                        'https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
                    ],
                    attribution: '地理院タイル',
                },
                terrain: gsiTerrainSource,
            },
            layers: [
                {
                    id: 'gsipale',
                    type: 'raster',
                    source: 'gsipale',
                },
            ],
            terrain: {
                source: 'terrain',
                exaggeration: 1.2,
            },
        },
        center: [139.767125, 35.681236],
        zoom: 11,
    });

})

</script>
<template>
    <div id="map"></div>
</template>
<style scoped>
#map {
    height: 100vh;
}
</style>