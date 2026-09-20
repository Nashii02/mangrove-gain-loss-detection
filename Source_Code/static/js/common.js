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
    const col = c === 'gain' ? COLORS.gain : c === 'loss' ? COLORS.loss : COLORS.mangrove;
    return { color: col, weight: 1.5, fillColor: col, fillOpacity: 0.45 };
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
