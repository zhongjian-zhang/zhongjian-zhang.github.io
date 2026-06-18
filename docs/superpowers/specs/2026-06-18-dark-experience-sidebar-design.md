# Dark Experience Cards and Sidebar Alignment

## Scope

Improve the desktop profile sidebar and the three experience cards without
changing their content, order, or mobile information architecture.

## Experience Cards

- Lighten the dark-theme card surface from near-black navy to a neutral blue-gray.
- Place each institution logo on the same subtle translucent light backing so
  dark brand colors remain legible.
- Keep the backing compact, rectangular, and consistent across all three logos.
- Preserve the existing light-theme cards and responsive card layout.

## Profile Sidebar

- Move the desktop contact rows slightly to the right so their icon and text
  columns align visually with the profile content above.
- Keep the visitor map centered independently of the contact-row offset.
- Render the unmodified Busuanzi site page-view count on the production
  `zhongjian-zhang.github.io` hostname.
- Render `-----` on `localhost` and `127.0.0.1`, because Busuanzi groups
  those shared development hostnames into unrelated public counters.
- Do not abbreviate the production count with `K` or `M` suffixes.
- Treat the counter as page views reported by the external counter service,
  not as a verified count of unique visitors.

## Validation

- Build the Jekyll site successfully.
- Inspect dark and light themes at desktop width.
- Inspect the affected sections at a mobile width.
- Confirm all three logos remain readable and the sidebar/map alignment does not
  regress.
