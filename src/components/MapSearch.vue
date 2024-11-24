<template>
    <div class="maplibregl-ctrl maplibregl-ctrl-group map-search">
        <input placeholder="場所を検索" v-model="searchInput" @click="flipMode" @keydown.enter="addressSearchByEnterKey">
        <button id="clear-button" @click="clearInput" v-if="searchInput != ''"><img :src="clear" /></button>
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
    <div v-if="store.mode == 'menu' && searchInput == ''" class="search-guide">横浜市内の地名を検索できます</div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import type { Ref } from 'vue'
import { useMapStore } from '../store/mapStore';
import search from '../assets/search.svg';
import clear from '../assets/x.svg';
const store = useMapStore();

interface Feature {
    type: string;
    geometry: Geometry;
    properties: FeatureProperties;
}

interface Geometry {
    type: string;
    coordinates: number[];
}

interface FeatureProperties {
    addressCode: string;
    title: string;
    dataSource: number;
}
const searchInput = ref('');
const searchResults: Ref<Feature[]> = ref([]);
const lastSearchTime = ref(0);
const searchAlert = ref('');

const addressSearchInternal = async () => {
    const url = `https://msearch.gsi.go.jp/address-search/AddressSearch?q=${searchInput.value}`;

    const response = await fetch(url);

    const data = await response.json();
    searchResults.value = data.filter((feature: Feature) => feature.properties.addressCode.startsWith('1410') || feature.properties.addressCode.startsWith('1411'));
    if (searchResults.value.length == 0) {
        searchAlert.value = '該当する場所がありませんでした';
    } else {
        searchAlert.value = '';
    }
    lastSearchTime.value = Date.now();
};


const addressSearchByEnterKey = (event: KeyboardEvent) => {
    if (event.keyCode === 13) {
        addressSearch();
    }
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
    width: 208px;
    padding: 1px 2px;
    padding-right: 36px;
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
    opacity: 0.6;
    height: 2
}

#search-button {
    width: 2.375rem;
    height: 2.375rem;
}


#search-button img {
    margin-bottom: -4px;
    opacity: 0.6;
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



.search-guide {

    text-align: center;
    background: #fff;
    border: #666 1px solid;
    border-radius: 1.5rem;
    margin-top: 1.125rem;
    padding-top: 0.575rem;
    padding-bottom: 0.525rem;
    filter: drop-shadow(5px 5px 3px rgba(0, 0, 0, .2));
}

.search-guide:before {
    content: "";
    position: absolute;
    background: #666;
    left: 50%;
    width: 20px;
    height: 18px;
    clip-path: polygon(0 100%, 50% 0, 100% 100%);
    transform: translateX(-50%) translateY(-150%);

}

.search-guide:after {
    content: "";
    position: absolute;
    background: #fff;
    left: 50%;
    width: 19px;
    height: 17px;
    clip-path: polygon(0 100%, 50% 0, 100% 100%);
    transform: translateX(-50%) translateY(-150%);


}

.search-item {
    padding: 14px;

}

.search-item:hover {
    background: #eee;

}
</style>