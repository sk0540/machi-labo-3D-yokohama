<template>
    <div v-if="store.mode != 'legend'" class="maplibregl-ctrl maplibregl-ctrl-group map-menu">
        <button @click="store.mode = 'legend'">凡例
        </button>
    </div>
    <div v-show="store.mode == 'legend'" class="maplibregl-ctrl maplibregl-ctrl-group map-legend">
        <div class="legend-header">
            凡例<button @click="store.mode = 'menu'"><img class="close-button" :src="close" /></button></div>
        <MapLegend />
    </div>
</template>
<script setup lang="ts">
import { useMapStore } from '../store/mapStore';
import MapLegend from './MapLegend.vue';
import close from '../assets/x.svg';
const store = useMapStore();
</script>
<style scoped>
.map-menu {
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.map-menu button {
    font-size: 17px;
    width: 120px;
    height: 33px;
    font-weight: bold;
    color: #333;
    position: relative;
    top: 1px;
}

.map-legend {
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: left;
    max-height: calc(100vh - 227px);
    max-height: calc(100dvh - 227px);
    width: 15rem;
    margin-bottom: 13px;
}

@media screen and (max-height: 24rem) {
    .map-legend {
        margin-left: 308px;
        margin-bottom: -84px;
        max-height: calc(100vh - 24px);
        max-height: calc(100dvh - 24px);
    }
}

.map-legend div+div {
    border-top: 1px solid #ddd;
}



.legend-header {
    font-weight: bold;
    display: flex;
    align-items: center;
    font-size: 17px;

    padding-top: 1px;
    padding-left: 13px;
    margin-bottom: -1px;

}

.legend-header button {
    height: 37px;
    width: 37px;
    margin-left: auto;
}

.legend-header button img {
    height: 20px;
    width: 20px;
    opacity: 0.6;
}
</style>