// Checks for fixtures/clean-tree served under /a/b/, loaded by interaction-harness.html?checks=hosted-checks.js.
// The harness opens a/b/index.html: the tree's entry page, or the view itself on a stage that publishes only the view.

const view = 'views/saved-guides/index.html';

// Fails when the server answered the page in the frame with an error, such as a 404 for a tree staged at another prefix.
function assertServed({ page, assert }) {
  const { window: win } = page();
  const [navigation] = win.performance.getEntriesByType('navigation');
  const status = navigation?.responseStatus;
  assert(!status || status < 400, `${win.location.pathname} returned HTTP ${status}`);
}

// Follows the entry page's link to the view. A page without the link is the view itself.
async function openView(helpers) {
  const { $$, loaded, click } = helpers;
  assertServed(helpers);
  if (!$$('#to-view').length) return;
  const next = loaded();
  click('#to-view');
  await next;
  assertServed(helpers);
}

check('entry reaches view', async helpers => {
  const { $, $$, page, assert } = helpers;
  assertServed(helpers);
  assert($$('#to-view').length === 1, 'the page at a/b/index.html has no link to the view');
  await openView(helpers);
  const path = page().window.location.pathname;
  assert(path.endsWith(`/a/b/${view}`), `the link reached ${path}`);
  assert($('#view-heading').textContent.trim() === 'Your saved guides', 'the view heading is missing');
});

check('shared tokens applied', async helpers => {
  const { $, style, assert } = helpers;
  await openView(helpers);
  $('#view-heading');
  const token = style(':root', '--color-paper');
  assert(token === '#f5f3e9', `--color-paper is "${token}", so shared/tokens.css did not apply`);
  const background = style('body', 'background-color');
  assert(background === 'rgb(245, 243, 233)', `the body background is ${background}, so shared/components.css did not apply`);
});
