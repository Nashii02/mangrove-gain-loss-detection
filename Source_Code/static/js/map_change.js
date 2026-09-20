/* ==========================================================
   Change Detection page — consecutive-year comparison map
   ========================================================== */

const mapChange = L.map('map-change').setView([16.375, 120.335], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(mapChange);
L.control.scale({ imperial: false }).addTo(mapChange);

const sel1 = document.getElementById('sel-y1');
const sel2 = document.getElementById('sel-y2');
let changeLayer = null;

/* Constrain "later year" to (earlier year + 1) — thesis: consecutive pairs only */
function syncSelects() {
  const y1 = +sel1.value;
  sel2.querySelectorAll('option').forEach(o => {
    o.disabled = +o.value !== y1 + 1;
  });
  if (+sel2.value !== y1 + 1) sel2.value = y1 + 1;
}
sel1.addEventListener('change', syncSelects);
syncSelects();

async function loadChange() {
  const y1 = sel1.value, y2 = sel2.value;
  ['card-gain', 'card-loss', 'card-stable', 'card-net']
    .forEach(id => document.getElementById(id).textContent = '…');

  try {
    const d = await fetchJSON(`/api/change/${y1}/${y2}`);
    if (changeLayer) mapChange.removeLayer(changeLayer);

    changeLayer = L.geoJSON(d.geojson, {
      style: styleByClass(),
      onEachFeature: (f, l) => {
        const c = f.properties.class;
        const label = c === 'gain' ? 'Mapped mangrove gain' : 'Mapped mangrove loss';
        const desc  = c === 'gain' ? 'non-mangrove → mangrove' : 'mangrove → non-mangrove';
        l.bindPopup(`<strong style="color:${c === 'gain' ? COLORS.gain : COLORS.loss}">${label}</strong><br>
                     ${desc}<br><small>${y1} → ${y2}</small>`);
      }
    }).addTo(mapChange);

    if (changeLayer.getBounds && changeLayer.getBounds().isValid()) {
      mapChange.fitBounds(changeLayer.getBounds(), { padding: [24, 24] });
    }

    document.getElementById('card-gain').textContent   = fmt(d.gain_ha) + ' ha';
    document.getElementById('card-loss').textContent   = fmt(d.loss_ha) + ' ha';
    document.getElementById('card-stable').textContent = fmt(d.stable_mangrove_ha) + ' ha';

    const net = (d.gain_ha ?? 0) - (d.loss_ha ?? 0);
    const netEl = document.getElementById('card-net');
    netEl.textContent = (net >= 0 ? '+' : '−') + fmt(Math.abs(net)) + ' ha';
    netEl.classList.toggle('text-forest', net >= 0);
    netEl.classList.toggle('text-loss',   net < 0);
  } catch (e) {
    showErr(document.getElementById('card-gain'), e);
  }
}

document.getElementById('btn-load').addEventListener('click', loadChange);
loadChange();   // initial: 2023 → 2024
