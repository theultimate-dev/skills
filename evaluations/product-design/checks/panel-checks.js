// Checks for fixtures/panel-bug and fixtures/panel-fixed, loaded by interaction-harness.html?checks=panel-checks.js.

check('panel opens on click', async ({ click, record, assert }) => {
  const hidden = record('#filters', 'hidden');
  click('#filters-button');
  assert(hidden.values().includes(null), 'the panel kept its hidden attribute throughout the click');
});

check('panel stays open after one click', async ({ click, wait, visible, assert }) => {
  click('#filters-button');
  await wait(100);
  assert(visible('#filters'), 'the panel is hidden after one click');
});

check('panel closes on Escape', async ({ click, press, visible, assert }) => {
  click('#filters-button');
  assert(visible('#filters'), 'the panel did not open');
  press('Escape');
  assert(!visible('#filters'), 'the panel is still visible');
});

check('focus returns to the control', async ({ click, press, focused, $, assert }) => {
  click('#filters-button');
  assert(focused() !== $('#filters-button'), 'focus did not move into the panel');
  press('Escape');
  assert(focused() === $('#filters-button'), `focus is on ${focused().outerHTML.slice(0, 60)}`);
});

check('aria-expanded follows the panel', async ({ click, press, attr, assert }) => {
  assert(attr('#filters-button', 'aria-expanded') === 'false', 'aria-expanded is not false before opening');
  click('#filters-button');
  assert(attr('#filters-button', 'aria-expanded') === 'true', 'aria-expanded is not true while open');
  press('Escape');
  assert(attr('#filters-button', 'aria-expanded') === 'false', 'aria-expanded is not false after closing');
});

check('panel closes after the timeout', async ({ click, wait, visible, assert }) => {
  click('#filters-button');
  assert(visible('#filters'), 'the panel did not open');
  await wait(2200);
  assert(!visible('#filters'), 'the panel is still visible after 2.2 s without interaction');
});
