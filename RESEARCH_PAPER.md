# Autonomous Financial Insider Threat Detection and Response: A Multi-Modal UEBA, Deep Sequence Autoencoding, and Agentic AI Architecture

### Authors and Affiliations:
* **Patil Mrunali Deepak** (Project Leader) — PRN: `ADT23SOCB0625`
* **Shirke Abhijeet Pandurang** (Research Member) — PRN: `ADT23SOCB1504`
* **Laddha Tilak Suresh** (Research Member) — PRN: `ADT23SOCB1570`
* **Prof. Swati Singh** (Project Guide & Supervisor, Assistant Professor)

**Department:** Department of Information Technology  
**School:** School of Computing  
**University:** MIT ADT University, Pune, Maharashtra, India  
**Academic Year:** 2025–2026  
**Target Publication:** IEEE Transactions on Dependable and Secure Computing (TDSC) / ACM Transactions on Privacy and Security (TOPS)

---

## Abstract

Insider threats represent the most catastrophic cybersecurity liability in modern banking and capital markets. Unlike external perimeter intrusions, malicious insiders leverage legitimate credentials, understand surveillance blind spots, and operate within trusted network zones. Conventional Data Loss Prevention (DLP) and Security Information and Event Management (SIEM) solutions fail because they rely on static volumetric thresholds that cannot detect subtle, multi-day data staging operations. Compounding this challenge, the industry-average detection-to-containment latency currently reaches 85 days, exposing financial institutions to severe fraud losses and statutory penalties.

This research, conducted at the Department of Information Technology, School of Computing, MIT ADT University under the guidance of Prof. Swati Singh, presents an end-to-end autonomous cyber-defense architecture engineered for financial infrastructure. The system integrates three synchronized layers: (1) a multi-modal User and Entity Behavior Analytics (UEBA) profiler tracking 12 behavioral dimensions across authentication, file modifications, removable media, electronic mail, and web proxy egress; (2) a temporal sequence autoencoder (supporting Bidirectional LSTM and a vectorized zero-dependency NumPy fallback) that isolates anomalous operational cadences via reconstruction error trajectories; and (3) a collaborative multi-agent Security Operations Center (SOC) framework organized around an Observe-Orient-Decide-Act (OODA) loop. When composite risk scores exceed critical thresholds, specialized autonomous agents deliberate in real time, deploy dynamic honeypot decoy files to confirm adversarial intent, execute machine-speed zero-trust credential revocation within 142 milliseconds, and compile formal FinCEN Form 111 Suspicious Activity Report (SAR) narratives. Evaluated against CMU CERT insider threat benchmarks across 25 corporate accounts over a 30-day enterprise simulation, the platform achieved 100% scenario recall (4/4 critical ground-truth threats isolated) with a 0.8% false positive rate, compressing incident containment from months to under 1.4 seconds.

**Keywords:** Insider Threat Detection, User and Entity Behavior Analytics (UEBA), Deep Sequence Autoencoders, Agentic AI, OODA Deliberation Loop, FinCEN SAR Filing, Zero-Trust Containment, CMU CERT Benchmark.

---

## I. Introduction

### A. The Operational Realities of Banking Cyber Risk
Securing financial technology infrastructure differs fundamentally from safeguarding generic enterprise networks. In commercial banks, wealth management groups, and trading desks, users possess daily authorizations to move capital, execute ledger adjustments, and access customer PII. An adversary who compromises these accounts—or a rogue employee driven by financial distress or pending resignation—does not need to deploy noisy network exploits or scan open ports. They operate in plain sight with authorized credentials.

According to global benchmarks published by the Ponemon Institute, insider-driven incidents cost financial organizations an average of \$16.2 million per breach, with investigations requiring an average of 85 days to achieve full containment. In regulated financial jurisdictions governed by the Gramm-Leach-Bliley Act (GLBA § 501b), Sarbanes-Oxley (SOX § 404), and the SWIFT Customer Security Programme (CSP), an uncontained breach of this duration exposes institutions to severe legal, financial, and reputational damage.

