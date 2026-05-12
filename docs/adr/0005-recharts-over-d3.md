# ADR 0005 — Recharts over D3

**Status:** Accepted  
**Date:** 2026-05-12

## Context

The dashboard requires bar charts for enrollment, retention, and GPA distribution. The two primary charting options in the React ecosystem are D3.js and Recharts (which is itself built on D3).

D3 gives complete control over SVG elements, scales, and axes. It is the right choice for custom, non-standard visualizations. However, D3 takes ownership of DOM elements and does not integrate cleanly with React's virtual DOM — charts typically require `useEffect` with imperative `d3.select()` calls, which bypasses React's rendering model and makes components hard to test and reason about.

Recharts wraps D3's scales and layout logic in a declarative React component API. `<BarChart data={data}>` renders a composable SVG chart without any `useEffect` or imperative DOM access. Each chart variant (bar, line, area) is a separate composable component, and all configuration (axes, tooltips, grids) is expressed as JSX props.

## Decision

Use Recharts for all charts. D3 is not installed.

## Consequences

**Benefits:**
- Charts are pure React components: testable with Testing Library, renderable in Storybook without setup.
- Responsive layout via `<ResponsiveContainer>` requires no manual resize observers.
- Tooltip and axis formatting use simple formatter functions — no D3 scale knowledge required.
- TypeScript types are provided by `recharts` without a separate `@types` package.

**Trade-offs:**
- Recharts controls the SVG structure; custom shapes or unusual chart types require dropping to D3 internals or forking component code.
- Recharts' animation library (react-spring internally) occasionally causes layout jank on slow devices.
- Recharts v2 does not support server-side rendering natively — acceptable for this SPA.
