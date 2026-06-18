const test = require('node:test');
const assert = require('node:assert/strict');
const { isLocalHostname, observeVisitCount } = require('../assets/js/visit-count.js');

function createCounterFixture(hostname) {
  const observerCallbacks = [];
  let textContent = '';
  let writeCount = 0;
  const value = {};

  Object.defineProperty(value, 'textContent', {
    get() {
      return textContent;
    },
    set(nextValue) {
      textContent = String(nextValue);
      writeCount += 1;
      observerCallbacks.forEach((callback) => queueMicrotask(callback));
    }
  });

  class FakeMutationObserver {
    constructor(callback) {
      this.callback = callback;
    }

    observe() {
      observerCallbacks.push(this.callback);
    }
  }

  const document = {
    documentElement: {},
    addEventListener() {},
    getElementById(id) {
      return id === 'busuanzi_value_site_pv' ? value : null;
    }
  };

  return {
    root: {
      document,
      location: { hostname },
      MutationObserver: FakeMutationObserver
    },
    value,
    getWriteCount() {
      return writeCount;
    }
  };
}

test('recognizes local development hostnames', () => {
  assert.equal(isLocalHostname('localhost'), true);
  assert.equal(isLocalHostname('127.0.0.1'), true);
  assert.equal(isLocalHostname('::1'), true);
  assert.equal(isLocalHostname('zhongjian-zhang.github.io'), false);
});

test('replaces a delayed local Busuanzi value with five dashes', async () => {
  const fixture = createCounterFixture('127.0.0.1');
  observeVisitCount(fixture.root);

  fixture.value.textContent = '10301511';
  await new Promise((resolve) => setImmediate(resolve));

  assert.equal(fixture.value.textContent, '-----');
  assert.equal(fixture.getWriteCount(), 3);
});

test('preserves the raw production Busuanzi value', async () => {
  const fixture = createCounterFixture('zhongjian-zhang.github.io');
  observeVisitCount(fixture.root);

  fixture.value.textContent = '849';
  await new Promise((resolve) => setImmediate(resolve));

  assert.equal(fixture.value.textContent, '849');
  assert.equal(fixture.getWriteCount(), 1);
});