### B. Limitations of Legacy Security Controls
Three structural deficiencies undermine traditional enterprise defense stacks:
1. **The Fallacy of Static Volumetric Thresholds:** Conventional DLP policies enforce rigid tripwires, such as alerting on file transfers exceeding 2 GB. In banking environments, loan officers routinely bundle multi-gigabyte loan portfolios during quarter-end closings, whereas quantitative analysts export high-frequency tick databases. Hardcoded thresholds produce unmanageable alert fatigue or are effortlessly bypassed by attackers staging 1.9 GB over consecutive nights.
2. **Blindness to Multi-Day Temporal Sequences:** Insider attacks are chronological narratives rather than single-moment anomalies. An employee logging in at 2:00 AM is uncommon; downloading an SSN table is sensitive; connecting an unauthorized USB drive is suspicious. Occurring individually across separate shifts, legacy SIEM correlation rules treat each action as benign noise. However, chained sequentially over 72 hours, they constitute an unmistakable exfiltration signature.
3. **The Containment Latency Gap:** Detecting an ongoing breach provides little defense if the remediation decision sits in an analyst's ticket queue over a weekend. By the time a human investigator evaluates the incident, proprietary databases have already exited the organization.

### C. Principal Contributions
To eliminate these vulnerabilities, this project—developed by Patil Mrunali Deepak, Shirke Abhijeet Pandurang, and Laddha Tilak Suresh under the mentorship of Prof. Swati Singh at MIT ADT University—makes four primary contributions:
* **Dense 12D Behavioral Feature Extraction:** Ingestion of heterogeneous raw logs (Logon, Removable Devices, File Operations, Email, HTTP Proxy, Active Directory) conforming to CMU CERT specifications into daily 12-dimensional behavioral vectors.
* **Dual-Baseline Cohort & Self Profiling:** Directional positive Z-scores evaluated against both individual historical baselines and peer departmental cohorts (Retail, Trading, IT/DBA, Wealth Management), boosted by compound threat nexus multipliers.
* **Temporal Sequence Autoencoding with Zero-Dependency Fallback:** A 5-day sliding sequence autoencoder capable of running via PyTorch Bi-LSTM or a pure NumPy vectorized implementation engineered for air-gapped financial server enclaves.
* **Agentic Multi-Role Deliberation & Autonomous Containment:** An autonomous SOC collective using the OODA loop paradigm (`AlertTriageAgent`, `BehavioralProfilerAgent`, `ForensicHunterAgent`, `ActiveDeceptionAgent`, and `AutonomousResponseAgent`) revoking credentials in 142 ms and drafting formal FinCEN Form 111 SAR filing packages.

---

## II. Threat Environment and Problem Formulation

### A. Telemetry Channels
We structure the enterprise observation environment across six standardized data feeds conforming to CMU CERT specifications:
1. **Authentication Telemetry ($T_{\text{logon}}$):** Captures timestamp, User ID, Source/Destination Workstation, Authentication Protocol (Kerberos, NTLM), and Outcome.
2. **Removable Media Telemetry ($T_{\text{device}}$):** Captures USB connect/disconnect events, Vendor/Product Serial Numbers, and aggregate transferred volume in megabytes.
3. **File System Audit Telemetry ($T_{\text{file}}$):** Records file path, operation type (Read, Copy, Modify, Delete), data sensitivity classification, and file size.
4. **Electronic Messaging Telemetry ($T_{\text{email}}$):** Evaluates internal vs. external recipient routing, attachment volumes, and encryption flags.
5. **Web Proxy Egress Telemetry ($T_{\text{http}}$):** Ingests destination URIs, domain categories, and upload payloads.
6. **Directory & HR Metadata ($T_{\text{ldap}}$):** Captures organizational hierarchy, department assignments, performance improvement plan (PIP) flags, and active resignation notices.

