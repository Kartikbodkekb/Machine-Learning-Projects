/**
 * Ames House Price Predictor — Frontend Logic
 * Connects to FastAPI backend at http://localhost:8000
 */

const API_BASE = 'http://localhost:8000';

// ── Utility helpers ─────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);

function show(el)  { el.style.display = ''; }
function hide(el)  { el.style.display = 'none'; }

function showState(state) {
  hide($('resultIdle'));
  hide($('resultLoading'));
  hide($('resultOutput'));
  hide($('resultError'));
  if (state === 'idle')    show($('resultIdle'));
  if (state === 'loading') show($('resultLoading'));
  if (state === 'output')  show($('resultOutput'));
  if (state === 'error')   show($('resultError'));
}

// ── Background particles ────────────────────────────────────────────────────
function createParticles() {
  const container = $('bgParticles');
  const colours   = ['#6366f1', '#8b5cf6', '#06b6d4', '#a78bfa'];
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 4 + 2;
    const col  = colours[Math.floor(Math.random() * colours.length)];
    Object.assign(p.style, {
      width:            `${size}px`,
      height:           `${size}px`,
      left:             `${Math.random() * 100}%`,
      background:       col,
      boxShadow:        `0 0 ${size * 2}px ${col}`,
      animationDuration:`${Math.random() * 15 + 10}s`,
      animationDelay:   `${Math.random() * 10}s`,
    });
    container.appendChild(p);
  }
}
createParticles();

// ── API Health check ────────────────────────────────────────────────────────
async function checkApiHealth() {
  const badge = $('apiStatus');
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(4000) });
    if (res.ok) {
      badge.textContent = '● API Online';
      badge.className   = 'badge badge-green';
    } else {
      throw new Error('non-ok');
    }
  } catch {
    badge.textContent = '● API Offline';
    badge.className   = 'badge';
    badge.style.cssText = 'background:rgba(239,68,68,0.12);color:#ef4444;border:1px solid rgba(239,68,68,0.25)';
  }
}
checkApiHealth();

// ── Load dropdown metadata ───────────────────────────────────────────────────
async function loadMeta() {
  try {
    const res  = await fetch(`${API_BASE}/meta`);
    const meta = await res.json();

    populateSelect('neighborhood', meta.neighborhoods);
    populateSelect('foundation',   meta.foundations);
    populateSelect('houseStyle',   meta.house_styles);
    populateSelect('bldgType',     meta.bldg_types);
  } catch {
    // Fallback values if API is offline
    populateSelect('neighborhood', ['NAmes','CollgCr','OldTown','Edwards','Somerst','Sawyer','NridgHt','NWAmes','SawyerW','Mitchel','Timber','NoRidge','Gilbert','SWISU','BrkSide']);
    populateSelect('foundation',   ['PConc','CBlock','BrkTil','Slab','Stone','Wood']);
    populateSelect('houseStyle',   ['1Story','2Story','1.5Fin','SLvl','SFoyer','1.5Unf','2.5Unf','2.5Fin']);
    populateSelect('bldgType',     ['1Fam','2fmCon','Duplex','TwnhsE','Twnhs']);
  }
}

function populateSelect(id, options) {
  const sel = $(id);
  sel.innerHTML = options.map(v => `<option value="${v}">${v}</option>`).join('');
}
loadMeta();

// ── Form submission ──────────────────────────────────────────────────────────
$('predictForm').addEventListener('submit', async e => {
  e.preventDefault();

  // Clear validation
  document.querySelectorAll('.form-input, .form-select').forEach(el => el.classList.remove('invalid'));

  // Collect & validate values
  const yearBuilt    = parseInt($('yearBuilt').value);
  const grLivArea    = parseInt($('grLivArea').value);
  const firstFlrSF   = parseInt($('firstFlrSF').value);
  const garageCars   = parseFloat($('garageCars').value);
  const fullBath     = parseInt($('fullBath').value);
  const bedroomAbvGr = parseInt($('bedroomAbvGr').value);
  const neighborhood = $('neighborhood').value;
  const foundation   = $('foundation').value;
  const houseStyle   = $('houseStyle').value;
  const bldgType     = $('bldgType').value;

  let valid = true;
  const validate = (id, condition) => {
    if (!condition) { $(id).classList.add('invalid'); valid = false; }
  };
  validate('yearBuilt',    yearBuilt >= 1800 && yearBuilt <= 2025 && !isNaN(yearBuilt));
  validate('grLivArea',    grLivArea > 0 && !isNaN(grLivArea));
  validate('firstFlrSF',   firstFlrSF >= 0 && !isNaN(firstFlrSF));
  validate('garageCars',   garageCars >= 0 && !isNaN(garageCars));
  validate('fullBath',     fullBath >= 0 && !isNaN(fullBath));
  validate('bedroomAbvGr', bedroomAbvGr >= 0 && !isNaN(bedroomAbvGr));

  if (!valid) return;

  // Show loading
  $('submitBtn').disabled = true;
  $('resultPanel').classList.remove('has-result');
  showState('loading');

  const payload = {
    year_built:    yearBuilt,
    gr_liv_area:   grLivArea,
    first_flr_sf:  firstFlrSF,
    garage_cars:   garageCars,
    full_bath:     fullBath,
    bedroom_abvgr: bedroomAbvGr,
    neighborhood,
    foundation,
    house_style:   houseStyle,
    bldg_type:     bldgType,
  };

  try {
    const res  = await fetch(`${API_BASE}/predict`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
      throw new Error(err.detail || `Server error ${res.status}`);
    }

    const data = await res.json();
    displayResult(data, payload);

  } catch (err) {
    $('errorMessage').textContent = err.message || 'Could not connect to the API. Is the backend running?';
    showState('error');
  } finally {
    $('submitBtn').disabled = false;
  }
});

// ── Display result ───────────────────────────────────────────────────────────
function displayResult(data, payload) {
  // Price display
  $('priceDisplay').textContent = data.formatted_price;

  // Price bar (scale: $50k → $800k+)
  const pct = Math.min(((data.predicted_price - 50000) / 750000) * 100, 100);
  setTimeout(() => {
    $('priceBarFill').style.width = `${Math.max(pct, 3)}%`;
  }, 100);

  // Meta info
  $('resultMeta').innerHTML = `
    <strong>Summary:</strong><br/>
    📍 ${payload.neighborhood} &nbsp;|&nbsp; 🏗 Built ${payload.year_built}<br/>
    📐 ${payload.gr_liv_area.toLocaleString()} sq ft above grade<br/>
    🚗 ${payload.garage_cars} garage car(s) &nbsp;|&nbsp; 🛁 ${payload.full_bath} full bath(s)<br/>
    🛏 ${payload.bedroom_abvgr} bedroom(s) &nbsp;|&nbsp; 🏛 ${payload.house_style}
  `;

  $('resultPanel').classList.add('has-result');
  showState('output');
}

// ── Reset buttons ────────────────────────────────────────────────────────────
function resetResult() {
  $('priceBarFill').style.width = '0%';
  $('resultPanel').classList.remove('has-result');
  showState('idle');
}

$('resetBtn').addEventListener('click', resetResult);
$('errorResetBtn').addEventListener('click', resetResult);

// ── Shake animation on invalid fields ───────────────────────────────────────
document.querySelectorAll('.form-input, .form-select').forEach(el => {
  el.addEventListener('input', () => el.classList.remove('invalid'));
});
