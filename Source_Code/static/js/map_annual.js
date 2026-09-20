/* ==========================================================
   Annual Maps page — year switcher + mangrove GeoJSON layer
   ========================================================== */

const mapAnnual = L.map('map-annual').setView([16.375, 120.335], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(mapAnnual);
L.control.scale({ imperial: false }).addTo(mapAnnual);

let annualLayer = null;

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

    document.getElementById('sel-area').textContent = fmt(d.area_ha) + ' ha';
    document.getElementById('sel-px').textContent =
      d.pixels != null ? `${d.pixels.toLocaleString()} pixels (10 m grid)` : '';
  } catch (e) {
    showErr(document.getElementById('sel-area'), e);
  }
}

document.querySelectorAll('.year-btn')
  .forEach(b => b.addEventListener('click', () => loadYear(b.dataset.year)));

loadYear(2024);   // default view — most recent observation year
