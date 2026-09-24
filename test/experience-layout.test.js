const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const page = fs.readFileSync(path.resolve(__dirname, '../_pages/about.md'), 'utf8');
const experienceSection = page.split('<div class="experience-list">')[1];
const cards = experienceSection.split('<article class="experience-item">').slice(1);

test('school experiences use the same role-and-research row as China Telecom', () => {
  assert.equal(cards.length, 4);

  for (const [name, role, research] of [
    ['National University of Singapore', 'Joint Ph.D. student', 'Graph Foundation Models, Self-Evolving Agents'],
    ['Hong Kong University of Science and Technology (Guangzhou)', 'Research visitor', 'Graph Foundation Models, Cross-Domain Generalization, Agent Memory'],
    ['Lehigh University', 'Research visitor', 'Graph Adversarial Robustness, Large Language Models'],
  ]) {
    const card = cards.find((item) => item.includes(`<div class="experience-title">${name}</div>`));
    assert.ok(card, `${name} card is missing`);
    assert.ok(card.includes(`<div class="experience-detail"><span>${role}</span><strong>${research}</strong></div>`));
    assert.equal((card.match(/class="experience-detail"/g) || []).length, 2);
  }
});

test('NUS experience remains ongoing', () => {
  const nus = cards.find((item) => item.includes('<div class="experience-title">National University of Singapore</div>'));
  assert.ok(nus);
  assert.match(nus, /<div class="experience-time">2026\.08 - now<\/div>/);
});
