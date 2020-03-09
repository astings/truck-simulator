<template>
  <div>
    <vl-map
      :load-tiles-while-animating="true"
      :load-tiles-while-interacting="true"
      data-projection="EPSG:4326"
      style="height: 500px"
    >
      <vl-view
        :zoom.sync="zoom"
        :center.sync="center"
        :rotation.sync="rotation"
      ></vl-view>

      <vl-feature id="point" :properties="{ prop: 'value', prop2: 'value' }">
        <vl-geom-point :coordinates="ans"></vl-geom-point>
      </vl-feature>

      <vl-feature>
              <vl-geom-multi-point :coordinates="trucks">
              </vl-geom-multi-point>
      </vl-feature>

      <vl-layer-tile id="osm">
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>
    </vl-map>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MyMap',
  data() {
    return {
      zoom: 12,
      center: [2.329, 48.859],
      rotation: 0,
      ans: [0, 0],
      trucks: [0, 0],
    };
  },
  methods: {
    call() {
      axios
        .get('http://localhost:5000')
        .then((response) => {
          this.ans = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    call_trucks() {
      axios
        .get('http://localhost:5000/trucks')
        .then((response) => {
          this.trucks = response.data;
          // eslint-disable-next-line no-console
          console.log(this.trucks);
        })
        .catch((err) => {
          // eslint-disable-next-line no-console
          console.log(err);
        });
    },
    intervalFetchData() {
      setInterval(() => {
        this.call();
        this.call_trucks();
      }, 1000);
    },
  },
  async created() {
    this.call();
    this.call_trucks();
  },
  mounted() {
    this.call();
    this.call_trucks();
    this.intervalFetchData();
  },
};
</script>
