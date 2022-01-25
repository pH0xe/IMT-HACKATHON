<template>
  <q-page class="flex flex-center">
    <l-map style="height:80vh; width: 90%" :options="{attributionControl: false}" :center="center" :zoom="zoom" :max-zoom="zoom">
      <l-tile-layer :url="url"></l-tile-layer>
      <l-polyline
        v-for="(polyline, index) in polylines"
        :lat-lngs="polyline.latlngs"
        :color="polyline.color"
        :key="index"
      ></l-polyline>
      <l-marker v-for="(marker, index) in markers" :lat-lng="marker.pos" :key="index" :name="marker.name"></l-marker>
    </l-map>
  </q-page>
</template>

<script>
import "leaflet/dist/leaflet.css"
import { LMap, LPolyline, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

export default {
  name: 'PageIndex',

  components: {
    LMap,
    LPolyline,
    LTileLayer,
    LMarker
  },

  props: {},
  data: () => ({
    url: 'https://a.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
    polylines: [],
    center: [47.282167, -1.520539],
    zoom: 20,
    markers: [
      {
        pos: [47.282155, -1.520595],
        name: 'Constant'
      },
      {
        pos: [47.282160008774675, -1.5205599927049434],
        name: 'Julien'
      },
    ]
  }),

  computed: {},

  methods: {},

  mounted() {
    this.$store.dispatch('gps/fetchPure').then(res => {
      this.polylines = res;
    })
  }
};
</script>
