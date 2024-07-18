<template>
    <div class="legend-container">
        <div class="legend" v-for="zoneNum in zoneNums" :key="zoneNum" :class="displayType(zoneNum)">
            <div class="legend-inner" @click="handleClick(zoneNum)">
                <MapZoneDesc :num="zoneNum" :display="displayType(zoneNum)" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { zoneNums } from '../data/zoneData';
import MapZoneDesc from './MapZoneDesc.vue';


const activeZoneNum = ref<number | null>(null);

const handleClick = (zoneNum: number) => {
    if (zoneNum === activeZoneNum.value) {
        activeZoneNum.value = null;
    } else {
        activeZoneNum.value = zoneNum;
    }
};
const displayType = (zoneNum: number) => {
    if (zoneNum === activeZoneNum.value) {
        return 'detail';
    }
    else {
        return 'title';
    }
};

</script>
<style scoped>
.legend-container {
    overflow-y: auto;
    color: #333;


}



.legend-container::-webkit-scrollbar {
    width: 0.75rem;
}

.legend-container::-webkit-scrollbar-thumb {
    background-color: #e0e0e0;
    border-radius: 0.375rem;
}

.legend-inner {
    padding: 0.625rem;
    z-index: 9999;
}



.title.legend:hover {
    background: rgba(0, 0, 0, 0.05);
}


.legend-container {

    background: linear-gradient(white 30%, transparent),
        linear-gradient(transparent, white 70%) 0 100%,
        linear-gradient(rgba(0, 32, 64, 0.2) -100%, transparent),
        linear-gradient(transparent, rgba(0, 32, 64, 0.2) 100%) 0 100%;

    background-size: 100% 60px, 100% 60px, 100% 30px, 100% 30px;
    background-repeat: no-repeat;
    background-color: white;
    background-attachment: local, local, scroll, scroll;
}
</style>