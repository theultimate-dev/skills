/* Scripted checks for project/direction-a.html, for templates/interaction-harness.html.
   Stage direction-a.html untouched at <staging>/a/b/, copy the harness and this file to <staging>/, serve <staging>/ over local HTTP, then open
   interaction-harness.html?page=a/b/direction-a.html&checks=direction-a-checks.js&width=1024&height=768
   and once more with &width=320 for the narrow-frame check. Each check starts from a fresh load. */

check('placement control shows only the chosen group and All shows every group', async ({ click, visible, $$, assert }) => {
  assert(visible('[data-group="builtin"]') && !visible('[data-group="external"]'), 'the page does not start on the built-in group alone');
  click('input[name="placement"][value="external"]');
  assert(visible('[data-group="external"]') && !visible('[data-group="builtin"]'), 'External did not replace Built-in');
  click('input[name="placement"][value="all"]');
  assert($$('.group').every(g => visible(g)), 'All did not show every group');
});

check('settings control sets appearance, contrast, transparency, motion and banner on the page root', async ({ click, attr, style, assert }) => {
  click('input[name="appearance"][value="dark"]');
  assert(attr('html', 'data-appearance') === 'dark', 'appearance is not dark');
  assert(style('html', '--text') === '#f5f5f7', `dark text token is ${style('html', '--text')}`);
  click('#opt-contrast'); assert(attr('html', 'data-contrast') === 'more', 'contrast is not more');
  assert(style('html', '--text') === '#ffffff', `dark increased-contrast text token is ${style('html', '--text')}`);
  click('#opt-transparency'); assert(attr('html', 'data-transparency') === 'reduce', 'transparency is not reduce');
  assert(style('html', '--panel-alpha') === '1', `panel alpha is ${style('html', '--panel-alpha')}`);
  click('#opt-motion'); assert(attr('html', 'data-motion') === 'reduce', 'motion is not reduce');
  click('#opt-banner'); assert(attr('html', 'data-banner') === 'on', 'banner is not on');
});

check('notification banner appears over the panel only when switched on', async ({ click, visible, style, assert }) => {
  assert(!visible('.panel-scene .banner'), 'the banner is visible before it is switched on');
  click('#opt-banner');
  assert(visible('.panel-scene .banner'), 'the banner is not visible after it is switched on');
});

check('choosing a settings tab shows that section in every settings window', async ({ click, $$, attr, assert }) => {
  click('input[name="placement"][value="all"]');
  click('#w1-tab-destinations');
  const open = $$('.tp').filter(p => !p.hidden);
  assert(open.length === 3 && open.every(p => p.dataset.sec === 'destinations'), `open panels: ${open.map(p => p.id).join(', ')}`);
  assert(attr('#w2-tab-destinations', 'aria-selected') === 'true' && attr('#w3-tab-schedule', 'aria-selected') === 'false', 'aria-selected did not follow');
});

check('arrow keys move between tabs, wrap, and keep focus on the selected tab', async ({ click, press, focused, attr, $, assert }) => {
  click('#w2-tab-schedule');
  press('ArrowRight');
  assert(focused() === $('#w2-tab-destinations'), 'ArrowRight did not focus Destinations');
  press('ArrowLeft'); press('ArrowLeft');
  assert(focused() === $('#w2-tab-notifications'), 'ArrowLeft from Schedule did not wrap to Notifications');
  press('Home');
  assert(focused() === $('#w2-tab-schedule') && attr('#w2-tab-schedule', 'tabindex') === '0', 'Home did not return to Schedule');
});

check('reduced motion replaces the Running label with Running and a percentage', async ({ click, visible, assert }) => {
  click('input[name="placement"][value="details"]');
  assert(visible('.pl-motion') && !visible('.pl-static'), 'normal motion does not show the plain Running label');
  click('#opt-motion');
  assert(!visible('.pl-motion') && visible('.pl-static'), 'reduced motion does not show Running with a percentage');
});

check('every fixed-scale scene keeps its token width and scrolls inside its own container', async ({ click, $$, page, style, assert }) => {
  click('input[name="placement"][value="all"]');
  const doc = page().document;
  assert(doc.documentElement.scrollWidth <= page().window.innerWidth, `page scrolls sideways: ${doc.documentElement.scrollWidth} > ${page().window.innerWidth}`);
  const px = name => parseFloat(style('html', name));
  for (const scene of $$('.scene')) {
    const w = scene.getBoundingClientRect().width;
    const token = scene.style.getPropertyValue('--scene-w');
    if (token === 'var(--display-width)') assert(Math.abs(w - px('--display-width')) < .5, `built-in scene is ${w} wide`);
    if (token === 'var(--external-display-width)') assert(Math.abs(w - px('--external-display-width')) < .5, `external scene is ${w} wide`);
    const box = scene.parentElement;
    assert(['auto', 'scroll'].includes(page().window.getComputedStyle(box).overflowX), 'scene container does not scroll sideways');
    if (w > page().window.innerWidth) assert(box.scrollWidth > box.clientWidth, 'a scene wider than the frame does not scroll in its container');
  }
});
