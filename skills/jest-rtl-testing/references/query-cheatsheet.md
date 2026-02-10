# Query Methods Cheatsheet

Complete reference for Testing Library query methods.

## Query Type Differences

| Type | Single Element | Multiple Elements | When Not Found | Async |
|------|----------------|-------------------|----------------|-------|
| **getBy** | `getByRole` | `getAllByRole` | Throws error ⚠️ | ❌ |
| **queryBy** | `queryByRole` | `queryAllByRole` | Returns `null` | ❌ |
| **findBy** | `findByRole` | `findAllByRole` | Throws error ⚠️ | ✅ (Promise) |

### When to Use Each

- **getBy\*** - Element **already exists** in the DOM
- **queryBy\*** - Need to **assert element doesn't exist** (`expect(...).not.toBeInTheDocument()`)
- **findBy\*** - Wait for element to **appear asynchronously** (e.g., after API response)

## Query Priority (Context-Aware)

### ⚠️ Performance Consideration

**`getByRole` can be slow on large views** ([github.com/testing-library/dom-testing-library/issues/820](https://github.com/testing-library/dom-testing-library/issues/820))

### For Small Components (< 50 elements)

Use `getByRole` for accessibility validation:

```javascript
const submitButton = screen.getByRole('button', { name: /submit/i })
const heading = screen.getByRole('heading', { level: 1 })
```

### For Large Views (Complex UIs, Lists, Tables)

Prefer `getByLabelText` and `getByText` for better performance:

```javascript
// ✅ Better performance
const emailInput = screen.getByLabelText(/email/i)
const welcomeText = screen.getByText(/welcome back/i)

// ⚠️ May be slow with many elements
const button = screen.getByRole('button', { name: /submit/i })
```

## Priority Guide

### 🥇 Priority 1: Best Performance + Accessibility

#### `getByLabelText`

**Best for all form fields. Excellent performance on any view size.**

```javascript
screen.getByLabelText('Email')
screen.getByLabelText(/email/i)

// Supports various patterns
<label htmlFor="email">Email</label>
<input id="email" />

<label>Email <input /></label>

<input aria-label="Email" />
```

#### `getByText`

**Great for non-interactive content. Excellent performance.**

```javascript
// Recommended: Use regex for flexibility
screen.getByText(/welcome/i)
screen.getByText(/^Welcome back!$/)

// Custom matcher
screen.getByText((content, element) => {
  return content.startsWith('Welcome')
})
```

#### `getByRole`

**Best for small components. Use cautiously on large views.**

```javascript
// Excellent for accessibility validation
screen.getByRole('button', { name: /submit/i })
screen.getByRole('heading', { level: 1 })
screen.getByRole('checkbox', { checked: true })

// ⚠️ Warning: Slow on views with 50+ elements
// For large lists/tables, prefer getByText or getByLabelText
```

**Common roles:**

| Role | Elements | Example |
|------|---------|---------|
| `button` | `<button>`, `<input type="button">` | Buttons |
| `textbox` | `<input type="text">`, `<textarea>` | Text inputs |
| `checkbox` | `<input type="checkbox">` | Checkboxes |
| `link` | `<a href="...">` | Links |
| `heading` | `<h1>`~`<h6>` | Headings (level: 1-6) |
| `list`, `listitem` | `<ul>`, `<li>` | Lists |
| `dialog` | ARIA dialog | Modals |
| `status` | ARIA status | Loading states |
| `alert` | ARIA alert | Error messages |

**getByRole options:**
- `name` - Accessible name (text, label)
- `level` - Heading level (1-6)
- `checked`, `pressed`, `selected`, `expanded` - States
- `hidden` - Include aria-hidden (default: false)

### 🥉 Priority 2: Semantic Queries

#### `getByPlaceholderText`

For forms without labels (prefer adding labels).

```javascript
screen.getByPlaceholderText('Enter email')
```

#### `getByDisplayValue`

For pre-filled form fields.

```javascript
screen.getByDisplayValue('John Doe') // Input with default value
```

#### `getByAltText`

For images with alt text.

```javascript
screen.getByAltText('Profile picture')
```

### 🚫 Priority 3: Last Resort

#### `getByTestId`

**Use only when no semantic option exists. Document why in AGENTS.md.**

```javascript
screen.getByTestId('complex-chart')

// HTML
<div data-testid="complex-chart">...</div>
```

**Acceptable use cases:**
- Complex data visualizations (charts, maps)
- Third-party components (no HTML control)
- After exhausting semantic options

---

## Multiple Elements

```javascript
// getAll - Expects ≥1, throws if none
const buttons = screen.getAllByRole('button')

// queryAll - Returns empty array if none
const buttons = screen.queryAllByRole('button')

// findAll - Async wait
const items = await screen.findAllByRole('listitem')
```

---

## Async Utilities

### `findBy*` - Wait for Appearance

```javascript
const element = await screen.findByText('Success')
const button = await screen.findByRole('button', {}, { timeout: 3000 })
```

### `waitFor` - Wait for Condition

```javascript
await waitFor(() => {
  expect(screen.getByRole('button')).toBeEnabled()
})

await waitFor(
  () => expect(screen.getByText(/success/i)).toBeInTheDocument(),
  { timeout: 3000, interval: 100 }
)
```

### `waitForElementToBeRemoved` - Wait for Disappearance

```javascript
const loader = screen.getByText('Loading...')
await waitForElementToBeRemoved(loader)

// Or with query
await waitForElementToBeRemoved(() => screen.getByText('Loading...'))
```

---

## Within - Scope Queries

```javascript
import { within } from '@testing-library/react'

const sidebar = screen.getByRole('navigation')
within(sidebar).getByRole('button', { name: /login/i })

// In lists
const items = screen.getAllByRole('listitem')
within(items[0]).getByText('Item 1')
```

---

## Quick Decision Flow

```
Start
 ↓
Form field?
 → Yes: getByLabelText ✅
 ↓ No
Non-interactive text?
 → Yes: getByText ✅
 ↓ No
Button/link in SMALL component?
 → Yes: getByRole ✅
 ↓ No
Element in LARGE view (list/table)?
 → Yes: getByText or getByLabelText ✅
     (Avoid getByRole for performance)
 ↓ No
Image?
 → Yes: getByAltText or getByRole('img')
 ↓ No
No other option?
 → Last resort: getByTestId
   (Document why in AGENTS.md)
```

---

## TextMatch Strategies

```javascript
// String - Partial match
screen.getByText('Hello')

// Regex - Recommended
screen.getByText(/hello/i) // Case-insensitive
screen.getByText(/^Hello$/) // Exact

// Function - Custom logic
screen.getByText((content, element) => {
  return content.startsWith('Welcome') && element.tagName === 'H1'
})

// Options
screen.getByText('Hello', { exact: false })
```

---

## References

- [Testing Library Queries](https://testing-library.com/docs/queries/about/)
- [Query Priority](https://testing-library.com/docs/queries/about/#priority)
- [ARIA Roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)
- [getByRole Performance Issue](https://github.com/testing-library/dom-testing-library/issues/820)

---

**Last Updated**: 2026-02-10
