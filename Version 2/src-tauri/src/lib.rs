use serde_json::Value;
use std::path::PathBuf;
use std::process::Command;

#[tauri::command]
fn get_system_snapshot() -> Result<Value, String> {
    let script = diagnostic_script_path();
    if !script.exists() { return Err(format!("Diagnostic script not found: {}", script.display())); }
    // Development bridge only; bundle Python as a sidecar in a later milestone.
    let output = Command::new("python").arg(&script).output()
        .map_err(|e| format!("Could not start Python. Install Python 3 and ensure python is on PATH. Details: {e}"))?;
    if !output.status.success() {
        return Err(format!("Python diagnostic process failed: {}", String::from_utf8_lossy(&output.stderr).trim()));
    }
    serde_json::from_slice::<Value>(&output.stdout).map_err(|e| format!("Python returned invalid JSON: {e}"))
}
fn diagnostic_script_path() -> PathBuf {
    std::env::current_dir().unwrap_or_else(|_| PathBuf::from(".")).join("diagnostics").join("diagnose.py")
}
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default().invoke_handler(tauri::generate_handler![get_system_snapshot])
        .run(tauri::generate_context!()).expect("error while running CyperfX Technician Console");
}