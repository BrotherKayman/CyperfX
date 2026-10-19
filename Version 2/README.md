# CyperfX — Version 2

Windows-first, local-first technician diagnostics application built brick by brick with **Tauri 2 + React + TypeScript + Python + C**.

## Current milestone: application template

This directory is an isolated Version 2 scaffold. It does not replace or modify the existing CyperfX application outside this folder.

### Stack
- **Desktop shell:** Tauri 2 / Rust
- **UI:** React + TypeScript + Vite
- **Diagnostics engine:** Python 3 (read-only system inventory to start)
- **Native systems layer:** C scaffold for later, carefully scoped low-level diagnostics

### Prerequisites (Windows)
1. Node.js LTS
2. Rust toolchain
3. Microsoft C++ Build Tools and Windows SDK
4. Python 3.11+
5. Git

See Tauri's Windows prerequisites: https://v2.tauri.app/start/prerequisites/

### Run locally
From this `Version 2` directory:

```powershell
npm install
python -m pip install -r diagnostics/requirements.txt
npm run tauri dev
```

The development bridge invokes Python for a **read-only** system snapshot. If the Python command on your machine is `py` rather than `python`, update `src-tauri/src/lib.rs` accordingly.

### Important current limitations
- This is a development scaffold, not a packaged production build.
- Python is invoked from the host environment; bundling Python for fully offline installation is a later packaging task.
- No malware detection, disk surface testing, SMART interpretation, repair, quarantine, or deletion is implemented yet.
- The C folder is a scaffold only and is not compiled or invoked.
- Diagnostic output is informational and must not be treated as a definitive hardware or security verdict.

### Build sequence
1. Application shell and system dashboard (current)
2. Physical drive inventory and read-only health signals
3. Explicitly initiated local threat scanning with explainable findings
4. Diagnostic history and exportable reports
5. Offline packaging, permissions review, and test coverage

**Safety rule:** diagnostics remain read-only by default. Any future repair or quarantine action must require an explicit technician confirmation.
