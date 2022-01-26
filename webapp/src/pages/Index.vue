<template>
  <q-page class="row items-center">

    <l-map
      class="col-10 q-ml-md"
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
        :color="getColor(index)"
        :key="index"
      ></l-polyline>
    </l-map>

    <div class="flex flex-center column q-mx-md col-2 side">

      <div class="flex flex center column full-width">
        <q-select v-model="course" :options="courseOptions" label="Course" class="q-my-md" @update:model-value="onUpdate"/>
        <q-btn outline color="secondary" icon="download" label="Télécharger" @click="onDownload" :disable="!course"/>
      </div>

      <div class="flex flex-center column">
        <span>Temps:</span>
        <span>{{ (time/1000).toFixed(2) }} secondes</span>
        <q-slider
          v-model="time"
          :min="0"
          :max="getNbMilli || 100"
          :step="10"
          vertical
          reverse
          :disable="!course"
        ></q-slider>
      </div>
      <div class="full-width">
        <q-list bordered>
          <q-item
            v-for="(stat, index) in getVitesse()"
            :key="index"
          >
            <q-item-section avatar>
              <q-avatar :color="stat[2]" text-color="white" >
                {{ stat[1][0] }}
              </q-avatar>
            </q-item-section>

            <q-item-section>{{ stat[1] }}</q-item-section>
            

            <q-item-section>
              <q-item-label>Vitesse</q-item-label>
              <q-item-label caption lines="2">{{ stat[0].toFixed(2) }}km/h</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>



      </div>
      
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
    course: null,
    courseOptions: []
  }),

  computed: {
    getMin() {
      return parseInt(this.polylines[0]?.times[0])
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
      return parseInt(max);
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
      const i = poly.times.findIndex(t => t > search);
      return poly.latlngs.slice(0, i);
    },

    getVitesse() {
      const res = []
      if (this.polylines.length > 0) {
        this.polylines.forEach((poly, index) => {
          if (poly.times && poly.vitesse) {
            const search = this.time + this.getMin;
            const i = poly.times.findIndex(t => t >= search);
            let vit = poly.vitesse[i];
            if (!vit) vit = 0;
            res.push([vit, poly.name, this.getColor(index)])
          }
        })        
      }
      return res;
    },
    getColor(index) {
      const colors = ['red', 'blue', 'green', 'yellow', 'purple']
      return colors[index % 5]
    },

    onUpdate(value) {
      this.$store.dispatch('gps/fetchData', { id: parseInt(value) }).then(res => {
      this.polylines = res.data;
      this.polylines.forEach(polyline => {
        this.time = this.getNbMilli
        this.$store.dispatch('gps/calculVitesse', { latlngs: polyline.latlngs, times: polyline.times })
          .then(speeds => {
            polyline.vitesse = speeds;
          });
        });
      }).catch(err => console.log(err))
    },

    onDownload() {
      this.$store.dispatch('gps/fetchFile', { id: parseInt(this.course) }).then(res => {
        console.log(res);
      })
    }
  },

  mounted() {
    this.$store.dispatch('gps/fetchCount').then(res => {
        this.courseOptions = res.data;
    });
  }
};
</script>

<style scoped>
.q-slider {
  margin: 10px
}
.font-bold {
  font-weight: bold;
}
.side {
  height: 80vh;
  justify-content: space-around;
}
</style>
