<template>
    <div class="maplibregl-ctrl maplibregl-ctrl-group map-search">
        <input placeholder=" 場所を入力" v-model="searchInput" @click="flipMode" @keydown.enter="addressSearch">
        <button id="clear-button" @click="clearInput"><img :src="clear" /></button>
        <button id="search-button" @click="addressSearch"><img :src="search" /></button>
    </div>
    <div class="maplibregl-ctrl maplibregl-ctrl-group search-alert" v-if="store.mode == 'search' && searchAlert != ''">
        {{
            searchAlert }}
    </div>
    <div class="maplibregl-ctrl maplibregl-ctrl-group search-result" v-if="store.mode == 'search'">

        <div v-for="item in searchResults" class="search-item"
            @click="emitMoveto(item.properties.title, item.geometry.coordinates)">{{
                item.properties.title }}
        </div>
    </div>

</template>
<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue'
import { useMapStore } from '../store/mapStore';
import search from '../assets/search.svg';
import clear from '../assets/x.svg';
const store = useMapStore();

interface Feature {
    type: string; // Feature の種類 ("Feature")
    geometry: Geometry; // Feature のジオメトリ
    properties: FeatureProperties; // Feature のプロパティ
}

interface Geometry {
    type: string; // ジオメトリの種類 ("Point")
    coordinates: number[]; // ジオメトリ座標
}

interface FeatureProperties {
    addressCode: string; // 住所コード
    title: string; // 施設名
    dataSource: number; // データソース
}
const searchInput = ref('');
const searchResults: Ref<Feature[]> = ref([]);
const lastSearchTime = ref(0);
const searchAlert = ref('');

const addressSearchInternal = async () => {
    const url = `https://msearch.gsi.go.jp/address-search/AddressSearch?q=${searchInput.value}`;

    const response = await fetch(url);

    const data = await response.json();
    searchResults.value = data.filter((feature: Feature) => feature.properties.addressCode.startsWith('1410' || '1411'));
    if (searchResults.value.length == 0) {
        searchAlert.value = '該当する場所がありませんでした';
    } else {
        searchAlert.value = '';
    }
    lastSearchTime.value = Date.now();
};


const addressSearch = async () => {
    store.mode = 'search'
    if (Date.now() - lastSearchTime.value < 8000) {
        searchResults.value = [];
        searchAlert.value = 'しばらくお待ち下さい';
        setTimeout(() => {
            addressSearchInternal();
        }, 8000 - (Date.now() - lastSearchTime.value));
    } else {
        addressSearchInternal();
    }
};

const flipMode = () => {
    if (store.mode === 'search') {
        store.mode = 'menu'
        if (searchAlert.value === '該当する場所がありませんでした') {
            searchAlert.value = '';
        }
    }
    else {
        store.mode = 'search'
    }
}
const clearInput = () => {
    searchResults.value = []
    searchInput.value = ''

}

const emitMoveto = (title: string, coordinates: number[]) => {
    searchInput.value = title;
    emit('moveto', coordinates);
};


const emit = defineEmits<{
    (e: 'moveto', coord: number[]): void

}>();
</script>
<style scoped>
.map-search {
    background: #fff;
    display: flex;
    height: 38px;
    margin-top: 10px;
    border-radius: 4px;
}

.map-search input {
    flex-grow: 1;
    font-size: 19px;
    text-indent: 0.5em;
    width: 250px;
    padding: 1px 2px;
}

#clear-button {
    margin-left: -38px;
    width: 38px;
    height: 38px;
}

#clear-button img {
    width: 20px;
    height: 20px;
    margin-bottom: -4px;
    opacity: 0.5;
    height: 2
}

#search-button {
    width: 2.375rem;
    height: 2.375rem;
}


#search-button img {
    margin-bottom: -4px;
    opacity: 0.5;
}

.search-alert {
    padding: 10px 14px;
    margin-top: 8px;
}

.search-result {
    max-height: calc(100vh - 262px);
    max-height: calc(100dvh - 262px);
    overflow-y: scroll;
    width: 18rem;


}

.search-item {
    padding: 14px;

}

.search-item:hover {
    background: #eee;

}
</style>