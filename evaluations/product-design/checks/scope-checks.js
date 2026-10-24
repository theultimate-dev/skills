// Declares names the harness uses internally, then one real check: the harness keeps its own names out of
// the checks file's scope, so the check still runs. Loaded with ?checks=scope-checks.js on fixtures/panel-fixed/.
const frame = '#filters';
const config = { opened: false };
let lines = [];
function report(name) { return name; }
function finish() {}

check('a checks file may reuse the harness names', async ({ click, visible, assert }) => {
  click('#filters-button');
  assert(visible(frame), 'the panel did not open');
});
