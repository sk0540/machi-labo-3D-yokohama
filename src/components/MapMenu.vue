<template>

    <div v-if="mode == 'menu'" class="maplibregl-ctrl maplibregl-ctrl-group map-menu">
        <button @click="mode = 'legend'">凡例
        </button>
    </div>
    <div v-if="mode == 'legend'" class="maplibregl-ctrl maplibregl-ctrl-group map-legend">
        <div class="legend-header"><button @click="mode = 'menu'">＜</button>
            凡例</div>
        <MapLegend />
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
const mode = ref("menu");
import MapLegend from './MapLegend.vue';
</script>
<style scoped>
.map-menu {
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.map-menu button {
    font-size: 16px;
    width: 117px;
    height: 39px;
    font-weight: bold;
    color: #333;
}

.map-legend {
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: left;
    max-height: calc(100vh - 64px);
    width: 15rem;

}

.map-legend div+div {
    border-top: 1px solid #ddd;
}



.legend-header {
    font-weight: bold;
    display: flex;
    align-items: center;
    font-size: 15px;

}

.legend-header button {
    height: 39px;
    width: 39px;
}
</style>