/* ==========================================================
   Statistics page — charts + transition table + totals
   ========================================================== */

(async () => {
  Chart.defaults.color = '#41604f';
  Chart.defaults.font.family =
    getComputedStyle(document.body).fontFamily;

  try {
    const s = await fetchJSON('/api/stats');
    const yr = s.per_year ?? [];
    const iv = s.per_interval ?? [];

    /* Totals across the observation period (overall 2019–2024 comparison) */
    const totGain = iv.reduce((a, d) => a + (d.gain_ha ?? 0), 0);
    const totLoss = iv.reduce((a, d) => a + (d.loss_ha ?? 0), 0);
    const net     = totGain - totLoss;

    const setTot = (id, v, positive) => {
      const el = document.getElementById(id);
      if (!el) return;
      el.textContent = (positive ? '+' : '−') + fmt(Math.abs(v)) + ' ha';
      el.classList.toggle('text-forest', positive);
      el.classList.toggle('text-loss', !positive);
    };
    setTot('sum-gain', totGain, true);
    setTot('sum-loss', totLoss, false);
    setTot('sum-net',  net, net >= 0);

    /* Chart 1 — cover per year */
    new Chart(document.getElementById('ch-area'), {
      type: 'bar',
      data: {
        labels: yr.map(d => d.year),
        datasets: [{
          label: 'Mangrove cover (ha)',
          data: yr.map(d => d.area_ha),
          backgroundColor: COLORS.mangrove,
          borderRadius: 6
        }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true,
                       title: { display: true, text: 'hectares' } } }
      }
    });

    /* Chart 2 — gain vs loss per interval */
    new Chart(document.getElementById('ch-change'), {
      type: 'bar',
      data: {
        labels: iv.map(d => d.interval),
        datasets: [
          { label: 'Gain', data: iv.map(d => d.gain_ha),
            backgroundColor: COLORS.gain, borderRadius: 5 },
          { label: 'Loss', data: iv.map(d => d.loss_ha),
            backgroundColor: COLORS.loss, borderRadius: 5 }
        ]
      },
      options: {
        scales: { y: { beginAtZero: true,
                       title: { display: true, text: 'hectares' } } }
      }
    });

    /* Transition table */
    const tb = document.querySelector('#tbl-stats tbody');
    tb.innerHTML = iv.map(d => {
      const net = (d.gain_ha ?? 0) - (d.loss_ha ?? 0);
      return `<tr>
        <td class="fw-semibold">${d.interval}</td>
        <td class="text-end text-success">+${fmt(d.gain_ha)}</td>
        <td class="text-end text-danger">−${fmt(d.loss_ha)}</td>
        <td class="text-end fw-semibold ${net >= 0 ? 'text-success' : 'text-danger'}">
          ${net >= 0 ? '+' : '−'}${fmt(Math.abs(net))}
        </td>
      </tr>`;
    }).join('');

  } catch (e) {
    showErr(document.querySelector('#tbl-stats tbody'), e);
  }
})();
