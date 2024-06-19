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
        minZoom: 9,
        maxZoom: 17.999
    });

    const colors = {
        1: '#57ae4c',
        2: '#6ad08e',
        3: '#8dcb49',
        4: '#b1b700',
        5: '#d8cb57',
        6: '#ddb696',
        7: '#db9b61',
        9: '#d093ba',
        10: '#e27096',
        11: '#a5a5de',
        12: '#5ecccc',
        13: '#6296dd',
        23: '#999999',
        default: '#cccccc'
    };

    const descs: { [key: number]: string } = {
        1: "第一種低層住居専用地域",
        2: "第二種低層住居専用地域",
        3: "第一種中高層住居専用地域",
        4: "第二種中高層住居専用地域",
        5: "第一種住居地域",
        6: "第二種住居地域",
        7: "準住居地域",
        9: "近隣商業地域",
        10: "商業地域",
        11: "準工業地域",
        12: "工業地域",
        13: "工業専用地域",
        23: "市街化調整区域"
    }
    map.on('load', () => {
        map.addSource('terrain', gsiTerrainSource);
        /*map.addSource('plateau', {
            type: 'vector',
            tiles: ['https://indigo-lab.github.io/plateau-tokyo23ku-building-mvt-2020/{z}/{x}/{y}.pbf'],
            minzoom: 10,
            maxzoom: 16,
            attribution:
                "データの出典：<a href='https://github.com/indigo-lab/plateau-tokyo23ku-building-mvt-2020'>plateau-tokyo23ku-building-mvt-2020 by indigo-lab</a> (<a href='https://www.mlit.go.jp/plateau/'>国土交通省 Project PLATEAU</a> のデータを加工して作成)",
        },);*/
        map.addSource('buildings', {
            type: 'vector',
            tiles: ['http://localhost:5173//mvt/{z}/{x}/{y}.pbf'],
            minzoom: 12,
            maxzoom: 16
        });
        map.addSource('zones', {
            type: 'geojson',
            data: 'urf_6697_op.geojson'
        });
        /*map.addLayer({
            id: 'bldg',
            type: 'fill-extrusion',
            source: 'plateau',
            'source-layer': 'bldg',
            minzoom: 10,
            maxzoom: 18,
            paint: {
                'fill-extrusion-color': '#797979',
                'fill-extrusion-height': ['get', 'measuredHeight'],
            },
        });*/

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
            minzoom: 9,
            maxzoom: 18,
            paint: { 'background-color': '#fff' }
        }, 'hills');//タイルの境目に標高ノイズを発生させないための白背景
        map.addLayer({
            id: 'buildings',
            type: 'fill-extrusion',
            source: 'buildings',
            'source-layer': 'bldg',
            paint: {
                'fill-extrusion-color': [
                    'match',
                    ['get', 'function'],
                    1, colors[1],
                    2, colors[2],
                    3, colors[3],
                    4, colors[4],
                    5, colors[5],
                    6, colors[6],
                    7, colors[7],
                    9, colors[9],
                    10, colors[10],
                    11, colors[11],
                    12, colors[12],
                    13, colors[13],
                    23, colors[23],
                    colors.default
                ],
                'fill-extrusion-height': ['get', 'measuredHeight'],
            },
        });
        map.addLayer({
            id: 'zones',
            type: 'fill',
            source: 'zones',
            'paint': {
                'fill-color': [
                    'match',
                    ['get', 'function'],
                    1, colors[1],
                    2, colors[2],
                    3, colors[3],
                    4, colors[4],
                    5, colors[5],
                    6, colors[6],
                    7, colors[7],
                    9, colors[9],
                    10, colors[10],
                    11, colors[11],
                    12, colors[12],
                    13, colors[13],
                    23, colors[23],
                    colors.default
                ],
                'fill-opacity': 0.1,
            }
        });
        map.setTerrain({ source: 'terrain' });


        // Create a popup, but don't add it to the map yet.
        const popup = new maplibreGl.Popup({
            closeButton: false,
            closeOnClick: false
        });
        map.on('mousemove', 'zones', (e) => {
            if (e.features) {
                const zoneNum = e.features[0].properties.function;
                map.getCanvas().style.cursor = 'pointer';
                popup.setLngLat(e.lngLat).setHTML(descs[zoneNum]).addTo(map);
            }
        });
        map.on('mouseleave', 'zones', () => {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });

        /*map.addControl(
            new maplibreGl.TerrainControl({
                source: 'terrain'
            })
        );*/
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