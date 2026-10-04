/* ==========================================================
   Annual Maps page — year switcher + mangrove GeoJSON layer
   ========================================================== */

const mapAnnual = L.map('map-annual').setView([16.376, 120.332], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(mapAnnual);
L.control.scale({ imperial: false }).addTo(mapAnnual);

let annualLayer = null;
let roiAnnualLayer = null;

// Overlay official study area boundary
fetchJSON('/api/meta').then(meta => {
  if (meta && meta.study_area && meta.study_area.geojson) {
    roiAnnualLayer = L.geoJSON(meta.study_area.geojson, {
      style: { color: '#1B4332', weight: 2.5, fillOpacity: 0.05, dashArray: '4, 4' }
    }).addTo(mapAnnual);
    roiAnnualLayer.bindPopup('<strong>Brgy. Dulao Shoreline</strong><br>Official Study Area Boundary (2019–2024)<br><small>Aringay, La Union</small>');
  }
}).catch(() => {});

async function loadYear(year) {
  // Button active state
  document.querySelectorAll('.year-btn').forEach(b => {
    const on = b.dataset.year === String(year);
    b.classList.toggle('btn-forest', on);
    b.classList.toggle('btn-outline-forest', !on);
  });

  document.getElementById('sel-year').textContent = year;
  document.getElementById('sel-area').innerHTML =
    '<span class="placeholder-glow"><span class="placeholder col-8"></span></span>';
  document.getElementById('sel-px').innerHTML = '&nbsp;';

  try {
    const d = await fetchJSON(`/api/annual/${year}`);
    if (annualLayer) mapAnnual.removeLayer(annualLayer);

    annualLayer = L.geoJSON(d.geojson, {
      style: styleByClass(),
      onEachFeature: (f, l) =>
        l.bindPopup(`<strong>Mapped mangrove</strong><br>Year: ${year}`)
    }).addTo(mapAnnual);

    if (annualLayer.getBounds && annualLayer.getBounds().isValid()) {
      mapAnnual.fitBounds(annualLayer.getBounds(), { padding: [24, 24] });
    }

    document.getElementById('sel-area').textContent = fmt(d.area_ha) + ' hectares';
    document.getElementById('sel-px').textContent =
      d.pixels != null ? `${d.pixels.toLocaleString()} pixels (10-meter grid)` : '';
  } catch (e) {
    showErr(document.getElementById('sel-area'), e);
  }
}

document.querySelectorAll('.year-btn')
  .forEach(b => b.addEventListener('click', () => loadYear(b.dataset.year)));

loadYear(2024);   // default view — most recent observation year
