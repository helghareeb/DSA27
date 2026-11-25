'use strict';

const byId = id => document.getElementById(id);
const lecture = byId('lecture');
const scenario = byId('scenario');
const prediction = byId('prediction');
const play = byId('play');
let frame = 0;
let timer = null;

function getScenario() {
  return traceLessons[lecture.value].scenarios[Number(scenario.value)];
}

function stop() {
  clearInterval(timer);
  timer = null;
  play.textContent = 'Play';
}

function render() {
  const active = getScenario();
  const [rule, explanation, rows, check] = active.frames[frame];
  byId('explanation').textContent = explanation;
  byId('state').replaceChildren(...rows.flatMap(([label, value]) => {
    const term = document.createElement('dt');
    const description = document.createElement('dd');
    term.textContent = label;
    description.textContent = value;
    description.className = 'state';
    return [term, description];
  }));
  for (const [index, item] of Array.from(byId('rules').children).entries()) {
    if (index === rule) item.setAttribute('aria-current', 'step');
    else item.removeAttribute('aria-current');
  }
  byId('progress').textContent = `Step ${frame + 1} of ${active.frames.length}`;
  byId('back').disabled = frame === 0;
  byId('next').disabled = frame === active.frames.length - 1;
  prediction.open = false;
  prediction.hidden = !check;
  if (check) {
    byId('question').textContent = check[0];
    byId('answer').textContent = check[1];
  }
}

function move(step) {
  const end = getScenario().frames.length - 1;
  frame = Math.min(end, Math.max(0, step));
  render();
  if (frame === end) stop();
}

function loadScenario() {
  stop();
  const active = getScenario();
  byId('intro').textContent = active.intro;
  byId('rules').replaceChildren(...active.rules.map(rule => {
    const item = document.createElement('li');
    item.textContent = rule;
    return item;
  }));
  frame = 0;
  render();
}

function loadLecture() {
  const week = lecture.value;
  const active = traceLessons[week];
  byId('title').textContent = active.title;
  document.title = `${active.title} · DSA27`;
  byId('quiz').href = `https://helghareeb.github.io/en/quizzes/dsa27/week-${week}/`;
  byId('arabic-quiz').href = `https://helghareeb.github.io/ar/quizzes/dsa27/week-${week}/`;
  scenario.replaceChildren(...active.scenarios.map((item, index) => new Option(item.name, index)));
  loadScenario();
}

function loadFromHash() {
  const week = location.hash.match(/^#week-(\d\d)$/)?.[1];
  lecture.value = Object.hasOwn(traceLessons, week) ? week : '10';
  loadLecture();
}

function playOrPause() {
  if (timer !== null) {
    stop();
    return;
  }
  if (byId('next').disabled) move(0);
  play.textContent = 'Pause';
  timer = setInterval(() => move(frame + 1), 1600);
}

lecture.replaceChildren(...Object.entries(traceLessons)
  .sort(([a], [b]) => Number(a) - Number(b))
  .map(([week, lesson]) => new Option(`${week} · ${lesson.title}`, week)));
lecture.addEventListener('change', () => { location.hash = `week-${lecture.value}`; });
scenario.addEventListener('change', loadScenario);
window.addEventListener('hashchange', loadFromHash);
byId('restart').addEventListener('click', () => { stop(); move(0); });
byId('back').addEventListener('click', () => { stop(); move(frame - 1); });
byId('next').addEventListener('click', () => { stop(); move(frame + 1); });
play.addEventListener('click', playOrPause);
document.addEventListener('keydown', event => {
  if (event.target.closest('button, select, a, summary') || event.altKey || event.ctrlKey || event.metaKey) return;
  const buttons = { ArrowLeft: 'back', ArrowRight: 'next', r: 'restart', p: 'play' };
  const button = buttons[event.key];
  if (button) {
    event.preventDefault();
    byId(button).click();
  }
});
loadFromHash();
