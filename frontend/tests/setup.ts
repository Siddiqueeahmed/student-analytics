import '@testing-library/jest-dom'

global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}

// axe-core calls getContext for colour-contrast; jsdom doesn't implement it
HTMLCanvasElement.prototype.getContext = () => null as unknown as CanvasRenderingContext2D
