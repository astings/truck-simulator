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
        <vl-geom-multi-point
          :coordinates="[
            [116.544921, 40.451633],
            [116.545264, 40.451649],
            [116.545865, 40.451698],
            [116.546144, 40.451551],
            [116.546337, 40.451274],
            [116.546788, 40.451143],
            [116.547324, 40.451078],
            [116.547539, 40.450996],
            [116.547839, 40.450719],
            [116.54844, 40.450506],
            [116.548933, 40.450604],
            [116.549448, 40.450604],
            [116.550242, 40.450376],
            [116.550865, 40.450163],
            [116.551702, 40.449935],
            [116.552581, 40.449576]
          ]"
        ></vl-geom-multi-point>
      </vl-feature>

      <vl-feature>
        <vl-geom-multi-line-string
          :coordinates="[
            [
              [116.544921, 40.451633],
              [116.545264, 40.451649],
              [116.545865, 40.451698],
              [116.546144, 40.451551],
              [116.546337, 40.451274],
              [116.546788, 40.451143],
              [116.547324, 40.451078]
            ],
            [
              [116.547839, 40.450719],
              [116.54844, 40.450506],
              [116.548933, 40.450604],
              [116.549448, 40.450604],
              [116.550242, 40.450376],
              [116.550865, 40.450163],
              [116.551702, 40.449935],
              [116.552581, 40.449576]
            ]
          ]"
        ></vl-geom-multi-line-string>
      </vl-feature>

      <vl-layer-tile id="osm">
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>
    </vl-map>
    <div style="padding: 20px">
      Zoom: {{ zoom }}<br />
      Center: {{ center }}<br />
      Rotation: {{ rotation }}<br />
      Info : {{ ans }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MyMap',
  data() {
    return {
      zoom: 15,
      center: [2.253921, 48.82759],
      rotation: 0,
      pos: [3, 48.82759],
      ans: null,
    };
  },
  methods: {
    call() {
      axios
        .get('http://127.0.0.1:5000')
        .then((response) => {
        // JSON responses are automatically parsed.
          this.ans = response.data;
        });
    },
    intervalFetchData() {
      setInterval(() => {
        this.call();
      }, 1000);
    },
  },
  created() {
    this.call();
  },
  mounted() {
    this.call();
    // Run the intervalFetchData function once to set the interval time for later refresh
    this.intervalFetchData();
  },
};
</script>
