import { api } from "src/boot/axios";

const interval = 1000;

export function fetchData(_, { id }) {
  let path = "/data?type=json";
  if (id != null) path += "&id=" + id;
  return api.get(path);
}



const calculVitesse = (latlngs) => {
  const distances = []; // distance depuis le dernier point geographique
  distances.push(0);
  const R = 6378137;
  for (let i = 1; i < latlngs.length; i++) {
    const lat1 = degToRad(latlngs[0][0]);
    const lon1 = degToRad(latlngs[0][1]);
    const lat2 = degToRad(latlngs[1][0]);
    const lon2 = degToRad(latlngs[1][1]);

    const dlon = (lon2 - lon1) / 2;
    const dlat = (lat2 - lat1) / 2;
    const a = (Math.sin(dlat) * Math.sin(dlat)) + Math.cos(lat1) * Math.cos(lat2) * (Math.sin(dlon) * Math.sin(dlon));
    const d = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    distances.push(d * R);
  }

  const vitesse = []; // vitesse moyenne entre le dernier point
  vitesse.push(0); // v = d/t;
  distances.forEach(d => vitesse.push(d/interval))
  return vitesse;
}

const degToRad = (deg) => {
  return deg * (Math.PI / 180);
}
