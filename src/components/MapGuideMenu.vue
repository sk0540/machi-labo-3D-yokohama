<template>

    <div class="maplibregl-ctrl maplibregl-ctrl-group " id="guide-menu">
        <button>ガイド
        </button>
    </div>
</template>
<script setup lang="ts">

</script>
<style scoped>
#guide-menu {
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
}

#guide-menu button {
    font-size: 17px;
    width: 120px;
    height: 33px;
    font-weight: bold;
    color: #333;
    position: relative;
    top: 1px;
}
</style>