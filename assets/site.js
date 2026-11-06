const input = document.querySelector('#dictionary-search');
const status = document.querySelector('#search-status');
// Search only the 13 root tables; vowel and initial reference tables stay visible.
const tables = [...document.querySelectorAll('#dictionary table')].filter(table =>
  table.tHead.rows[0].cells[0].textContent.trim() === 'ハングル' &&
  [...table.tBodies[0].rows].some(row => row.cells[0].textContent.trim() === '가' ||
    /^[가-힣]$/.test(row.cells[0].textContent.trim()))
);
const rows = tables.flatMap(table => [...table.tBodies[0].rows]);
function searchDictionary() {
  const query = input.value.trim().normalize('NFKC').toLocaleLowerCase('ja');
  let count = 0;
  for (const row of rows) {
    const matches = row.textContent.normalize('NFKC').toLocaleLowerCase('ja').includes(query);
    row.hidden = !matches;
    if (matches) count++;
  }
  status.textContent = query ? `${count} / ${rows.length} 語根が見つかりました` : `${rows.length} 語根を収録`;
}
input.addEventListener('input', searchDictionary);
searchDictionary();
const links = [...document.querySelectorAll('nav a')];
function markCurrent() {
  const hash = location.hash || '#home';
  for (const link of links) {
    if (link.hash === hash) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
}
window.addEventListener('hashchange', markCurrent);
markCurrent();
