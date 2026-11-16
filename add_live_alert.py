# -*- coding: utf-8 -*-
"""
Injects the Live High-Performance SOC Alert Simulator into ui/dashboard.html
"""

import sys
import os

HTML_PATH = os.path.join(r"c:\Users\MRUNALI\Downloads\insider_threat_detection_ueba", "ui", "dashboard.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Inject Header Button
header_target = '''        <button onclick="showDatasetModal()" class="px-3 py-1.5 bg-cyan-950 hover:bg-cyan-900 border border-cyan-700 text-cyan-300 rounded text-xs font-semibold transition flex items-center space-x-1">
          <span>📁 CERT Logs</span>
        </button>'''

header_btn_code = '''        <!-- Live SOC Threat Alert Simulator Button -->
        <button onclick="triggerLiveAlertModal(0)" id="liveAlertBtn" class="px-3 py-1.5 bg-gradient-to-r from-rose-600 via-red-600 to-rose-700 hover:from-rose-500 hover:to-red-500 border border-rose-400 text-white rounded text-xs font-bold transition flex items-center space-x-1.5 shadow-lg shadow-rose-900/60 animate-pulse">
          <span class="w-2 h-2 rounded-full bg-white animate-ping"></span>
          <span>🚨 Live SOC Alert</span>
          <span class="px-1.5 py-0.2 rounded bg-white/20 text-white text-[10px] font-mono">P1</span>
        </button>

        <button onclick="showDatasetModal()" class="px-3 py-1.5 bg-cyan-950 hover:bg-cyan-900 border border-cyan-700 text-cyan-300 rounded text-xs font-semibold transition flex items-center space-x-1">
          <span>📁 CERT Logs</span>
        </button>'''

if header_target in html and "triggerLiveAlertModal" not in html:
    html = html.replace(header_target, header_btn_code, 1)
    print("Injected header button successfully.")
else:
    print("Header button already exists or target not found.")

# 2. Inject Modal HTML before Toast Notification
toast_target = '''  <!-- Toast Notification -->'''

modal_html = '''  <!-- Live High-Performance SOC Threat Alert Modal -->
  <div id="liveAlertModal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-3 sm:p-5 overflow-y-auto">
    <div class="bg-[#0b0f19] border-2 border-rose-500/80 rounded-2xl max-w-5xl w-full p-5 sm:p-6 space-y-4 shadow-2xl shadow-rose-950/80 my-auto text-slate-100 animate-in fade-in zoom-in-95 duration-200">
      
      <!-- Top Alert Bar -->
      <div class="flex flex-wrap items-center justify-between pb-3 border-b border-rose-500/30 gap-3">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-rose-600/20 border border-rose-500 flex items-center justify-center text-rose-400 shadow-lg shadow-rose-600/30 animate-pulse">
            <span class="text-xl">🚨</span>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-extrabold text-sm sm:text-base text-rose-400 tracking-wider font-mono">FIN-SOC ZERO-TRUST THREAT INTERCEPTION</span>
              <span id="alertSeverityBadge" class="px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/40 text-xs font-mono font-bold animate-pulse">P1_CRITICAL (99.9/100)</span>
            </div>
            <p class="text-xs text-slate-400 font-mono mt-0.5">Autonomous Zero-Trust Containment Active • Response Latency &lt; 1.4s</p>
          </div>
        </div>

        <div class="flex items-center space-x-2">
          <!-- Audio Siren Toggle Button -->
          <button onclick="toggleAlertAudio()" id="alertAudioToggleBtn" class="px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 hover:border-slate-500 text-xs font-mono text-slate-300 flex items-center space-x-1.5 transition">
            <span id="alertAudioIcon">🔊</span>
            <span id="alertAudioStatus">Siren ON</span>
          </button>
          <!-- Close Button -->
          <button onclick="closeLiveAlertModal()" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center text-sm font-bold transition">
            ✕
          </button>
        </div>
      </div>

      <!-- Threat Scenario Selector Bar -->
      <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-2.5">
        <div class="text-[11px] font-mono text-slate-400 uppercase tracking-wider mb-2 flex items-center justify-between">
          <span>Select Planted Attack Scenario:</span>
          <span class="text-rose-400 font-semibold text-[10px]">4 Ground-Truth Benchmarks</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
          <button onclick="switchLiveAlertScenario(0)" id="scenBtn0" class="alert-scen-btn px-2.5 py-1.5 rounded bg-rose-950/80 border border-rose-500/80 text-rose-200 font-medium text-left truncate transition">
            <div class="font-bold text-[11px] truncate">1. Devon Reed (Retail)</div>
            <div class="text-[10px] text-slate-400 truncate">Bulk USB Exfil (3.8GB)</div>
          </button>
          <button onclick="switchLiveAlertScenario(1)" id="scenBtn1" class="alert-scen-btn px-2.5 py-1.5 rounded bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200 font-medium text-left truncate transition">
            <div class="font-bold text-[11px] truncate">2. Marcus Vance (Trading)</div>
            <div class="text-[10px] text-slate-400 truncate">Rogue Ledger & VaR</div>
          </button>
          <button onclick="switchLiveAlertScenario(2)" id="scenBtn2" class="alert-scen-btn px-2.5 py-1.5 rounded bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200 font-medium text-left truncate transition">
            <div class="font-bold text-[11px] truncate">3. Devon Reed (Core IT)</div>
            <div class="text-[10px] text-slate-400 truncate">SWIFT Wire Log Wipe</div>
          </button>
          <button onclick="switchLiveAlertScenario(3)" id="scenBtn3" class="alert-scen-btn px-2.5 py-1.5 rounded bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200 font-medium text-left truncate transition">
            <div class="font-bold text-[11px] truncate">4. Sophia Chen (Wealth)</div>
            <div class="text-[10px] text-slate-400 truncate">Cloud Staging & Poaching</div>
          </button>
        </div>
      </div>

      <!-- Quantitative Telemetry Cards Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="p-3 rounded-xl bg-slate-900/90 border border-rose-500/30">
          <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wide">Detection Latency</div>
          <div id="alertMetricLatency" class="text-xl font-bold font-mono text-rose-400 mt-0.5">142.6 ms</div>
          <div class="text-[10px] text-emerald-400 font-mono mt-0.5">⚡ Machine-Speed Closed Loop</div>
        </div>
        <div class="p-3 rounded-xl bg-slate-900/90 border border-rose-500/30">
          <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wide">12D UEBA Statistical Drift</div>
          <div id="alertMetricZScore" class="text-xl font-bold font-mono text-amber-400 mt-0.5">+18.4σ</div>
          <div class="text-[10px] text-slate-400 font-mono mt-0.5">Peer Baseline: ≤ 1.5σ</div>
        </div>
        <div class="p-3 rounded-xl bg-slate-900/90 border border-rose-500/30">
          <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wide">Bi-LSTM Recon Loss</div>
          <div id="alertMetricLoss" class="text-xl font-bold font-mono text-indigo-400 mt-0.5">0.510 MSE</div>
          <div class="text-[10px] text-slate-400 font-mono mt-0.5">Baseline: 0.021 ± 0.007</div>
        </div>
        <div class="p-3 rounded-xl bg-slate-900/90 border border-rose-500/30">
          <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wide">Financial Exposure</div>
          <div id="alertMetricExposure" class="text-xl font-bold font-mono text-rose-300 mt-0.5">$3,506,250</div>
          <div class="text-[10px] text-rose-400 font-mono mt-0.5">Est. Fraud & Legal Risk</div>
        </div>
      </div>

      <!-- Navigation Tabs Inside Modal -->
      <div class="flex items-center space-x-2 border-b border-slate-800 pb-2 text-xs font-mono">
        <button onclick="switchAlertViewTab('hud')" id="alertTabHudBtn" class="px-3 py-1.5 rounded-lg bg-rose-600 text-white font-bold flex items-center space-x-1.5 transition">
          <span>🛡️ Tactical HUD & OODA Loop</span>
        </button>
        <button onclick="switchAlertViewTab('siem')" id="alertTabSiemBtn" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 font-bold flex items-center space-x-1.5 transition">
          <span>📋 Machine SIEM JSON (Splunk/CEF)</span>
        </button>
        <button onclick="switchAlertViewTab('sar')" id="alertTabSarBtn" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 font-bold flex items-center space-x-1.5 transition">
          <span>⚖️ FinCEN SAR Form 111 Regulatory Draft</span>
        </button>
      </div>

      <!-- TAB 1: Visual Tactical HUD & OODA Deliberation -->
      <div id="alertContentHud" class="space-y-4">
        <!-- Target Info & MITRE ATT&CK Badges -->
        <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div>
            <div class="text-[11px] font-mono text-slate-400 uppercase">Actor Profile & Target Dossier:</div>
            <div class="mt-1 flex items-baseline space-x-2">
              <span id="alertTargetName" class="font-bold text-sm text-white">Devon Reed</span>
              <span id="alertTargetId" class="font-mono text-slate-400">(USR_RET_04)</span>
            </div>
            <div id="alertTargetRoleDept" class="text-slate-300 mt-0.5">Credit Analyst • Retail Banking</div>
            <div id="alertTargetTerminal" class="text-slate-400 font-mono text-[11px] mt-0.5">Terminal: PC-RET-044 (IP: 10.14.2.88)</div>
            <div id="alertTargetHr" class="text-amber-400 font-mono text-[11px] mt-1">⚠️ Active Flight Risk: Resignation Filed (2026-05-31)</div>
          </div>
          <div>
            <div class="text-[11px] font-mono text-slate-400 uppercase">MITRE ATT&CK Matrix Alignment:</div>
            <div id="alertMitreBadges" class="flex flex-wrap gap-1.5 mt-2">
              <span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 font-mono text-[11px]">T1052.001 Exfiltration Over USB</span>
              <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono text-[11px]">T1078 Valid Accounts</span>
              <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 font-mono text-[11px]">T1048 Exfil Over Protocol</span>
            </div>
            <div class="text-[11px] font-mono text-emerald-400 mt-2 flex items-center space-x-1">
              <span>🎯 Dynamic Honeypot Trap:</span>
              <span id="alertHoneypotStatus" class="font-bold">TOUCH CONFIRMED (Q4_Client_Tax_Records.xlsx)</span>
            </div>
          </div>
        </div>

        <!-- Sub-millisecond Autonomous Killswitch Timeline -->
        <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
          <div class="text-[11px] font-mono text-slate-400 uppercase flex items-center justify-between">
            <span>Machine-Speed Zero-Trust Killswitch Execution:</span>
            <span class="text-emerald-400 font-bold text-[10px]">TOTAL CONTAINMENT: 1,337 ms</span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <div class="text-slate-400 text-[10px]">Kerberos Token Revoke</div>
              <div class="text-emerald-400 font-bold">142 ms</div>
              <div class="text-[10px] text-slate-500">Active Directory TGT</div>
            </div>
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <div class="text-slate-400 text-[10px]">Host Network Isolation</div>
              <div class="text-emerald-400 font-bold">310 ms</div>
              <div class="text-[10px] text-slate-500">Microsegmentation Rule</div>
            </div>
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <div class="text-slate-400 text-[10px]">Relational Ledger Freeze</div>
              <div class="text-emerald-400 font-bold">205 ms</div>
              <div class="text-[10px] text-slate-500">Core Banking Gateway</div>
            </div>
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <div class="text-slate-400 text-[10px]">FinCEN SAR Package</div>
              <div class="text-emerald-400 font-bold">680 ms</div>
              <div class="text-[10px] text-slate-500">Form 111 XML Narrative</div>
            </div>
          </div>
        </div>

        <!-- Multi-Agent OODA Deliberation Transcript -->
        <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
          <div class="text-[11px] font-mono text-slate-400 uppercase flex items-center justify-between">
            <span>Multi-Agent OODA Loop Real-Time Deliberation:</span>
            <span class="text-cyan-400 font-bold text-[10px]">4 Autonomous Personas</span>
          </div>
          <div id="alertOodaTranscript" class="space-y-2 text-xs font-mono max-h-48 overflow-y-auto pr-1">
            <!-- Populated via JS -->
          </div>
        </div>
      </div>

      <!-- TAB 2: Machine-Speed SIEM JSON (Splunk/CEF) -->
      <div id="alertContentSiem" class="hidden space-y-3">
        <div class="flex items-center justify-between text-xs font-mono text-slate-400">
          <span>Structured SIEM Common Event Format (CEF / JSON v2.4):</span>
          <button onclick="copyAlertSiemJson()" class="px-2.5 py-1 rounded bg-cyan-950 hover:bg-cyan-900 border border-cyan-700 text-cyan-300 font-bold transition flex items-center space-x-1">
            <span>📋 Copy SIEM JSON</span>
          </button>
        </div>
        <pre id="alertSiemCodeBlock" class="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-cyan-300 overflow-x-auto max-h-96 leading-relaxed selection:bg-cyan-900"></pre>
      </div>

      <!-- TAB 3: FinCEN Form 111 SAR Regulatory Draft -->
      <div id="alertContentSar" class="hidden space-y-3">
        <div class="flex items-center justify-between text-xs font-mono text-slate-400">
          <span>U.S. Treasury FinCEN Form 111 Electronic Filing Narrative (31 CFR § 1020.320):</span>
          <button onclick="downloadAlertFinCenSar()" class="px-2.5 py-1 rounded bg-emerald-950 hover:bg-emerald-900 border border-emerald-700 text-emerald-300 font-bold transition flex items-center space-x-1">
            <span>📄 Download Official SAR (.txt)</span>
          </button>
        </div>
        <pre id="alertSarCodeBlock" class="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-emerald-300 overflow-x-auto max-h-96 leading-relaxed whitespace-pre-wrap"></pre>
      </div>

      <!-- Modal Footer Action Buttons -->
      <div class="flex flex-wrap items-center justify-between pt-3 border-t border-slate-800 gap-2">
        <div class="flex items-center space-x-2">
          <button onclick="executeInstantQuarantine()" id="alertQuarantineBtn" class="px-4 py-2 bg-gradient-to-r from-rose-700 to-red-600 hover:from-rose-600 hover:to-red-500 border border-rose-500 text-white rounded-lg text-xs font-bold transition shadow-lg shadow-rose-900/40 flex items-center space-x-1.5">
            <span>🛡️ Enforce Machine Quarantine</span>
          </button>
          <button onclick="copyAlertSiemJson()" class="px-3 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 rounded-lg text-xs font-semibold transition">
            📋 Copy JSON
          </button>
          <button onclick="downloadAlertFinCenSar()" class="px-3 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 rounded-lg text-xs font-semibold transition">
            📄 Export FinCEN SAR
          </button>
        </div>
        <button onclick="closeLiveAlertModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-semibold transition">
          ✕ Dismiss Alert
        </button>
      </div>

    </div>
  </div>

  <!-- Toast Notification -->'''

if toast_target in html and 'id="liveAlertModal"' not in html:
    html = html.replace(toast_target, modal_html, 1)
    print("Injected liveAlertModal HTML successfully.")
else:
    print("Modal HTML already exists or toast target not found.")

# 3. Inject JavaScript Logic before closing </script>
script_target = '''  </script>
</body>'''

js_code = '''    // =========================================================================
    // HIGH-PERFORMANCE LIVE SOC ALERT SIMULATOR & AUDIO SYNTHESIZER
    // =========================================================================
    let alertAudioEnabled = true;
    let audioCtx = null;
    let currentLiveAlertScenario = 0;

    const LIVE_ALERT_SCENARIOS = [
      {
        id: "ALT-2026-FIN-08492",
        title: "Bulk Customer PII Exfiltration Over Removable Media",
        user_id: "USR_RET_04",
        name: "Devon Reed",
        role: "Credit Analyst",
        department: "Retail Banking",
        terminal: "PC-RET-044 (IP: 10.14.2.88)",
        hr: "⚠️ Active Flight Risk: 30-Day Resignation Notice (2026-05-31)",
        severity: "P1_CRITICAL (99.9/100)",
        latency: "142.6 ms",
        zscore: "+18.4σ",
        recon_loss: "0.510 MSE",
        exposure: "$3,506,250",
        honeypot: "TOUCH CONFIRMED (Q4_Client_Tax_Records.xlsx)",
        mitre: ["T1052.001 Exfiltration Over USB", "T1078 Valid Accounts", "T1048 Exfil Over Protocol"],
        ooda: [
          { time: "00:00.012", agent: "AlertTriageAgent", stage: "OBSERVE", text: "Ingested anomalous weekend telemetry. 02:14 AM logon detected. Verified IT maintenance calendar: No approved maintenance scheduled. Escalated to P1_CRITICAL." },
          { time: "00:00.045", agent: "BehavioralProfilerAgent", stage: "ORIENT", text: "12D behavioral vector indicates +18.4σ volumetric drift over Retail peer cohort. Active Directory cross-reference flags pending resignation. Nexus multiplier triggered." },
          { time: "00:00.098", agent: "ActiveDeceptionAgent", stage: "DECIDE", text: "Dynamic honeypot 'Q4_Client_Tax_Records.xlsx' read event intercepted within 400ms! Malicious intent mathematically corroborated. Risk elevated to 99.9." },
          { time: "00:00.142", agent: "AutonomousResponseAgent", stage: "ACT", text: "Executing Zero-Trust Containment: Kerberos TGT revoked (142ms), Endpoint isolated (310ms), Ledger write locks placed (205ms), FinCEN SAR Form 111 auto-drafted (680ms)." }
        ]
      },
      {
        id: "ALT-2026-FIN-09104",
        title: "Unauthorized Ledger Write Locks & VaR Limit Tampering",
        user_id: "USR_TRD_02",
        name: "Marcus Vance",
        role: "Derivatives Trader",
        department: "Trading & Markets",
        terminal: "PC-TRD-BACKUP-09 (Unassigned Terminal)",
        hr: "⚠️ High Unhedged Risk: Trading Exposure Deficit Notice",
        severity: "P1_CRITICAL (95.8/100)",
        latency: "165.2 ms",
        zscore: "+14.2σ",
        recon_loss: "0.740 MSE",
        exposure: "$8,500,000",
        honeypot: "DECOY BYPASS ATTEMPT DETECTED",
        mitre: ["T1565.001 Stored Data Manipulation", "T1078 Valid Accounts", "T1562 Impair Defenses"],
        ooda: [
          { time: "00:00.015", agent: "AlertTriageAgent", stage: "OBSERVE", text: "02:45 AM authentication from unassigned backup console PC-TRD-BACKUP-09. Triggering SOX § 404 internal control violation." },
          { time: "00:00.052", agent: "BehavioralProfilerAgent", stage: "ORIENT", text: "Deep sequence autoencoder shows catastrophic reconstruction failure (0.740 vs 0.021 normal baseline). Trader is operating outside trading hours." },
          { time: "00:00.105", agent: "ForensicHunterAgent", stage: "DECIDE", text: "Exclusive write lock on core_ledger_positions.db and tampering with risk_limits_var.conf confirmed. Estimated unhedged exposure: $8.5M." },
          { time: "00:00.165", agent: "AutonomousResponseAgent", stage: "ACT", text: "Trading account suspended (88ms), Bloomberg/FIX API session keys terminated, database transaction rolled back from immutable shadow copy." }
        ]
      },
      {
        id: "ALT-2026-FIN-07319",
        title: "SWIFT Gateway Privilege Abuse & Audit Trail Wiping",
        user_id: "USR_IT_01",
        name: "Devon Reed",
        role: "Lead Database Administrator",
        department: "Core IT & Infrastructure",
        terminal: "SRV-SWIFT-GW-01 (IP: 10.14.0.12)",
        hr: "⚠️ Disciplinary Action Flag: Active Performance Improvement Plan",
        severity: "P1_CRITICAL (91.0/100)",
        latency: "189.4 ms",
        zscore: "+12.8σ",
        recon_loss: "0.485 MSE",
        exposure: "$12,400,000",
        honeypot: "TRIPWIRE TRIGGERED (WireGatewayKeys_BAK)",
        mitre: ["T1070.001 Clear Event Logs", "T1078.002 Domain Accounts", "T1068 Privilege Escalation"],
        ooda: [
          { time: "00:00.018", agent: "AlertTriageAgent", stage: "OBSERVE", text: "Direct root access detected on SWIFT wire payment gateway server outside maintenance window." },
          { time: "00:00.061", agent: "BehavioralProfilerAgent", stage: "ORIENT", text: "Employee under formal disciplinary review. Truncation command issued against db_transaction_audit.log." },
          { time: "00:00.114", agent: "ForensicHunterAgent", stage: "DECIDE", text: "Attacker attempting anti-forensics trail erasure. SWIFT CSP 2.1 mandatory immediate session eviction condition met." },
          { time: "00:00.189", agent: "AutonomousResponseAgent", stage: "ACT", text: "Root SSH session dropped, PAM credential rotation executed, immutable WORM audit logs promoted, CISO emergency alert dispatched." }
        ]
      },
      {
        id: "ALT-2026-FIN-06621",
        title: "High-Net-Worth Portfolio Cloud Staging & Poaching",
        user_id: "USR_WLT_03",
        name: "Sophia Chen",
        role: "Vice President",
        department: "Wealth Management",
        terminal: "PC-WLT-VP03 (IP: 10.14.3.44)",
        hr: "⚠️ Competitor Meeting Flag: Pre-employment background query",
        severity: "P2_HIGH (88.5/100)",
        latency: "210.1 ms",
        zscore: "+11.5σ",
        recon_loss: "0.395 MSE",
        exposure: "$5,200,000",
        honeypot: "ACTIVE TOUCH (VIP_HNW_Account_Keys.csv)",
        mitre: ["T1567.002 Exfiltration to Cloud Storage", "T1005 Data from Local System"],
        ooda: [
          { time: "00:00.020", agent: "AlertTriageAgent", stage: "OBSERVE", text: "Encrypted HTTPS multipart upload of 850 MB to external unapproved file locker detected." },
          { time: "00:00.070", agent: "BehavioralProfilerAgent", stage: "ORIENT", text: "42 High-Net-Worth private client summaries harvested within 15 minutes. Normal daily export: 0 MB." },
          { time: "00:00.128", agent: "ActiveDeceptionAgent", stage: "DECIDE", text: "Embedded watermarked canary tokens detected in outbound payload. Target competitor firm identified." },
          { time: "00:00.210", agent: "AutonomousResponseAgent", stage: "ACT", text: "Web proxy connection terminated mid-transfer, DLP token invalidated, Legal Hold lock placed on workstation." }
        ]
      }
    ];

    function playCyberAlarmSound() {
      if (!alertAudioEnabled) return;
      try {
        if (!audioCtx) {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
          audioCtx.resume();
        }
        
        // Synthesize futuristic two-tone cyber alert chime
        const now = audioCtx.currentTime;
        const osc1 = audioCtx.createOscillator();
        const osc2 = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc1.type = "sine";
        osc1.frequency.setValueAtTime(880, now);
        osc1.frequency.exponentialRampToValueAtTime(440, now + 0.15);
        osc1.frequency.setValueAtTime(880, now + 0.20);
        osc1.frequency.exponentialRampToValueAtTime(440, now + 0.35);

        osc2.type = "triangle";
        osc2.frequency.setValueAtTime(659.25, now);
        osc2.frequency.setValueAtTime(587.33, now + 0.20);

        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(audioCtx.destination);

        osc1.start(now);
        osc2.start(now);
        osc1.stop(now + 0.45);
        osc2.stop(now + 0.45);
      } catch (e) {
        console.warn("Audio Context init suppressed:", e);
      }
    }

    function toggleAlertAudio() {
      alertAudioEnabled = !alertAudioEnabled;
      document.getElementById("alertAudioIcon").innerText = alertAudioEnabled ? "🔊" : "🔇";
      document.getElementById("alertAudioStatus").innerText = alertAudioEnabled ? "Siren ON" : "Siren OFF";
      showToast(alertAudioEnabled ? "Alert sound enabled" : "Alert sound muted");
    }

    function triggerLiveAlertModal(scenarioIdx = 0) {
      currentLiveAlertScenario = scenarioIdx;
      document.getElementById("liveAlertModal").classList.remove("hidden");
      playCyberAlarmSound();
      renderLiveAlertScenario(scenarioIdx);
      switchAlertViewTab('hud');
    }

    function closeLiveAlertModal() {
      document.getElementById("liveAlertModal").classList.add("hidden");
    }

    function switchLiveAlertScenario(idx) {
      currentLiveAlertScenario = idx;
      playCyberAlarmSound();
      renderLiveAlertScenario(idx);
    }

    function renderLiveAlertScenario(idx) {
      const scen = LIVE_ALERT_SCENARIOS[idx];

      // Update Scenario Button styles
      [0, 1, 2, 3].forEach(i => {
        const btn = document.getElementById("scenBtn" + i);
        if (i === idx) {
          btn.className = "alert-scen-btn px-2.5 py-1.5 rounded bg-rose-950/80 border border-rose-500/80 text-rose-200 font-medium text-left truncate transition";
        } else {
          btn.className = "alert-scen-btn px-2.5 py-1.5 rounded bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200 font-medium text-left truncate transition";
        }
      });

      // Update Metrics
      document.getElementById("alertSeverityBadge").innerText = scen.severity;
      document.getElementById("alertMetricLatency").innerText = scen.latency;
      document.getElementById("alertMetricZScore").innerText = scen.zscore;
      document.getElementById("alertMetricLoss").innerText = scen.recon_loss;
      document.getElementById("alertMetricExposure").innerText = scen.exposure;

      // Update Actor Profile
      document.getElementById("alertTargetName").innerText = scen.name;
      document.getElementById("alertTargetId").innerText = "(" + scen.user_id + ")";
      document.getElementById("alertTargetRoleDept").innerText = scen.role + " • " + scen.department;
      document.getElementById("alertTargetTerminal").innerText = "Terminal: " + scen.terminal;
      document.getElementById("alertTargetHr").innerText = scen.hr;
      document.getElementById("alertHoneypotStatus").innerText = scen.honeypot;

      // Update MITRE badges
      const mitreContainer = document.getElementById("alertMitreBadges");
      mitreContainer.innerHTML = scen.mitre.map(m => 
        `<span class="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 font-mono text-[11px]">${m}</span>`
      ).join("");

      // Update OODA transcript
      const oodaContainer = document.getElementById("alertOodaTranscript");
      oodaContainer.innerHTML = scen.ooda.map(step => `
        <div class="p-2 rounded bg-slate-950 border border-slate-800/80">
          <div class="flex items-center space-x-2 text-[10px] text-slate-400">
            <span class="text-rose-400 font-bold">[${step.time}]</span>
            <span class="px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-300 font-bold">${step.stage}</span>
            <span class="text-slate-300 font-bold">${step.agent}</span>
          </div>
          <div class="text-[11px] text-slate-300 mt-1 pl-1 border-l-2 border-rose-500/50">${step.text}</div>
        </div>
      `).join("");

      // Generate SIEM JSON
      const siemPayload = {
        alert_id: scen.id,
        timestamp: new Date().toISOString(),
        engine: "Autonomous-UEBA-DeepSequence-v2.4",
        detection_latency_ms: parseFloat(scen.latency),
        threat_severity: scen.severity.split(" ")[0],
        actor: {
          user_id: scen.user_id,
          name: scen.name,
          role: scen.role,
          department: scen.department,
          workstation: scen.terminal
        },
        telemetry: {
          composite_risk_score: parseFloat(scen.severity.match(/\\(([0-9.]+)/)[1]),
          statistical_drift_z: scen.zscore,
          autoencoder_recon_loss_mse: parseFloat(scen.recon_loss),
          financial_exposure_usd: scen.exposure,
          deception_trap_interaction: scen.honeypot
        },
        mitre_attack: scen.mitre,
        closed_loop_actions: [
          { action: "REVOKE_KERBEROS_TGT", status: "EXECUTED", latency_ms: 142 },
          { action: "ISOLATE_HOST_FIREWALL", status: "EXECUTED", latency_ms: 310 },
          { action: "FREEZE_LEDGER_TRANSACTIONS", status: "EXECUTED", latency_ms: 205 },
          { action: "COMPILE_FINCEN_SAR_PACKAGE", status: "READY", latency_ms: 680 }
        ]
      };
      document.getElementById("alertSiemCodeBlock").innerText = JSON.stringify(siemPayload, null, 2);

      // Generate FinCEN SAR Narrative
      const sarText = 
`========================================================================================
UNITED STATES DEPARTMENT OF THE TREASURY
FINANCIAL CRIMES ENFORCEMENT NETWORK (FinCEN) — FORM 111 (SAR)
ELECTRONIC COMPLIANCE FILING NARRATIVE [31 CFR § 1020.320]
========================================================================================
FILING INSTITUTION:    MERIDIAN BANK & TRUST (FDIC #49102)
INCIDENT REFERENCE:    ${scen.id}
DATE / TIME STAMP:     ${new Date().toUTCString()}
THREAT CLASSIFICATION: UNAUTHORIZED INTRUSION & INSIDER THREAT (GLBA § 501b / SOX § 404)

PART I — SUBJECT INFORMATION:
1. Legal Name:         ${scen.name}
2. Identifier (User):  ${scen.user_id}
3. Organizational Role: ${scen.role}
4. Operating Unit:     ${scen.department}
5. Assigned Host:      ${scen.terminal}
6. HR Risk Flag:       ${scen.hr}

PART II — SUSPICIOUS ACTIVITY & FORENSIC CHRONOLOGY:
On observation date ${new Date().toISOString().split("T")[0]}, the automated User and Entity Behavior
Analytics (UEBA) engine isolated statistically anomalous operational patterns associated
with user account ${scen.user_id}.

Quantitative forensic telemetry recorded a directional positive standard score deviation
of ${scen.zscore} against established departmental peer baselines. Concurrently, the 5-day
sliding sequence autoencoder yielded a reconstruction Mean Squared Error of ${scen.recon_loss},
significantly exceeding the normal operational baseline (0.021 ± 0.007 MSE).

Adversarial intent was conclusively confirmed via dynamic active deception honeypot:
${scen.honeypot}.

Estimated potential financial exposure and legal liability is valued at ${scen.exposure}.

PART III — CLOSED-LOOP AUTONOMOUS CONTAINMENT ACTIONS:
In accordance with zero-trust cyber defense governance policies, the autonomous multi-agent
framework enacted the following machine-speed containment controls:
  1. Active Directory Kerberos Token Invalidation (142 ms)
  2. Endpoint Network Microsegmentation Isolation (310 ms)
  3. Relational Database Gateway Write Freeze (205 ms)
  4. Immutable Log Preservation & Compliance Package Compilation (680 ms)

Total containment elapsed time: 1,337 ms (~1.34 seconds).
Report electronically compiled and dispatched for authorized Chief Compliance Officer review.
========================================================================================`;
      document.getElementById("alertSarCodeBlock").innerText = sarText;
    }

    function switchAlertViewTab(tab) {
      document.getElementById("alertContentHud").classList.toggle("hidden", tab !== 'hud');
      document.getElementById("alertContentSiem").classList.toggle("hidden", tab !== 'siem');
      document.getElementById("alertContentSar").classList.toggle("hidden", tab !== 'sar');

      document.getElementById("alertTabHudBtn").className = tab === 'hud'
        ? "px-3 py-1.5 rounded-lg bg-rose-600 text-white font-bold flex items-center space-x-1.5 transition"
        : "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 font-bold flex items-center space-x-1.5 transition";

      document.getElementById("alertTabSiemBtn").className = tab === 'siem'
        ? "px-3 py-1.5 rounded-lg bg-cyan-700 text-white font-bold flex items-center space-x-1.5 transition"
        : "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 font-bold flex items-center space-x-1.5 transition";

      document.getElementById("alertTabSarBtn").className = tab === 'sar'
        ? "px-3 py-1.5 rounded-lg bg-emerald-700 text-white font-bold flex items-center space-x-1.5 transition"
        : "px-3 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 font-bold flex items-center space-x-1.5 transition";
    }

    function copyAlertSiemJson() {
      const code = document.getElementById("alertSiemCodeBlock").innerText;
      navigator.clipboard.writeText(code).then(() => {
        showToast("✓ SIEM JSON copied to clipboard!");
      }).catch(() => {
        showToast("✓ SIEM JSON ready in console");
      });
    }

    function downloadAlertFinCenSar() {
      const text = document.getElementById("alertSarCodeBlock").innerText;
      const scen = LIVE_ALERT_SCENARIOS[currentLiveAlertScenario];
      const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `FinCEN_SAR_${scen.id}_${scen.user_id}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast("✓ Downloaded FinCEN Form 111 SAR!");
    }

    function executeInstantQuarantine() {
      const btn = document.getElementById("alertQuarantineBtn");
      btn.innerHTML = `<span>⏳ Enforcing Zero-Trust Lockdown...</span>`;
      btn.className = "px-4 py-2 bg-amber-600 text-white rounded-lg text-xs font-bold transition flex items-center space-x-1.5";
      
      playCyberAlarmSound();

      setTimeout(() => {
        btn.innerHTML = `<span>✓ MACHINE QUARANTINED (100%)</span>`;
        btn.className = "px-4 py-2 bg-emerald-600 text-white rounded-lg text-xs font-bold transition flex items-center space-x-1.5";
        showToast("🛡️ Zero-Trust Quarantine Enforced across all endpoints!");
      }, 700);
    }

  </script>
</body>'''

if script_target in html and 'HIGH-PERFORMANCE LIVE SOC ALERT SIMULATOR' not in html:
    html = html.replace(script_target, js_code, 1)
    print("Injected JS logic successfully.")
else:
    print("JS logic already exists or script target not found.")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated dashboard.html successfully! Total size:", len(html))