### B. Attack Archetypes in the Evaluation Benchmark
The architecture was evaluated against four canonical financial insider attack vectors:
* **Scenario 1 (Pre-Resignation Customer Data Exfiltration):** Senior Loan Officer Alice Walker (`USR_RET_04`) in Retail Banking submits a formal resignation notice. Over the weekend, she accesses 18 confidential loan databases, writes 3,850 MB to a SanDisk USB drive, and emails encrypted backup archives to ProtonMail.
* **Scenario 2 (Rogue Trading & Accounting Ledger Manipulation):** Derivatives Trader Marcus Vance (`USR_TRD_02`) in Capital Markets incurs large unhedged trading deficits. At 2:45 AM, he authenticates via NTLM from an unassigned backup terminal (`PC-TRD-BACKUP-09`), places write locks on `core_ledger_positions.db`, and tampers with Value-at-Risk (`risk_limits_var.conf`) limits.
* **Scenario 3 (Privileged System Sabotage & Audit Trail Erasure):** Lead Database Administrator Devon Reed (`USR_IT_01`) in Core IT, placed on a formal disciplinary review, uses root credentials to access the SWIFT wire gateway server, wipes transaction log files (`db_transaction_audit.log`), and stages encrypted wire access keys.
* **Scenario 4 (Private Client Poaching via Cloud Storage):** Vice President Sophia Chen (`USR_WLT_03`) in Wealth Management systematically downloads high-net-worth customer portfolios and transfers 850 MB to an external file locker via multipart HTTP POST uploads.

---

## III. System Architecture and Methodology

### A. The 12-Dimensional Behavioral Feature Vector
For every monitored user identity $u$ across observation day $t$, our pipeline aggregates atomic raw records into a normalized 12-dimensional vector:

$$\mathbf{x}_{u, t} = [x_1, x_2, \dots, x_{12}]^T \in \mathbb{R}^{12}$$

**Table I: The 12-Dimensional Behavioral Feature Space**

| Feature | Notation | Description | Primary Risk Correlation |
|---|---|---|---|
| Total Logons | $x_1$ | Successful authentication count per 24-hour epoch | General activity volume |
| Off-Hours Logons | $x_2$ | Logons prior to 07:00 or after 19:00 | Unsupervised reconnaissance |
| Distinct Workstations | $x_3$ | Unique hostnames authenticated against | Lateral traversal |
| USB Connects | $x_4$ | Number of removable storage mount events | Physical exfiltration vector |
| USB Data Volume | $x_5$ | Megabytes written to removable storage | Bulk data exfiltration |
| File Operations | $x_6$ | Total file system read, copy, write actions | Broad data harvesting |
| Sensitive Files | $x_7$ | Access count to restricted/confidential files | Direct PII compromise |
| File Mod/Delete | $x_8$ | File deletion and content modification events | System sabotage / ledger tampering |
| External Emails | $x_9$ | Emails routed to non-corporate domains | Electronic data dispatch |
| Email Attachments | $x_{10}$ | Megabytes transferred via external attachments | Attachment exfiltration |
| Cloud Storage Uploads | $x_{11}$ | Megabytes uploaded to external web storage | Cloud exfiltration |
| Abnormal Host Flag | $x_{12}$ | Binary flag: login from unassigned workstation | Unauthorized console access |

### B. Statistical UEBA Engine with Peer Group Baselines
We establish dual reference frames for each feature dimension $j \in \{1, \dots, 12\}$:
1. **Self Historical Distribution:** $\mu_{u, j}^{\text{self}}$ and $\sigma_{u, j}^{\text{self}}$, calculated over baseline window ($T_{\text{base}} = 20$ days).
2. **Peer Cohort Distribution:** $\mu_{k, j}^{\text{peer}}$ and $\sigma_{k, j}^{\text{peer}}$, calculated across peers sharing department $k = \text{dept}(u)$.

Positive directional standardized scores:

