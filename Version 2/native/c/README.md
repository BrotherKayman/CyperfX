# Native C diagnostics layer

This folder reserves the place for a future native C module. It is not compiled or invoked in the initial scaffold.

Potential scoped uses include Windows system-information helpers and physical-drive enumeration when higher-level libraries do not expose required data. Define interfaces, validation, memory ownership, error handling and tests before adding native code. Keep diagnostics read-only by default; no automatic repair, destructive disk operations, stealth, or unconfirmed quarantine.