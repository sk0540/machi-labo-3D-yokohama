<template>
    <div class="maplibregl-ctrl maplibregl-ctrl-group map-title">
        <img src="/ml3-y.svg" />
    </div>
</template>
<script setup lang="ts">
</script>
<style scoped>
.map-title {
    background: #fff;
    /*background: rgb(255, 255, 255, 0.9);*/
    display: flex;
    align-items: center;
    z-index: 9999;
}

.map-title {
    opacity: 1;
    /* width: 16rem; */
    height: 36px;
    padding: 0.25rem 2rem;
}

.map-title img {
    margin-left: auto;
    margin-right: auto;
}
</style>