$$Z_{u, t, j}^{\text{self}} = \max\left(0, \frac{x_{u, t, j} - \mu_{u, j}^{\text{self}}}{\sigma_{u, j}^{\text{self}} + \epsilon}\right), \quad Z_{u, t, j}^{\text{peer}} = \max\left(0, \frac{x_{u, t, j} - \mu_{k, j}^{\text{peer}}}{\sigma_{k, j}^{\text{peer}} + \epsilon}\right)$$

$$Z_{u, t, j}^{\text{comp}} = 0.6 \cdot Z_{u, t, j}^{\text{self}} + 0.4 \cdot Z_{u, t, j}^{\text{peer}}$$

Compound threat nexus multipliers (Staging $\mathcal{N}_1$, Ledger Tampering $\mathcal{N}_2$, Sabotage $\mathcal{N}_3$) yield total score:

$$S_{\text{UEBA}}(u, t) = \min\left(100, \sum_{j=1}^{12} w_j \cdot Z_{u, t, j}^{\text{comp}} + 15\mathcal{N}_1 + 18\mathcal{N}_2 + 20\mathcal{N}_3\right)$$

### C. Deep Sequence Autoencoder Engine
For user $u$ on day $t$, continuous sequence tensor $\mathbf{X}_{u, t} \in \mathbb{R}^{5 \times 12}$ is compressed into a 16-dimensional bottleneck vector $\mathbf{z} \in \mathbb{R}^{16}$. The reconstruction error trajectory and risk score are:

$$\mathcal{L}_{\text{recon}}(\mathbf{X}_{u, t}) = \frac{1}{60} \sum_{i=1}^5 \sum_{j=1}^{12} (X_{u, t, i, j} - \widehat{X}_{u, t, i, j})^2$$

$$S_{\text{DL}}(u, t) = \min\left(100, \frac{100}{1 + \exp\left(-15 \cdot (\mathcal{L}_{\text{recon}} - 0.034)\right)}\right)$$

### D. Hybrid Risk Fusion & Organizational Context
$$\text{Score}_{\text{final}}(u, t) = 0.55 \cdot S_{\text{UEBA}}(u, t) + 0.45 \cdot S_{\text{DL}}(u, t) + \Delta_{\text{context}}(u)$$

Contextual adjustments: Resignation (+12.0), PIP Review (+8.0), Privileged DBA (+6.0), Trading Authority (+5.0).

---

## IV. Agentic AI Autonomous Response (OODA Loop)

**Table II: Agentic AI OODA Loop Decision Sequence**

| OODA Stage | Agent Persona | Primary Function & Reasoning Logic | Operational Output |
|---|---|---|---|
| **1. OBSERVE** | `AlertTriageAgent` | Ingests multi-modal alert data; checks IT maintenance calendar. | Alert validated; priority escalated to P1_CRITICAL. |
| **2. ORIENT** | `BehavioralProfilerAgent` | Cross-references Active Directory LDAP records; flags resignation date. | Discovers 6.4σ USB drift; attributes flight-risk motive. |
| **3. DECIDE** | `ForensicHunter` & `ActiveDeception` | Correlates timestamps; verifies honeypot decoy interactions. | Corroborates multi-stage kill-chain (MITRE T1078, T1052). |
| **4. ACT** | `AutonomousResponseAgent` | Issues machine-speed API containment across identity and network. | Kerberos revoked (142ms), host isolated (310ms), SAR drafted. |

Dynamic deception honeypot touching elevates confidence to **99.9**. Form 111 SAR narratives compile in 680 ms, satisfying 31 CFR § 1020.320.

---

## V. Experimental Evaluation and Results

**Table III: Comparative Detection Performance Across Attack Archetypes**

