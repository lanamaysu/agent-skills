---
name: jest-rtl-testing
description: Use when writing, reviewing, or debugging Jest + React Testing Library tests, before writing test code or when tests fail
---

# Jest + React Testing Library Best Practices

**Core principle:** A test interacts with the application as a user does. A test does not check implementation details.

## Pre-Check

Do these steps before you write a test:

1. Find `AGENTS.md` in the project root. If it exists, read its Testing section.
2. Follow the `AGENTS.md` rules when they conflict with this skill.

---

Do not use this skill for pure-function tests (no DOM, no React), E2E tests, performance tests or visual regression tests.

---

## Quick Reference

### Query Priority

`getByRole` is slow on large views ([issue 820](https://github.com/testing-library/dom-testing-library/issues/820)), so the list puts `getByLabelText` and `getByText` first.

Use the first query in this list that finds the element:

1. `getByLabelText`: use for form fields.
2. `getByText`: use for non-interactive content.
3. `getByRole`: use only in small components. It also checks accessibility.
4. `getByPlaceholderText`, `getByDisplayValue`, `getByAltText`.
5. `getByTestId`: use only when no query above works. Add a code comment that tells why no accessible query works.

**Query types:**
- `getBy*`: the element must exist. The query throws an error if it finds no element.
- `queryBy*`: use to assert that an element is absent. The query returns `null`.
- `findBy*`: use to wait for an element. The query returns a Promise.

---

## Core Principles

1. **Async:** Use `findBy*` to wait for an element to appear. Use `waitForElementToBeRemoved` to wait for an element to disappear.
2. **Real interactions:** Use `@testing-library/user-event`. Do not use `fireEvent` when `user-event` can do the interaction.
3. **HTTP mocks:** Use MSW to mock network requests. Do not mock `fetch` or `axios` manually.

---

## Debugging

- Use `screen.debug()` to show the DOM.
- Make sure that the query type is correct: `getBy*`, `queryBy*` or `findBy*`.
- Use `screen.logTestingPlaygroundURL()` to find a better query.

---

## References

Do not read a reference file from start to end. Find the heading with `grep -n '^#' <file>`, then read only that section.

- [references/query-cheatsheet.md](./references/query-cheatsheet.md): read a section when you cannot select a query, or when you need `within` or `TextMatch`.
- [references/common-patterns.md](./references/common-patterns.md): read a section when you need a pattern. The patterns are forms, MSW, errors, modals, lists, file upload, context and hooks.

External sources:
- [Testing Library - Guiding Principles](https://testing-library.com/docs/guiding-principles)
- [Testing Library - Queries](https://testing-library.com/docs/queries/about)
- [Testing Library - Async](https://testing-library.com/docs/dom-testing-library/api-async)
- [MSW Documentation](https://mswjs.io/docs/)
- [Common mistakes with React Testing Library (Kent C. Dodds)](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

**Last Updated**: 2026-10-07
