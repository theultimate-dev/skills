// Checks for fixtures/native-scene, loaded by interaction-harness.html?checks=native-scene-checks.js&width=320.
// index.html follows the native-surface profile; widens.html is the control whose scene widens the page.

check('no page scroll at 320', async ({ page, assert }) => {
  const { window: win, document: doc } = page();
  assert(win.innerWidth === 320, `the frame is ${win.innerWidth} px wide; open the harness with width=320`);
  const width = doc.documentElement.scrollWidth;
  assert(width <= 320, `the page is ${width} px wide, so it scrolls sideways at 320`);
});

check('scene scrolls in its container', async ({ $, style, assert }) => {
  const container = $('.scene-viewport');
  assert(container.scrollWidth > container.clientWidth, `the scene fits its ${container.clientWidth} px container, so nothing scrolls in it`);
  const overflow = style(container, 'overflow-x');
  assert(overflow === 'auto' || overflow === 'scroll', `the container's overflow-x is ${overflow}, so the scene spills onto the page`);
});
