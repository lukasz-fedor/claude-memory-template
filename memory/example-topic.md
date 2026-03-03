# Debugging Notes

<!--
  EXAMPLE topic file. Keep entries brief and actionable.
  Reference from MEMORY.md index. Delete after reviewing.
-->

## Build Issues
- 2025-01-15: Hot reload ignores new CSS files — restart dev server after adding .module.css
- 2025-01-18: Path aliases (`@/components/`) work in app but fail in tests — mirror tsconfig paths in test config

## Deployment
- 2025-02-03: Preview deploys need env vars set in Vercel project settings, not just .env
- 2025-02-10: Build fails silently on Node 18 — .nvmrc enforces Node 20, CI needs matching config
- 2025-02-14: Static assets cached aggressively by CDN — add cache-busting hash to filenames
