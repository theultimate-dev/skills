// Checks for fixtures/clean-tree served under /a/b/, loaded by interaction-harness.html?checks=hosted-checks.js.
// The harness opens a/b/index.html: the tree's entry page, or the view itself on a stage that publishes only the view.

const view = 'views/saved-guides/index.html';

// Follows the entry page's link to the view. A page without the link is the view itself.
async function openView({ $$, loaded, click }) {
  if (!$$('#to-view').length) return;
  const next = loaded();
  click('#to-view');
  await next;
}

check('entry reaches view', async ({ $, $$, page, loaded, click, assert }) => {
  assert($$('#to-view').length === 1, 'the page at a/b/index.html has no link to the view');
  await openView({ $$, loaded, click });
  const path = page().window.location.pathname;
  assert(path.endsWith(`/a/b/${view}`), `the link reached ${path}`);
  assert($('#view-heading').textContent.trim() === 'Your saved guides', 'the view heading is missing');
});

check('shared tokens applied', async ({ $, $$, loaded, click, style, assert }) => {
  await openView({ $$, loaded, click });
  $('#view-heading');
  const token = style(':root', '--color-paper');
  assert(token === '#f5f3e9', `--color-paper is "${token}", so shared/tokens.css did not apply`);
  const background = style('body', 'background-color');
  assert(background === 'rgb(245, 243, 233)', `the body background is ${background}, so shared/components.css did not apply`);
});
