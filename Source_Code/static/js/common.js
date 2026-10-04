/* ==========================================================
   Shared helpers — used by every page
   ========================================================== */

const COLORS = {
  mangrove: '#2d6a4f',
  gain:     '#52b788',
  loss:     '#ba181b',
  stable:   '#1b4332'
};

const fmt = n => (n == null ? '—' : Number(n).toLocaleString(undefined,
  { maximumFractionDigits: 2 }));

/** GeoJSON styling by feature.properties.class (mangrove | gain | loss) */
function styleByClass() {
  return f => {
    const c = f.properties.class;
    if (c === 'gain') {
      return {
        color: '#1b4332',
        weight: 2,
        fillColor: COLORS.gain,
        fillOpacity: 0.5,
        dashArray: null
      };
    } else if (c === 'loss') {
      return {
        color: '#780016',
        weight: 2.5,
        fillColor: COLORS.loss,
        fillOpacity: 0.55,
        dashArray: '6, 6'
      };
    } else if (c === 'stable') {
      return {
        color: '#1b4332',
        weight: 1.5,
        fillColor: COLORS.stable,
        fillOpacity: 0.35,
        dashArray: null
      };
    } else if (c === 'stable_non_mangrove' || c === 'non_mangrove') {
      return {
        color: '#adb5bd',
        weight: 1.5,
        fillColor: '#dee2e6',
        fillOpacity: 0.18,
        dashArray: '3, 3'
      };
    }
    return {
      color: COLORS.mangrove,
      weight: 1.5,
      fillColor: COLORS.mangrove,
      fillOpacity: 0.4,
      dashArray: null
    };
  };
}

/** fetch + JSON + friendly errors (surfaces API "error" fields) */
async function fetchJSON(url) {
  const r = await fetch(url);
  if (!r.ok) {
    let msg = `Request failed (${r.status})`;
    try { const j = await r.json(); if (j && j.error) msg = j.error; } catch (_) {}
    throw new Error(msg);
  }
  return r.json();
}

/** Render an inline error message into an element */
function showErr(el, e) {
  if (!el) return;
  el.innerHTML =
    `<span class="text-danger"><i class="bi bi-exclamation-triangle me-1"></i>${e.message}</span>`;
}