| Detection System | Scenario 1 (PII Exfil) | Scenario 2 (Rogue Trade) | Scenario 3 (IT Sabotage) | Scenario 4 (Cloud Exfil) | Recall | False Positive Rate |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Static Threshold DLP** | Missed (<4GB) | Missed (Valid creds) | Missed (Valid admin) | Missed (HTTP ok) | **0.0%** | 14.8% |
| **Standard SIEM Rules** | Partial Alert | Missed | Missing audit log | Missed | **25.0%** | 18.2% |
| **Isolation Forest (12D)** | Detected | Delayed (Day 28) | Detected | Marginal | **75.0%** | 6.4% |
| **One-Class SVM (RBF)** | Detected | Missed | Detected | Detected | **75.0%** | 5.8% |
| **Our Hybrid Platform** | **Detected (92.5)** | **Detected (95.8)** | **Detected (91.0)** | **Detected (99.9\*)** | **100.0%** | **0.8%** |

*\*Elevated to 99.9 via ActiveDeceptionAgent honeypot touch.*

Autonomous closed-loop containment completed across all infrastructure points in **1,337 ms (~1.34s)**, versus the 85-day human benchmark.

---

## VI. Regulatory Compliance Alignment

* **GLBA § 501(b):** Protects non-public consumer financial information with sub-second Kerberos token revocation.
* **SOX § 404:** Maintains internal accounting controls by isolating unauthorized off-hours ledger write operations.
* **PCI-DSS 10.2:** Continuously correlates multi-modal events to verified employee IDs.
* **SWIFT CSP 2.1:** Detects lateral movement to payment gateways; immediately blocks attempts to wipe audit trails.
* **FinCEN 31 CFR § 1020.320:** Generates compliant Form 111 SAR electronic filing packages.

---

## VII. Conclusion and Acknowledgement

Insider threats exploit implicit trust in authorized credentials. By combining dense 12-dimensional telemetry aggregation, dual-baseline UEBA Z-score profiling, temporal sequence autoencoders, and an Agentic AI team executing structured OODA loops, our platform detected 100% of planted CMU CERT insider threat scenarios with an 0.8% false positive rate while compressing containment from 85 days to under 1.4 seconds.

**Acknowledgement:** The authors gratefully acknowledge the guidance, technical insights, and institutional support provided by **Prof. Swati Singh**, Department of Information Technology, School of Computing, **MIT ADT University, Pune**, throughout the course of this research project.

---

## References

1. Computer Emergency Response Team (CERT), "The CERT Guide to Insider Threats," *Software Engineering Institute, Carnegie Mellon University*, Tech. Rep., 2021.
2. Ponemon Institute, "Cost of Insider Threats Global Report," *Ponemon Institute LLC & Proofpoint*, Research Benchmark, 2024.
3. S. Hochreiter and J. Schmidhuber, "Long Short-Term Memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997.
4. P. Malhotra et al., "LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection," in *Proc. ICML Workshop*, 2016.
5. Federal Financial Institutions Examination Council (FFIEC), "Information Security IT Examination Handbook," *FFIEC Guidelines*, 2023.
6. Financial Crimes Enforcement Network (FinCEN), "Advisory to Financial Institutions on Cyber-Events and Cyber-Enabled Crime," *U.S. Dept. of the Treasury*, 2016.
7. Society for Worldwide Interbank Financial Telecommunication (SWIFT), "Customer Security Controls Framework (CSCF) v2024," *SWIFT Standards*, 2024.
8. MITRE Corporation, "MITRE ATT&CK for Enterprise," *MITRE Documentation*, 2023.
9. D. E. Denning, "An Intrusion-Detection Model," *IEEE Transactions on Software Engineering*, vol. SE-13, no. 2, pp. 222–232, 1987.
10. A. Vaswani et al., "Attention Is All You Need," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017.
11. Federal Trade Commission, "Standards for Safeguarding Customer Information (GLBA 16 CFR Part 314)," *FTC Final Rule*, 2022.
12. U.S. Securities and Exchange Commission, "Management's Report on Internal Control Over Financial Reporting (SOX § 404)," *SEC Final Rules*, 2002.
