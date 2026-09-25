const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const page = fs.readFileSync(path.resolve(__dirname, '../_pages/about.md'), 'utf8');
const news = page.split('<div class="news-timeline">')[1].split('</div>\n\n<h1 id="-publications"')[0];
const firstNews = news.split('<div class="news-item news-item--featured">')[1];
const publications = page.split('<div class="paper-list">')[1];
const firstPaper = publications.split('<article class="paper-item">')[1];

test('EvoMemBench acceptance is the newest featured news item', () => {
  assert.ok(firstNews, 'the newest featured News item is missing');
  assert.match(firstNews, /<div class="news-date">2026\.09<\/div>/);
  assert.match(
    firstNews,
    /<a href="https:\/\/arxiv\.org\/abs\/2605\.18421">EvoMemBench<\/a>/,
  );
  assert.match(firstNews, /NeurIPS 2026 Evaluations &amp; Datasets Track/);
  assert.equal((news.match(/news-item--featured/g) || []).length, 3);
});

test('EvoMemBench is the first publication with one owner asterisk', () => {
  assert.ok(firstPaper, 'the first publication is missing');
  assert.match(
    firstPaper,
    /EvoMemBench: Benchmarking Agent Memory from a Self-Evolving Perspective/,
  );
  assert.match(
    firstPaper,
    /Yuyao Wang, <strong>Zhongjian Zhang\*<\/strong>, Mo Chi, Kaichi Yu, Yuhan Li, Miao Peng, Bing Tong, Chen Zhang, Yan Zhou, Jia Li/,
  );
  assert.doesNotMatch(firstPaper, /Yuyao Wang\*/);
  assert.equal((firstPaper.match(/Zhongjian Zhang\*/g) || []).length, 1);
  assert.match(firstPaper, /<div class="paper-meta">NeurIPS'26 · Evaluations &amp; Datasets Track<\/div>/);
  assert.match(firstPaper, /href="https:\/\/arxiv\.org\/abs\/2605\.18421">Paper<\/a>/);
  assert.match(firstPaper, /href="https:\/\/github\.com\/DSAIL-Memory\/EvoMemBench">Code<\/a>/);
  assert.match(firstPaper, /data-bibtex="bibtex-evomembench26"/);
  assert.match(firstPaper, /@article\{wang2026evomembench,/);
});
