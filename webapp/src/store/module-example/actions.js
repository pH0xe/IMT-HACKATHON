import { api } from "src/boot/axios";

const interval = 100;

export function fetchData(_, { id }) {
  let path = "/data?type=json";
  if (id != null) path += "&id=" + id;
  return api.get(path);
}

export function fetchCount() {
  let path = "/count";
  return api.get(path);
}



export function calculVitesse(_, { latlngs, times }) {
  const distances = []; // distance depuis le dernier point geographique
  distances.push(0);
  const R = 6378137;
  // for (let i = 1; i < latlngs.length - 1; i++) {
  //   const lat1 = degToRad(latlngs[i-1][0]);
  //   const lon1 = degToRad(latlngs[i-1][1]);
  //   const lat2 = degToRad(latlngs[i+1][0]);
  //   const lon2 = degToRad(latlngs[i+1][1]);

  //   const dlon = (lon2 - lon1) / 2;
  //   const dlat = (lat2 - lat1) / 2;
  //   console.log((Math.sin(dlat) * Math.sin(dlat)));
  //   const a = (Math.sin(dlat) * Math.sin(dlat)) + Math.cos(lat1) * Math.cos(lat2) * (Math.sin(dlon) * Math.sin(dlon));
  //   const d = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  //   distances.push(d * R);
  // }

  for (let i = 1; i < latlngs.length - 1; i++) {
    const lat1 = degToRad(latlngs[i-1][0]);
    const lon1 = degToRad(latlngs[i-1][1]);
    const lat2 = degToRad(latlngs[i+1][0]);
    const lon2 = degToRad(latlngs[i+1][1]);

    const dlon = (lon2 - lon1) / 2;
    const dlat = (lat2 - lat1) / 2;
    const a = (Math.sin(dlat) * Math.sin(dlat)) + Math.cos(lat1) * Math.cos(lat2) * (Math.sin(dlon) * Math.sin(dlon));
    const d = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    distances.push(d * R);
  }

  const vitesse = []; // vitesse moyenne entre le dernier point
  vitesse.push(0); // v = d/t;

  for (let index = 1; index < distances.length -1; index++) {
    const int = times[index+1] - times[index-1]
    vitesse.push((distances[index]/int) * 1000 * 3.6)
  }
  return vitesse;
}

const degToRad = (deg) => {
  return deg * (Math.PI / 180);
}
