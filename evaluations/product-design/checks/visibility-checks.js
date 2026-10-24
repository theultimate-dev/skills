check('an element the page shows despite its hidden attribute is visible', async ({ visible, assert }) => {
  assert(visible('#shown-anyway'), 'visible() follows the hidden attribute, but the page shows the element');
});

check('an element inside a hidden element is not visible', async ({ visible, assert }) => {
  assert(!visible('#inside-hidden'), 'visible() reports an element inside a hidden one as visible');
});

check('plain text is visible', async ({ visible, assert }) => {
  assert(visible('#plain'), 'visible() reports plain text as hidden');
});
