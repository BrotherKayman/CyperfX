import { useEffect, useState } from "react";
import { Activity, AlertTriangle, Cpu, HardDrive, RefreshCw, ShieldCheck, MemoryStick, Monitor, CheckCircle2, CircleHelp } from "lucide-react";
import { invoke } from "@tauri-apps/api/core";

type Disk = { mountpoint: string; filesystem: string; total_gb: number; free_gb: number; used_percent: number };
type Snapshot = {
  computer_name: string; operating_system: string; os_release: string; processor: string;
  logical_processors: number; cpu_percent: number | null; memory_total_gb: number;
  memory_available_gb: number; memory_percent: number; disks: Disk[];
  battery_percent: number | null; battery_plugged_in: boolean | null;
  collected_at: string; notes: string[];
};

export default function App() {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function runDiagnosis() {
    setLoading(true); setError("");
    try { setSnapshot(await invoke<Snapshot>("get_system_snapshot")); }
    catch (e) { setError(String(e)); }
    finally { setLoading(false); }
  }
  useEffect(() => { void runDiagnosis(); }, []);

  const disk = snapshot?.disks?.[0];
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark">CX</div><div><strong>CyperfX</strong><span>TECHNICIAN CONSOLE</span></div></div>
      <div className="nav-label">WORKSPACE</div>
      <div className="nav-item active"><Activity size={17}/> Overview</div>
      <div className="nav-item muted"><HardDrive size={17}/> Drive health <span className="soon">NEXT</span></div>
      <div className="nav-item muted"><ShieldCheck size={17}/> Threat scan <span className="soon">NEXT</span></div>
      <div className="nav-item muted"><Monitor size={17}/> Reports <span className="soon">NEXT</span></div>
      <div className="sidebar-bottom"><span className="status-dot"/>Local workstation<br/><small>Read-only diagnostic mode</small></div>
    </aside>
    <main className="main-content">
      <header className="topbar"><div><div className="eyebrow">SYSTEM DIAGNOSTICS / OVERVIEW</div><h1>Computer health</h1><p>Review a live snapshot of this workstation.</p></div><button className="refresh-button" onClick={() => void runDiagnosis()} disabled={loading}><RefreshCw size={16} className={loading ? "spin" : ""}/>{loading ? "Scanning…" : "Run diagnosis"}</button></header>
      {error && <div className="error-banner"><AlertTriangle size={18}/><div><strong>Could not collect diagnostics</strong><p>{error}</p><small>Confirm Python 3 and dependencies are installed, then launch via Tauri.</small></div></div>}
      <section className="status-strip"><div className="status-icon"><CheckCircle2 size={20}/></div><div><strong>{snapshot ? "System snapshot collected" : loading ? "Collecting system information" : "Waiting for first scan"}</strong><p>{snapshot ? "Last checked " + new Date(snapshot.collected_at).toLocaleString() : "No changes will be made to this computer."}</p></div><span className="readonly-pill">READ-ONLY</span></section>
      <section className="metric-grid">
        <Metric icon={<Cpu/>} label="CPU usage" value={snapshot?.cpu_percent == null ? "—" : snapshot.cpu_percent.toFixed(0) + "%"} detail={snapshot ? snapshot.logical_processors + " logical processors" : "Awaiting scan"} percent={snapshot?.cpu_percent ?? 0}/>
        <Metric icon={<MemoryStick/>} label="Memory in use" value={snapshot ? snapshot.memory_percent.toFixed(0) + "%" : "—"} detail={snapshot ? snapshot.memory_available_gb.toFixed(1) + " GB available" : "Awaiting scan"} percent={snapshot?.memory_percent ?? 0}/>
        <Metric icon={<HardDrive/>} label="System storage" value={disk ? disk.used_percent.toFixed(0) + "%" : "—"} detail={disk ? disk.free_gb.toFixed(1) + " GB free on " + disk.mountpoint : "Awaiting scan"} percent={disk?.used_percent ?? 0}/>
      </section>
      <section className="content-grid">
        <div className="panel"><div className="panel-heading"><div><span className="eyebrow">HARDWARE & OS</span><h2>System information</h2></div><Monitor size={19}/></div>
          <InfoRow label="Computer name" value={snapshot?.computer_name ?? "—"}/><InfoRow label="Operating system" value={snapshot ? snapshot.operating_system + " " + snapshot.os_release : "—"}/><InfoRow label="Processor" value={snapshot?.processor ?? "—"}/><InfoRow label="Installed memory" value={snapshot ? snapshot.memory_total_gb.toFixed(1) + " GB" : "—"}/><InfoRow label="Battery" value={snapshot?.battery_percent == null ? "Not reported / desktop" : snapshot.battery_percent + "%" + (snapshot.battery_plugged_in ? " · Plugged in" : "")}/>
        </div>
        <div className="panel"><div className="panel-heading"><div><span className="eyebrow">INITIAL CHECK</span><h2>Observations</h2></div><CircleHelp size={19}/></div>
          {!snapshot && !error && <div className="empty-state">Collecting the first system snapshot…</div>}
          {snapshot && snapshot.notes.length === 0 && <div className="finding good"><CheckCircle2 size={18}/><div><strong>No immediate threshold warnings</strong><p>This is not a full hardware or malware scan.</p></div></div>}
          {snapshot?.notes.map((note, i) => <div className="finding warning" key={i}><AlertTriangle size={18}/><div><strong>Review recommended</strong><p>{note}</p></div></div>)}
          <div className="notice"><ShieldCheck size={17}/><p>Initial checks are indicators only. SMART drive health and threat scanning will be added as separate, evidence-based modules.</p></div>
        </div>
      </section>
      <section className="panel drive-panel"><div className="panel-heading"><div><span className="eyebrow">STORAGE INVENTORY</span><h2>Detected filesystems</h2></div><span className="count-pill">{snapshot?.disks.length ?? 0} found</span></div>
        {snapshot?.disks.length ? <div className="table-wrap"><table><thead><tr><th>Mount point</th><th>Filesystem</th><th>Capacity</th><th>Free</th><th>Used</th></tr></thead><tbody>{snapshot.disks.map(d => <tr key={d.mountpoint}><td><HardDrive size={15}/> {d.mountpoint}</td><td>{d.filesystem || "Unknown"}</td><td>{d.total_gb.toFixed(1)} GB</td><td>{d.free_gb.toFixed(1)} GB</td><td><div className="usage-cell"><div className="usage-track"><div style={{width: Math.min(d.used_percent, 100) + "%"}}/></div>{d.used_percent.toFixed(0)}%</div></td></tr>)}</tbody></table></div> : <div className="empty-state">Drive information will appear after the snapshot is collected.</div>}
      </section>
      <footer>CyperfX Version 2 <span>•</span> Local-first foundation <span>•</span> No repair or deletion actions</footer>
    </main>
  </div>;
}
function Metric({icon,label,value,detail,percent}:{icon:React.ReactNode;label:string;value:string;detail:string;percent:number}) {
  return <div className="metric-card"><div className="metric-top"><span className="metric-icon">{icon}</span><span className="eyebrow">{label}</span></div><div className="metric-value">{value}</div><div className="metric-detail">{detail}</div><div className="metric-track"><div style={{width:Math.max(0,Math.min(percent,100)) + "%"}}/></div></div>;
}
function InfoRow({label,value}:{label:string;value:string}) { return <div className="info-row"><span>{label}</span><strong>{value}</strong></div>;}