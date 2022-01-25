<template>
  <q-page class="row items-center">

    <l-map
      class="col-11 q-mx-md"
      style="height:90vh; flex-grow: 2; width: auto"
      :options="{attributionControl: false}"
      :center="center"
      :zoom="zoom"
      :max-zoom="zoom"
    >
      <l-tile-layer :url="url"></l-tile-layer>
      <l-polyline
        v-for="(polyline, index) in polylines"
        :lat-lngs="getLat(index)"
        :color="polyline.color"
        :key="index"
      ></l-polyline>
    </l-map>

    <div class="flex flex-center column q-mx-md col-1">
      <span>Temps:</span>
      <span>{{ time/1000 }} secondes</span>
      <q-slider
        v-model="time"
        :min="0"
        :max="getNbMilli"
        :step="1000"
        vertical
        reverse
      ></q-slider>
      <span>Vitesse:</span>
      <span>{{ getVitesse() }} </span>
    </div>


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
    LTileLayer
  },

  props: {},
  data: () => ({
    url: 'https://a.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
    polylines: [],
    center: [47.282167, -1.520539],
    zoom: 20,
    time: 0,
  }),

  computed: {
    getMin() {
      return this.polylines[0]?.times[0]
    },

    getMax() {
      let max = null;
      this.polylines.forEach(p => {
        if (max === null) {
          max = p.times[p.times.length-1];
        } else {
          if (p.times[p.times.length-1] > max) {
            max = p.times[p.times.length-1];
          }
        }
      });
      return max;
    },

    getNbSecond() {
      return (this.getMax - this.getMin) / 1000;
    },

    getNbMilli() {
      return (this.getMax - this.getMin);
    },
  },

  methods: {
    getLat(index) {
      const poly = this.polylines[index];
      const search = this.time + this.getMin;
      const i = poly.times.filter(t => t <= search);
      return poly.latlngs.slice(0, i.length);
    },

    getVitesse() {
      if (this.polylines.length > 0) {
        const poly = this.polylines[1];
        const search = this.time + this.getMin;
        const i = poly.times.findIndex(t => t === search);
        console.log(poly.vitesse);
        return poly.vitesse[i];
      }
      return 0;
    }
  },

  mounted() {
    this.$store.dispatch('gps/fetchPure').then(res => {
      this.polylines = res;
      this.time = this.getNbMilli;
    })
  }
};
</script>

<style scoped>
.q-slider {
  margin: 10px
}
</style>
