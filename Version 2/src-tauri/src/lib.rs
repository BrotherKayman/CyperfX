use serde_json::Value;
use std::path::PathBuf;
use std::process::Command;

#[tauri::command]
fn get_system_snapshot() -> Result<Value, String> {
    let script = diagnostic_script_path()
        .ok_or_else(|| "Could not locate diagnostics/diagnose.py. Run the app from the Version 2 project folder.".to_string())?;

    // Development bridge only; bundling Python as a sidecar is a later milestone.
    let output = Command::new("python").arg(&script).output()
        .map_err(|e| format!("Could not start Python. Install Python 3 and ensure python is on PATH. Details: {e}"))?;
    if !output.status.success() {
        return Err(format!("Python diagnostic process failed: {}", String::from_utf8_lossy(&output.stderr).trim()));
    }
    serde_json::from_slice::<Value>(&output.stdout).map_err(|e| format!("Python returned invalid JSON: {e}"))
}

fn diagnostic_script_path() -> Option<PathBuf> {
    let cwd = std::env::current_dir().ok()?;
    let candidates = [
        cwd.join("diagnostics").join("diagnose.py"),
        cwd.join("..").join("diagnostics").join("diagnose.py"),
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..").join("diagnostics").join("diagnose.py"),
    ];
    candidates.into_iter().find(|path| path.is_file())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default().invoke_handler(tauri::generate_handler![get_system_snapshot])
        .run(tauri::generate_context!()).expect("error while running CyperfX Technician Console");
}