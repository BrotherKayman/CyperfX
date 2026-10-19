# Version 2 architecture

- `src/` — React + TypeScript technician dashboard.
- `src-tauri/` — Tauri 2 / Rust desktop shell and command bridge.
- `diagnostics/` — Python read-only system inventory.
- `native/c/` — reserved native C diagnostics layer; not active yet.
- `tests/` — automated test suite placeholder.

## Trust boundaries

The UI calls a single Tauri command. The Rust command launches the local Python script and parses JSON. Do not pass arbitrary commands or user-supplied executable paths through this bridge. The first version reads system information only. Offline packaging, stable drive identifiers, SMART data, malware signatures, scan cancellation, and reports are later milestones.