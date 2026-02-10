# Common Testing Patterns

Common React Testing Library test patterns and examples.

---

## Table of Contents

1. [Form Testing](#form-testing)
2. [Async Data Loading with MSW](#async-data-loading-with-msw)
3. [Error Handling](#error-handling)
4. [Modal / Dialog](#modal--dialog)
5. [Lists & Pagination](#lists--pagination)
6. [File Upload](#file-upload)
7. [Context / Provider](#context--provider)
8. [Custom Hooks](#custom-hooks)

---

## Form Testing

### Basic Form Submission

```javascript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('user can submit login form', async () => {
  const user = userEvent.setup()
  const handleSubmit = jest.fn()
  
  render(<LoginForm onSubmit={handleSubmit} />)
  
  // Find inputs by label
  await user.type(screen.getByLabelText(/email/i), 'user@example.com')
  await user.type(screen.getByLabelText(/password/i), 'password123')
  
  // Submit
  await user.click(screen.getByRole('button', { name: /log in/i }))
  
  // Verify
  expect(handleSubmit).toHaveBeenCalledTimes(1)
  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password123'
  })
})
```

### Form Validation

```javascript
test('shows validation errors for invalid input', async () => {
  const user = userEvent.setup()
  render(<SignUpForm />)
  
  // Submit without filling fields
  await user.click(screen.getByRole('button', { name: /sign up/i }))
  
  // Verify error appears
  expect(await screen.findByRole('alert')).toHaveTextContent(
    /email is required/i
  )
  
  // Fill invalid email
  await user.type(screen.getByLabelText(/email/i), 'invalid-email')
  await user.click(screen.getByRole('button', { name: /sign up/i }))
  
  expect(await screen.findByRole('alert')).toHaveTextContent(
    /invalid email format/i
  )
})
```

### Select / Dropdown

```javascript
test('user can select option from dropdown', async () => {
  const user = userEvent.setup()
  render(<CountrySelector />)
  
  const select = screen.getByLabelText(/country/i)
  
  // Select option
  await user.selectOptions(select, 'US')
  
  // Verify selected
  expect(screen.getByRole('option', { name: /united states/i }).selected).toBe(
    true
  )
})
```

### Checkbox / Radio

```javascript
test('user can toggle checkbox', async () => {
  const user = userEvent.setup()
  render(<TermsCheckbox />)
  
  const checkbox = screen.getByRole('checkbox', { name: /accept terms/i })
  
  // Initially unchecked
  expect(checkbox).not.toBeChecked()
  
  // Check
  await user.click(checkbox)
  expect(checkbox).toBeChecked()
  
  // Uncheck
  await user.click(checkbox)
  expect(checkbox).not.toBeChecked()
})
```

---

## Async Data Loading with MSW

### 🎯 MSW is the Recommended Approach

**Why MSW over manual mocks:**
- ✅ Network-level interception (works with any HTTP library)
- ✅ Same handlers for tests and development
- ✅ No coupling to implementation details
- ✅ Realistic HTTP request/response cycle
- ✅ Easy error scenario testing

### MSW Setup

```javascript
// src/mocks/handlers.js
import { rest } from 'msw'

export const handlers = [
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(
      ctx.json({
        name: 'John Doe',
        email: 'john@example.com'
      })
    )
  })
]
```

```javascript
// src/mocks/server.js
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

```javascript
// setupTests.js
import { server } from './mocks/server'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### Basic MSW Test

```javascript
import { rest } from 'msw'
import { server } from './mocks/server'

test('displays user data after loading', async () => {
  render(<UserProfile userId="123" />)
  
  // Verify loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument()
  
  // Wait for data
  expect(await screen.findByText('John Doe')).toBeInTheDocument()
  expect(screen.getByText('john@example.com')).toBeInTheDocument()
  
  // Verify loading gone
  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
})
```

### MSW Error Scenarios

```javascript
test('handles server error', async () => {
  // Override handler for this test only
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) => {
      return res(ctx.status(500))
    })
  )
  
  render(<UserProfile userId="123" />)
  
  expect(await screen.findByRole('alert')).toHaveTextContent(
    /failed to load user data/i
  )
})

test('handles network error', async () => {
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) => {
      return res.networkError('Network connection failed')
    })
  )
  
  render(<UserProfile userId="123" />)
  
  expect(await screen.findByRole('alert')).toHaveTextContent(/network error/i)
})
```

### MSW with Dynamic Responses

```javascript
test('loads different users based on ID', async () => {
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) => {
      const { id } = req.params
      
      const users = {
        '1': { name: 'Alice' },
        '2': { name: 'Bob' }
      }
      
      return res(ctx.json(users[id]))
    })
  )
  
  const { rerender } = render(<UserProfile userId="1" />)
  expect(await screen.findByText('Alice')).toBeInTheDocument()
  
  rerender(<UserProfile userId="2" />)
  expect(await screen.findByText('Bob')).toBeInTheDocument()
})
```

---

## Error Handling

### API Error

```javascript
test('displays error message when API fails', async () => {
  server.use(
    rest.get('/api/data', (req, res, ctx) => {
      return res(ctx.status(500), ctx.json({ error: 'Server error' }))
    })
  )
  
  render(<DataList />)
  
  expect(await screen.findByRole('alert')).toHaveTextContent(/server error/i)
})
```

### Error Boundary

```javascript
test('error boundary catches and displays error', () => {
  // Suppress console.error for this test
  const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})
  
  const ThrowError = () => {
    throw new Error('Something went wrong')
  }
  
  render(
    <ErrorBoundary>
      <ThrowError />
    </ErrorBoundary>
  )
  
  expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
  
  consoleError.mockRestore()
})
```

---

## Modal / Dialog

### Open and Close

```javascript
test('opens and closes modal', async () => {
  const user = userEvent.setup()
  render(<App />)
  
  // Initially no modal
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  
  // Open modal
  await user.click(screen.getByRole('button', { name: /open modal/i }))
  
  // Modal appears
  const modal = screen.getByRole('dialog')
  expect(modal).toBeInTheDocument()
  
  // Close modal
  await user.click(within(modal).getByRole('button', { name: /close/i }))
  
  // Modal gone
  await waitForElementToBeRemoved(modal)
})
```

### Form Inside Modal

```javascript
test('user can submit form inside modal', async () => {
  const user = userEvent.setup()
  const handleSubmit = jest.fn()
  
  render(<App onSubmit={handleSubmit} />)
  
  // Open modal
  await user.click(screen.getByRole('button', { name: /add user/i }))
  
  const modal = screen.getByRole('dialog')
  
  // Fill form (scoped to modal)
  await user.type(within(modal).getByLabelText(/name/i), 'John Doe')
  await user.type(within(modal).getByLabelText(/email/i), 'john@example.com')
  
  // Submit
  await user.click(within(modal).getByRole('button', { name: /submit/i }))
  
  // Modal closes
  await waitForElementToBeRemoved(modal)
  
  // Verify handler
  expect(handleSubmit).toHaveBeenCalledWith({
    name: 'John Doe',
    email: 'john@example.com'
  })
})
```

---

## Lists & Pagination

### Render List

```javascript
test('renders list of items', () => {
  const items = [
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' },
    { id: 3, name: 'Item 3' }
  ]
  
  render(<ItemList items={items} />)
  
  const listItems = screen.getAllByRole('listitem')
  expect(listItems).toHaveLength(3)
  
  expect(screen.getByText('Item 1')).toBeInTheDocument()
  expect(screen.getByText('Item 2')).toBeInTheDocument()
  expect(screen.getByText('Item 3')).toBeInTheDocument()
})
```

### Empty State

```javascript
test('shows empty state when no items', () => {
  render(<ItemList items={[]} />)
  
  expect(screen.getByText(/no items found/i)).toBeInTheDocument()
  expect(screen.queryByRole('list')).not.toBeInTheDocument()
})
```

### Pagination

```javascript
test('user can navigate between pages', async () => {
  const user = userEvent.setup()
  render(<PaginatedList />)
  
  // Initial page 1
  expect(screen.getByText('Page 1 of 5')).toBeInTheDocument()
  
  // Next page
  await user.click(screen.getByRole('button', { name: /next/i }))
  
  // Wait for page 2
  expect(await screen.findByText('Page 2 of 5')).toBeInTheDocument()
  
  // Previous page
  await user.click(screen.getByRole('button', { name: /previous/i }))
  
  expect(await screen.findByText('Page 1 of 5')).toBeInTheDocument()
})
```

---

## File Upload

```javascript
test('user can upload a file', async () => {
  const user = userEvent.setup()
  const handleUpload = jest.fn()
  
  render(<FileUpload onUpload={handleUpload} />)
  
  // Create mock file
  const file = new File(['hello'], 'hello.txt', { type: 'text/plain' })
  
  // Find file input
  const input = screen.getByLabelText(/upload file/i)
  
  // Upload file
  await user.upload(input, file)
  
  // Verify filename displayed
  expect(screen.getByText('hello.txt')).toBeInTheDocument()
  
  // Confirm upload
  await user.click(screen.getByRole('button', { name: /confirm/i }))
  
  // Verify handler called
  expect(handleUpload).toHaveBeenCalledWith(file)
})
```

---

## Context / Provider

### Component Using Context

```javascript
import { ThemeContext } from './ThemeContext'

test('component renders with theme from context', () => {
  render(
    <ThemeContext.Provider value={{ theme: 'dark' }}>
      <ThemedButton />
    </ThemeContext.Provider>
  )
  
  const button = screen.getByRole('button')
  expect(button).toHaveClass('dark-theme')
})
```

### Custom Render with Providers

```javascript
// test-utils.js
import { render } from '@testing-library/react'
import { ThemeProvider } from './ThemeProvider'
import { AuthProvider } from './AuthProvider'

const AllTheProviders = ({ children }) => {
  return (
    <ThemeProvider>
      <AuthProvider>
        {children}
      </AuthProvider>
    </ThemeProvider>
  )
}

const customRender = (ui, options) =>
  render(ui, { wrapper: AllTheProviders, ...options })

// Re-export everything
export * from '@testing-library/react'
export { customRender as render }
```

```javascript
// In tests
import { render, screen } from './test-utils' // Custom render

test('renders with all providers', () => {
  render(<MyComponent />)
  // Component is wrapped with all providers
})
```

---

## Custom Hooks

### Using `renderHook`

```javascript
import { renderHook } from '@testing-library/react'

test('useCounter increments count', () => {
  const { result } = renderHook(() => useCounter())
  
  // Initial value
  expect(result.current.count).toBe(0)
  
  // Execute increment
  act(() => {
    result.current.increment()
  })
  
  // Verify result
  expect(result.current.count).toBe(1)
})
```

### Async Hook

```javascript
test('useFetch loads data', async () => {
  server.use(
    rest.get('/api/data', (req, res, ctx) => {
      return res(ctx.json({ data: 'test' }))
    })
  )
  
  const { result } = renderHook(() => useFetch('/api/data'))
  
  // Initial loading
  expect(result.current.loading).toBe(true)
  expect(result.current.data).toBe(null)
  
  // Wait for load complete
  await waitFor(() => {
    expect(result.current.loading).toBe(false)
  })
  
  // Verify data
  expect(result.current.data).toEqual({ data: 'test' })
})
```

### Hook with Provider

```javascript
test('useAuth returns current user', () => {
  const wrapper = ({ children }) => (
    <AuthProvider user={{ name: 'John' }}>
      {children}
    </AuthProvider>
  )
  
  const { result } = renderHook(() => useAuth(), { wrapper })
  
  expect(result.current.user.name).toBe('John')
})
```

---

## References

- [Testing Library - Example](https://testing-library.com/docs/react-testing-library/example-intro)
- [MSW Documentation](https://mswjs.io/docs/)
- [Common mistakes with React Testing Library](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

**Last Updated**: 2026-02-10
