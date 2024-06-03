<script setup lang="ts">
import 'maplibre-gl/dist/maplibre-gl.css'
import { Map } from 'maplibre-gl'
import { onMounted } from 'vue'
onMounted(() => {
    new Map({
        container: 'map',
        style: 'https://gsi-cyberjapan.github.io/gsivectortile-mapbox-gl-js/pale.json',
        center: [140.084556, 36.104611],
        zoom: 11,
    })
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