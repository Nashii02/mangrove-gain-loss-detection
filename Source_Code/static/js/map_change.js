/* ==========================================================
   Change Detection page — consecutive-year comparison map
   ========================================================== */

const mapChange = L.map('map-change').setView([16.376, 120.332], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(mapChange);
L.control.scale({ imperial: false }).addTo(mapChange);

const sel1 = document.getElementById('sel-y1');
const sel2 = document.getElementById('sel-y2');
const btnLoad = document.getElementById('btn-load');
const statusText = document.getElementById('status-text');
const alertContainer = document.getElementById('alert-container');
const alertBox = document.getElementById('alert-box');
const alertIcon = document.getElementById('alert-icon');
const alertMessage = document.getElementById('alert-message');
const mapSubtitle = document.getElementById('map-subtitle');

let changeLayer = null;
let roiBoundaryLayer = null;

// All 15 valid chronological comparison pairs (2019-2024)
const ALLOWED_PAIRS = [
  [2019, 2020], [2019, 2021], [2019, 2022], [2019, 2023], [2019, 2024],
  [2020, 2021], [2020, 2022], [2020, 2023], [2020, 2024],
  [2021, 2022], [2021, 2023], [2021, 2024],
  [2022, 2023], [2022, 2024],
  [2023, 2024]
];

// Load and overlay the official study-area boundary
fetchJSON('/api/meta').then(meta => {
  if (meta && meta.study_area && meta.study_area.geojson) {
    roiBoundaryLayer = L.geoJSON(meta.study_area.geojson, {
      style: { color: '#1B4332', weight: 2.5, fillOpacity: 0.05, dashArray: '4, 4' }
    }).addTo(mapChange);
    roiBoundaryLayer.bindPopup('<strong>Brgy. Dulao Shoreline</strong><br>Official Study Area Boundary (2019–2024)<br><small>Aringay, La Union</small>');
  }
}).catch(() => {});

function getAllowedLaterYears(y1) {
  return ALLOWED_PAIRS.filter(p => p[0] === y1).map(p => p[1]);
}

function syncSelectsFromY1(desiredY2) {
  const y1 = +sel1.value;
  const allowed = getAllowedLaterYears(y1);
  sel2.innerHTML = '';
  allowed.forEach(y2 => {
    const opt = document.createElement('option');
    opt.value = y2;
    opt.textContent = String(y2);
    sel2.appendChild(opt);
  });
  if (desiredY2 && allowed.includes(+desiredY2)) {
    sel2.value = desiredY2;
  } else {
    // Default to the latest available year
    sel2.value = allowed[allowed.length - 1];
  }
}

sel1.addEventListener('change', () => {
  const prevY2 = +sel2.value;
  syncSelectsFromY1(prevY2);
});

// Initialize with 2019 -> 2024
syncSelectsFromY1(2024);

function showAlert(type, iconClass, message) {
  if (!alertContainer || !alertBox) return;
  alertBox.className = `alert alert-${type} d-flex align-items-center mb-0`;
  alertIcon.innerHTML = `<i class="${iconClass}"></i>`;
  alertMessage.innerHTML = message;
  alertContainer.classList.remove('d-none');
}

function hideAlert() {
  if (alertContainer) alertContainer.classList.add('d-none');
}

async function loadChange() {
  const y1 = sel1.value, y2 = sel2.value;
  hideAlert();

  // Progress message
  btnLoad.disabled = true;
  btnLoad.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Analyzing…';
  if (statusText) {
    statusText.innerHTML = '<div class="spinner-border spinner-border-sm text-forest me-2" role="status"></div><span>Analyzing satellite images… this may take a minute.</span>';
  }

  ['card-gain', 'card-loss', 'card-stable', 'card-net']
    .forEach(id => document.getElementById(id).textContent = '…');

  try {
    const d = await fetchJSON(`/api/change/${y1}/${y2}`);
    if (changeLayer) mapChange.removeLayer(changeLayer);

    changeLayer = L.geoJSON(d.geojson, {
      style: styleByClass(),
      onEachFeature: (f, l) => {
        const c = f.properties.class;
        const isGain = c === 'gain';
        const isLoss = c === 'loss';
        const isStable = c === 'stable';
        const isNonMangrove = c === 'stable_non_mangrove';
        let label = 'Mapped Change';
        let meaning = '';
        let color = COLORS.mangrove;
        if (isGain) {
          label = 'Mapped Gain (▲)';
          meaning = 'Newly grown or appeared mangroves';
          color = COLORS.gain;
        } else if (isLoss) {
          label = 'Mapped Loss (▼)';
          meaning = 'Disappeared or was removed';
          color = COLORS.loss;
        } else if (isStable) {
          label = 'Stable Mangrove (●)';
          meaning = 'Mangroves that remained present and healthy';
          color = COLORS.stable;
        } else if (isNonMangrove) {
          label = 'Stable Non-mangrove (◻)';
          meaning = 'Open water, mudflats, and coastline without mangroves in either year';
          color = '#6c757d';
        }
        l.bindPopup(`<strong style="color:${color}">${label}</strong><br>
                     <span>${meaning}</span><br>
                     <span class="small text-muted">Area: <strong>${fmt(f.properties.area_ha)} hectares</strong></span><br>
                     <small class="text-muted">Observation period: ${y1} → ${y2}</small>`);
      }
    }).addTo(mapChange);

    if (changeLayer.getBounds && changeLayer.getBounds().isValid()) {
      mapChange.fitBounds(changeLayer.getBounds(), { padding: [24, 24] });
    }

    // Card values
    document.getElementById('card-gain').textContent   = fmt(d.gain_ha) + ' hectares';
    document.getElementById('card-loss').textContent   = fmt(d.loss_ha) + ' hectares';
    document.getElementById('card-stable').textContent = fmt(d.stable_mangrove_ha) + ' hectares';

    // Everyday size comparisons
    const gainFields = Math.round((d.gain_ha || 0) * 1.4);
    const lossFields = Math.round((d.loss_ha || 0) * 1.4);
    const stableFields = Math.round((d.stable_mangrove_ha || 0) * 1.4);
    const nonMangroveFields = Math.round((d.stable_non_mangrove_ha || 0) * 1.4);

    const gainComp = document.getElementById('gain-compare');
    if (gainComp) gainComp.innerHTML = `<i class="bi bi-bounding-box me-1"></i>About ${gainFields} football fields of new growth.`;

    const lossComp = document.getElementById('loss-compare');
    if (lossComp) lossComp.innerHTML = `<i class="bi bi-bounding-box me-1"></i>About ${lossFields} football fields of lost trees.`;

    const stableComp = document.getElementById('stable-compare');
    if (stableComp) stableComp.innerHTML = `<i class="bi bi-bounding-box me-1"></i>About ${stableFields} football fields retained.`;

    // Net change
    const net = (d.gain_ha ?? 0) - (d.loss_ha ?? 0);
    const netEl = document.getElementById('card-net');
    netEl.textContent = (net >= 0 ? '+' : '−') + fmt(Math.abs(net)) + ' hectares';
    netEl.classList.toggle('text-forest', net >= 0);
    netEl.classList.toggle('text-loss',   net < 0);

    const netComp = document.getElementById('net-compare');
    if (netComp) {
      const netFields = Math.round(Math.abs(net) * 1.4);
      netComp.innerHTML = `<i class="bi bi-info-circle me-1"></i>${net >= 0 ? 'Net gain' : 'Net loss'} of about ${netFields} football fields.`;
    }

    // Table elements
    const tableBadge = document.getElementById('table-interval-badge');
    if (tableBadge) tableBadge.textContent = `${y1} → ${y2}`;

    const tblGainArea = document.getElementById('tbl-gain-area');
    if (tblGainArea) tblGainArea.textContent = `+${fmt(d.gain_ha)} hectares`;
    const tblGainScale = document.getElementById('tbl-gain-scale');
    if (tblGainScale) tblGainScale.textContent = `About ${gainFields} football fields`;
    const tblGainDesc = document.getElementById('tbl-gain-desc');
    if (tblGainDesc) tblGainDesc.textContent = `Mangroves newly appeared in ${y2} that were not present in ${y1}.`;

    const tblLossArea = document.getElementById('tbl-loss-area');
    if (tblLossArea) tblLossArea.textContent = `−${fmt(d.loss_ha)} hectares`;
    const tblLossScale = document.getElementById('tbl-loss-scale');
    if (tblLossScale) tblLossScale.textContent = `About ${lossFields} football fields`;
    const tblLossDesc = document.getElementById('tbl-loss-desc');
    if (tblLossDesc) tblLossDesc.textContent = `Mangroves detected in ${y1} that disappeared by ${y2}. Priority area for coastal monitoring.`;

    const tblStableArea = document.getElementById('tbl-stable-area');
    if (tblStableArea) tblStableArea.textContent = `${fmt(d.stable_mangrove_ha)} hectares`;
    const tblStableScale = document.getElementById('tbl-stable-scale');
    if (tblStableScale) tblStableScale.textContent = `About ${stableFields} football fields`;
    const tblStableDesc = document.getElementById('tbl-stable-desc');
    if (tblStableDesc) tblStableDesc.textContent = `Mangrove stands that remained healthy and present in both ${y1} and ${y2}.`;

    const tblNonMangroveArea = document.getElementById('tbl-nonmangrove-area');
    if (tblNonMangroveArea) tblNonMangroveArea.textContent = `${fmt(d.stable_non_mangrove_ha)} hectares`;
    const tblNonMangroveScale = document.getElementById('tbl-nonmangrove-scale');
    if (tblNonMangroveScale) tblNonMangroveScale.textContent = `About ${nonMangroveFields} football fields`;
    const tblNonMangroveDesc = document.getElementById('tbl-nonmangrove-desc');
    if (tblNonMangroveDesc) tblNonMangroveDesc.textContent = `Water, mudflats, and shoreline within the study area with no mangrove canopy in either ${y1} or ${y2}.`;

    const tblNetArea = document.getElementById('tbl-net-area');
    if (tblNetArea) {
      tblNetArea.textContent = `${net >= 0 ? '+' : '−'}${fmt(Math.abs(net))} hectares`;
      tblNetArea.className = `text-end fw-bold ${net >= 0 ? 'text-success' : 'text-danger'}`;
    }
    const tblNetScale = document.getElementById('tbl-net-scale');
    if (tblNetScale) tblNetScale.textContent = `About ${Math.round(Math.abs(net) * 1.4)} football fields`;
    const tblNetDesc = document.getElementById('tbl-net-desc');
    if (tblNetDesc) {
      tblNetDesc.textContent = net >= 0
        ? `Overall forest expansion of ${fmt(net)} hectares between ${y1} and ${y2}.`
        : `Overall forest decline of ${fmt(Math.abs(net))} hectares between ${y1} and ${y2}.`;
    }

    if (mapSubtitle) mapSubtitle.textContent = `Comparing survey years ${y1} and ${y2}`;

    // Step 3 success message
    if (statusText) {
      statusText.innerHTML = `<i class="bi bi-check-circle-fill text-success me-2 fs-5"></i><span>Analysis complete for <strong>${y1} → ${y2}</strong>. Inspect the summary cards, map, and table below.</span>`;
    }
  } catch (e) {
    if (statusText) {
      statusText.innerHTML = '<i class="bi bi-exclamation-triangle-fill text-danger me-2 fs-5"></i><span>We could not complete the analysis for that period.</span>';
    }
    const errMsg = (e && e.error) || (e && e.message) || `The comparison between ${y1} and ${y2} is not available. Please choose from the allowed year pairs.`;
    showAlert('warning', 'bi bi-exclamation-triangle-fill text-warning', errMsg);
    ['card-gain', 'card-loss', 'card-stable', 'card-net', 'tbl-gain-area', 'tbl-loss-area', 'tbl-stable-area', 'tbl-nonmangrove-area', 'tbl-net-area']
      .forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = '—';
      });
  } finally {
    btnLoad.disabled = false;
    btnLoad.innerHTML = '<i class="bi bi-play-circle-fill me-1"></i> Detect Changes';
  }
}

btnLoad.addEventListener('click', loadChange);
loadChange();   // initial: 2023 → 2024
