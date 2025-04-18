// Add Jest setup code here
import '@testing-library/jest-dom';

// Mock the fetch API
global.fetch = jest.fn();

// Mock environment variables
process.env.NEXT_PUBLIC_API_BASE_URL = 'http://localhost:8000';
process.env.NEXT_PUBLIC_USE_MOCK_API = 'true';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // Deprecated
    removeListener: jest.fn(), // Deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Suppress specific console errors during tests
const originalError = console.error;
console.error = (...args) => {
  if (/Warning.*not wrapped in act/.test(args[0])) {
    return;
  }
  originalError.call(console, ...args);
};
