# Financial Insider Threat Detection & Autonomous Response Platform
### Powered by UEBA, CERT Dataset, Deep Learning, and Agentic AI

[![Compliance](https://img.shields.io/badge/Compliance-GLBA%20501(b)%20%7C%20SOX%20404%20%7C%20PCI--DSS%2010.2%20%7C%20SWIFT%20CSP-emerald)](#regulatory-compliance-mapping)
[![Model](https://img.shields.io/badge/Model-Bi--LSTM%20%2F%20Deep%20Sequence%20Autoencoder-cyan)](#deep-learning-sequence-anomaly-detection)
[![Agents](https://img.shields.io/badge/Agentic%20AI-OODA%20Autonomous%20SOC%20Team-indigo)](#agentic-ai-autonomous-soc-system)
[![Recall](https://img.shields.io/badge/CERT%20Recall-100%25%20(4%2F4%20Threats)-rose)](#evaluation--detection-performance)

---

## Executive Overview

In Banking & Capital Markets, insider threats are among the most financially catastrophic cyber risks. Insiders hold legitimate credentials, understand internal controls, and operate within authorized networks. Traditional rule-based Data Loss Prevention (DLP) and Security Information and Event Management (SIEM) systems fail because:
1. **Static Threshold Blindness**: Thresholds cannot differentiate between legitimate high-volume quarter-end reporting and malicious bulk customer PII exfiltration.
2. **Temporal Sequence Invisibility**: Attacks unfold across subtle multi-day sequences (off-hours logon $\rightarrow$ staging $\rightarrow$ removable drive connect $\rightarrow$ encrypted dispatch) where each individual step appears benign in isolation.
3. **Alert Fatigue & Slow Containment**: Security analysts take an average of 85 days to contain insider incidents (Ponemon Institute), exposing financial institutions to millions in fraud, regulatory fines, and reputation loss.

This platform provides an end-to-end, enterprise-grade solution uniting **CMU CERT multi-modal telemetry**, **User and Entity Behavior Analytics (UEBA)**, **Deep Learning sequence modeling (Bi-LSTM / Deep Autoencoder)**, and an **Agentic AI autonomous SOC response team**.

---

## System Architecture

```
                      [ CERT Banking & Finance Multi-Modal Logs ]
            (Logon, Removable Device, File Access, Email Exfiltration, HTTP)
                                     │
                                     ▼
                   ┌───────────────────────────────────┐
                   │  1. Ingestion & Feature Extractor  │
                   │     - 12D Behavioral Feature Vector│
                   │     - Temporal daily aggregation   │
                   └─────────────────┬─────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
    ┌─────────────────────────┐             ┌─────────────────────────┐
    │ 2. UEBA Profiling Engine│             │ 3. Deep Learning Engine │
    │  - Statistical baseline │             │  - Bi-LSTM Autoencoder  │
    │  - Peer group deviation │             │  - Reconstruction error │
    │  - Compound nexus boost │             │  - Multi-day sequence   │
    └────────────┬────────────┘             └────────────┬────────────┘
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     ▼
                   ┌───────────────────────────────────┐
                   │     4. Hybrid Risk Fusion Engine  │
                   │  R_final = α·R_UEBA + (1-α)·R_DL  │
                   │  + Context Boost (HR/Privilege)   │
                   └─────────────────┬─────────────────┘
                                     ▼ (Alert Threshold Exceeded)
    ┌─────────────────────────────────────────────────────────────────┐
    │ 5. Agentic AI Autonomous Incident Response & Deliberation       │
    │  ┌───────────────────────┐       ┌───────────────────────────┐  │
    │  │  Alert Triage Agent   │ ────> │ Behavioral Profiler Agent │  │
    │  │  (Priority & Filter)  │       │  (Identity & Cohort Norms)│  │
    │  └──────────┬────────────┘       └─────────────┬─────────────┘  │
    │             │                                  │                │
    │             ▼                                  ▼                │
    │  ┌───────────────────────┐       ┌───────────────────────────┐  │
    │  │ Forensic Hunter Agent │ ────> │ Autonomous Response Agent │  │
    │  │ (Multi-Modal Chains)  │       │ (Zero-Trust & SAR Report) │  │
    │  └───────────────────────┘       └─────────────┬─────────────┘  │
    │                                                │                │
    │                                                ▼                │
    │                                   [ Banking Compliance Action ]  │
    │                                  (Revoke Session, Freeze SWIFT, │
    │                                   Draft FinCEN SAR Form 111)    │
    └────────────────────────────────┬────────────────────────────────┘
                                     ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │ 6. Interactive Executive & Analyst Web Dashboard (Generative UI)│
    │    - Real-time Threat Stream   - UEBA Peer Radar & Z-Scores     │
    │    - Deep Learning Error Curve - Agent Deliberation Transcript  │
    │    - One-click Incident Triage & Human-in-the-Loop Remediation  │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Core System Modules

### 1. Data Layer: CERT Dataset & Banking Scenario Generator (`data/`)
- Implements strict schemas conforming to CMU CERT Insider Threat data standards:
  - `logon.csv`: Authentication events, workstations, source IPs, auth method.
  - `device.csv`: Removable USB media connects, serials, data transferred in MB.
  - `file.csv`: File open, read, copy, modify, delete with sensitivity classifications.
  - `email.csv`: Internal vs external recipients, attachment sizes, encryption flags.
  - `http.csv`: Web navigation, domain categories (Cloud Storage, Dark Web, Intranet), uploaded bytes.
  - `ldap.csv`: Active Directory metadata (department, clearance level, supervisor, resignation status, performance rating).
- Simulates realistic 30-day enterprise baseline behavior across 5 financial departments:
  * Retail Banking, Trading & Markets, Wealth Management, Core IT/DBA, Compliance.

### 2. UEBA Profiling Engine (`ueba/`)
- Aggregates atomic events into a **12-dimensional daily behavioral vector**:
  `total_logons`, `after_hours_logons`, `distinct_workstations`, `usb_connect_events`, `usb_data_volume_mb`, `files_accessed_count`, `sensitive_files_accessed`, `file_mod_del_events`, `external_emails_sent`, `email_attachments_mb`, `cloud_storage_uploads_mb`, `abnormal_workstation_used`.
- Computes **Peer Group Cohort Baselines** ($\mu_{peer}, \sigma_{peer}$) and **Individual Historical Baselines** ($\mu_{self}, \sigma_{self}$).
- Calculates multidimensional positive Z-scores:
  $$Z_f = 0.4 \cdot Z_{peer, f} + 0.6 \cdot Z_{self, f}$$
- Detects **Compound Threat Nexuses** (e.g. Off-hours login + Sensitive file access + Removable drive staging = non-linear risk multiplier).

### 3. Deep Learning Sequence Anomaly Detection (`models/`)
- **Architecture**: Temporal Sequence Autoencoder (sliding window $W = 5$ days, input dimension $W \times D = 60$).
- **Dual-Engine Implementation**:
  - Automatically utilizes **PyTorch Bi-LSTM Autoencoder** if available.
  - Features an embedded, vectorized **NumPy Deep Autoencoder** with Xavier initialization, Tanh/Linear projections, and gradient clipping for zero-dependency execution on any machine.
- Reconstructs normal behavioral trajectories; anomalies generate high reconstruction errors:
  $$\text{MSE}(X, \hat{X}) = \frac{1}{D} \sum_{j=1}^D (x_{t, j} - \hat{x}_{t, j})^2$$

### 4. Hybrid Risk Fusion & Regulatory Mapping (`models/hybrid_scorer.py`)
- Combines UEBA and Deep Learning scores with financial domain heuristics:
  $$\text{Score}_{hybrid} = 0.55 \cdot \text{Score}_{UEBA} + 0.45 \cdot \text{Score}_{DL} + \text{ContextBoost}$$
- Contextual boosts include pending employee resignation ($+12$), disciplinary PIP status ($+8$), and administrative/trading privileges ($+5$ to $+6$).
- Categorizes threat into tiers: `BENIGN` ($<40$), `SUSPICIOUS` ($40-64$), `HIGH_RISK` ($65-79$), `CRITICAL` ($\ge 80$).

### 5. Agentic AI Autonomous Incident Response Team (`agents/`)
Specialized agents operating in an **OODA (Observe-Orient-Decide-Act)** deliberation loop:
1. **AlertTriageAgent**: Tier-1 intake specialist, evaluates incoming alerts, filters planned maintenance false positives, sets P1-P4 priority.
2. **BehavioralProfilerAgent**: Identity & psychology specialist, analyzes peer group deviation, motive factors (resignation date, PIP review).
3. **ForensicHunterAgent**: Forensic investigator, stitches multi-modal logs into chronological kill-chains and maps to **MITRE ATT&CK for Enterprise** techniques.
4. **AutonomousResponseAgent**: Incident commander, executes zero-trust policy containment (Kerberos token revocation, host quarantine, SWIFT freeze) and drafts **FinCEN Form 111 SAR (Suspicious Activity Report)**.
5. **SOCOrchestrator**: Supervisors multi-agent debate, synthesizes evidence into an Executive Incident Dossier.

---

## Planted Banking Insider Threat Scenarios

| Scenario | Threat Actor | Role & Department | Attack Signature & Tactics | MITRE ATT&CK | Regulatory Impact |
|---|---|---|---|---|---|
| **1. Pre-resignation Data Theft** | Alice Walker (`USR_RET_04`) | Senior Loan Officer, Retail Banking | Resigned on Day 20. Off-hours weekend logons, mass read of 18 customer SSN files, 3.85 GB copied to SanDisk USB, encrypted ZIP dispatched to personal ProtonMail. | T1078, T1052, T1567, T1005 | GLBA 501(b), PCI-DSS 10.2 |
| **2. Rogue Trading & Ledger Tampering** | Marcus Vance (`USR_TRD_02`) | Derivatives Trader, Trading & Markets | Incurred off-book trading loss. 02:45 AM logon from abnormal backup terminal, direct write locks on `core_ledger_positions.db`, tampering with VaR limit configs. | T1078, T1565.001, T1083 | SOX 404, FINRA Rule 3110 |
| **3. Core IT Privilege Abuse & Sabotage** | Devon Reed (`USR_IT_01`) | Lead DBA, Core IT & Infrastructure | Disgruntled under PIP review. Lateral elevation to SWIFT gateway server, deleted Windows event audit logs (`db_transaction_audit.log`), staged encrypted SWIFT private keys. | T1078, T1070.001, T1552 | SWIFT CSP Control 2.1, FFIEC |
| **4. Client Poaching via Cloud Storage** | Sophia Chen (`USR_WLT_03`) | VP Wealth Management | Defecting to competitor hedge fund. Mass harvesting of high-net-worth portfolio PDFs and tax archives, 850 MB uploaded to Mega.nz cloud storage via HTTP POST. | T1005, T1567.002 | SEC Reg S-P, GLBA |

---

## Regulatory Compliance Mapping

| Financial Regulation | Mandate | How the Platform Enforces It |
|---|---|---|
| **GLBA 501(b)** (Gramm-Leach-Bliley Act) | Financial institutions must protect customer records and PII from unauthorized access or exfiltration. | Real-time USB data transfer monitoring, automated Kerberos session termination, and network host isolation. |
| **SOX Section 404** (Sarbanes-Oxley) | Requires internal controls over financial accounting records and audit integrity. | Detects unauthorized off-hours ledger modifications, unassigned workstation logins, and risk parameter alterations. |
| **PCI-DSS Req 10.2** | Track and monitor all access to cardholder data and network resources. | Correlates user-level file access and network egress with baseline peer distributions. |
| **SWIFT CSP 2.1 & 6.4** | Prevent unauthorized privilege escalation and audit log tampering on financial messaging systems. | Immediate detection and containment of administrative tampering with audit logs or wire gateway terminals. |
| **FinCEN Form 111 (SAR)** | Federal requirement to file a Suspicious Activity Report for unauthorized computer intrusion. | Agentic AI automatically synthesizes forensic evidence into complete SAR filing narratives. |

---

## Directory Structure

```
insider_threat_detection_ueba/
├── data/
│   ├── __init__.py
│   ├── cert_schema.py             # Standard CERT dataclasses & CSV exporter
│   └── banking_cert_generator.py   # Multi-modal enterprise log synthesizer
├── ueba/
│   ├── __init__.py
│   ├── features.py                # 12D behavioral feature extractor
│   └── engine.py                  # Peer baseline & multivariate Z-score profiler
├── models/
│   ├── __init__.py
│   ├── deep_anomaly_detector.py   # Bi-LSTM / Deep Sequence Autoencoder
│   └── hybrid_scorer.py           # Multi-model risk fusion & compliance scorer
├── agents/
│   ├── __init__.py
│   ├── base_agent.py              # OODA loop & message structures
│   └── soc_agents.py              # Triage, Profiler, Hunter, Response & Orchestrator
├── ui/
│   └── dashboard.html             # Standalone Cyber SOC interactive web dashboard
├── tests/
│   ├── __init__.py
│   └── test_system.py             # Comprehensive unit and integration test suite
├── pipeline.py                    # Master CLI pipeline runner
└── README.md                      # Documentation & compliance guide
```

---

## Quickstart & Usage

### 1. Run Master Detection Pipeline
Execute the full simulation and detection pipeline:
```bash
python pipeline.py --days 30 --output-dir ./output
```
This generates the CERT dataset, fits UEBA and Deep Learning models, dispatches incidents to Agentic AI, verifies detection against ground-truth scenarios, and outputs structured intelligence to `./output/threat_intelligence.json`.

### 2. Run Automated Test Suite
Verify system components and detection mechanics:
```bash
python -m unittest tests/test_system.py
```

### 3. Open Interactive SOC Dashboard
Open `ui/dashboard.html` (or the side-pane artifact `financial_soc_dashboard.html`) in any modern web browser:
- Filter active incidents across banking units.
- Inspect real-time **UEBA Radar Z-score deviations**.
- Review **Deep Learning sequence reconstruction loss curves**.
- Follow **Agentic AI deliberation transcripts** in real time.
- Review and transmit automated **FinCEN Form 111 SAR filings**.
- Test human-in-the-loop containment buttons (Token Revocation, Host Isolation).
