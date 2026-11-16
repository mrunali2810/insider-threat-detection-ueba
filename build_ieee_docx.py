# -*- coding: utf-8 -*-
"""
Generate IEEE Formatted Microsoft Word Document (.docx)
- Clean, 100% visible formulas (NO garbled unicode characters)
- "(Leader)" REMOVED from Patil Mrunali Deepak
- Clean author table with all 3 members + Prof. Swati Singh
- MIT ADT University, School of Computing, Dept of IT
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

OUTPUT = r"c:\Users\MRUNALI\Downloads\insider_threat_detection_ueba\IEEE_Research_Paper_Insider_Threat_Detection.docx"
DOWNLOADS_COPY = r"c:\Users\MRUNALI\Downloads\IEEE_Research_Paper_Mrunali_Patil.docx"

doc = docx.Document()

# ── Page Margins (IEEE standard: Top=0.75in, Bottom=1.0in, Left=0.625in, Right=0.625in) ──
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(0.625)
    section.right_margin = Inches(0.625)

style_normal = doc.styles['Normal']
font = style_normal.font
font.name = 'Times New Roman'
font.size = Pt(10)
font.color.rgb = RGBColor(0, 0, 0)

def set_cell_background(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

# ── Title Block (Full Width) ─────────────────────────────────────────────
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(12)
run_title = p_title.add_run(
    "Autonomous Financial Insider Threat Detection and Response:\n"
    "A Multi-Modal UEBA, Deep Sequence Autoencoding, and Agentic AI Architecture"
)
run_title.font.name = "Times New Roman"
run_title.font.size = Pt(20)
run_title.font.bold = True

# ── Authors Table (NO "(Leader)" - All equal co-authors + Guide) ─────────
author_table = doc.add_table(rows=1, cols=4)
author_table.alignment = WD_TABLE_ALIGNMENT.CENTER

authors_data = [
    ("Patil Mrunali Deepak", "PRN: ADT23SOCB0625\nDept. of Information Technology\nMIT ADT University, Pune\nmrunali.patil@mituniversity.edu.in"),
    ("Shirke Abhijeet Pandurang", "PRN: ADT23SOCB1504\nDept. of Information Technology\nMIT ADT University, Pune\nabhijeet.shirke@mituniversity.edu.in"),
    ("Laddha Tilak Suresh", "PRN: ADT23SOCB1570\nDept. of Information Technology\nMIT ADT University, Pune\ntilak.laddha@mituniversity.edu.in"),
    ("Prof. Swati Singh", "Project Guide & Supervisor\nAssistant Professor\nSchool of Computing\nMIT ADT University, Pune\nswati.singh@mituniversity.edu.in")
]

for col_idx, (name, details) in enumerate(authors_data):
    cell = author_table.cell(0, col_idx)
    set_cell_margins(cell, 40, 40, 40, 40)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    
    r_name = p.add_run(name + "\n")
    r_name.font.name = "Times New Roman"
    r_name.font.size = Pt(9.5)
    r_name.font.bold = True
    
    r_det = p.add_run(details)
    r_det.font.name = "Times New Roman"
    r_det.font.size = Pt(8)
    r_det.font.italic = True

p_space = doc.add_paragraph()
p_space.paragraph_format.space_before = Pt(8)
p_space.paragraph_format.space_after = Pt(8)

# ── Two-Column Section for the Paper Body ────────────────────────────────
body_section = doc.add_section(docx.enum.section.WD_SECTION.CONTINUOUS)
body_section.top_margin = Inches(0.75)
body_section.bottom_margin = Inches(1.0)
body_section.left_margin = Inches(0.625)
body_section.right_margin = Inches(0.625)

sectPr = body_section._sectPr
cols = OxmlElement('w:cols')
cols.set(qn('w:num'), '2')
cols.set(qn('w:space'), '720')
sectPr.append(cols)

def add_p(text, space_after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.bold = bold
    run.font.italic = italic
    return p

def add_sec_head(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.bold = True
    return p

def add_subsec_head(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.bold = True
    return p

def add_eq(eq_text, eq_num):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(eq_text + "\t\t" + eq_num)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(9.5)
    r1.font.bold = True
    return p

# ── Abstract & Index Terms ───────────────────────────────────────────────
p_abs = doc.add_paragraph()
p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_abs.paragraph_format.space_after = Pt(5)
p_abs.paragraph_format.line_spacing = 1.05
r_absh = p_abs.add_run("Abstract—")
r_absh.font.name = "Times New Roman"
r_absh.font.size = Pt(9)
r_absh.font.bold = True
r_absh.font.italic = True

r_abst = p_abs.add_run(
    "Insider threats represent the most catastrophic cybersecurity liability in modern banking and capital markets. "
    "Unlike external perimeter intrusions, malicious insiders leverage legitimate credentials, understand surveillance "
    "blind spots, and operate within trusted network zones. Conventional Data Loss Prevention (DLP) and Security "
    "Information and Event Management (SIEM) solutions fail because they rely on static volumetric thresholds that "
    "cannot detect subtle, multi-day data staging operations. Compounding this challenge, the industry-average "
    "detection-to-containment latency currently reaches 85 days, exposing financial institutions to severe fraud "
    "losses and statutory penalties.\n\n"
    "This research, conducted at the Department of Information Technology, School of Computing, MIT ADT University, "
    "presents an end-to-end autonomous cyber-defense architecture engineered for financial infrastructure under the "
    "supervision of Prof. Swati Singh. The system integrates three synchronized layers: (1) a multi-modal User and Entity "
    "Behavior Analytics (UEBA) profiler tracking 12 behavioral dimensions across authentication, file modifications, "
    "removable media, electronic mail, and web proxy egress; (2) a temporal sequence autoencoder (supporting Bidirectional "
    "LSTM and a vectorized zero-dependency NumPy fallback) that isolates anomalous operational cadences via reconstruction "
    "error trajectories; and (3) a collaborative multi-agent Security Operations Center (SOC) framework organized around an "
    "Observe-Orient-Decide-Act (OODA) loop. When composite risk scores exceed critical thresholds, specialized autonomous "
    "agents deliberate in real time, deploy dynamic honeypot decoy files to confirm adversarial intent, execute machine-speed "
    "zero-trust credential revocation within 142 milliseconds, and compile formal FinCEN Form 111 Suspicious Activity Report (SAR) "
    "narratives. Evaluated against CMU CERT insider threat benchmarks across 25 corporate accounts over a 30-day simulation, "
    "the platform achieved 100% scenario recall (4/4 critical ground-truth threats isolated) with a 0.8% false positive rate, "
    "compressing incident containment from months to under 1.4 seconds."
)
r_abst.font.name = "Times New Roman"
r_abst.font.size = Pt(9)

p_kw = doc.add_paragraph()
p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_kw.paragraph_format.space_after = Pt(10)
r_kwh = p_kw.add_run("Index Terms—")
r_kwh.font.name = "Times New Roman"
r_kwh.font.size = Pt(9)
r_kwh.font.bold = True
r_kwh.font.italic = True
r_kwt = p_kw.add_run(
    "Insider Threat Detection, User and Entity Behavior Analytics (UEBA), Deep Sequence Autoencoders, "
    "Agentic AI, OODA Deliberation Loop, FinCEN SAR Filing, Zero-Trust Containment, CMU CERT Benchmark."
)
r_kwt.font.name = "Times New Roman"
r_kwt.font.size = Pt(9)

# ── Section I: Introduction ──────────────────────────────────────────────
add_sec_head("I. INTRODUCTION")
add_subsec_head("A. The Operational Realities of Banking Cyber Risk")
add_p(
    "Securing financial technology infrastructure differs fundamentally from safeguarding generic enterprise networks. "
    "In commercial banks, wealth management groups, and trading desks, users possess daily authorizations to move capital, "
    "execute ledger adjustments, and access customer PII. An adversary who compromises these accounts—or a rogue employee "
    "driven by financial distress or pending resignation—does not need to deploy noisy network exploits or scan open ports. "
    "They operate in plain sight with authorized credentials."
)
add_p(
    "According to global benchmarks published by the Ponemon Institute, insider-driven incidents cost financial organizations "
    "an average of $16.2 million per breach, with investigations requiring an average of 85 days to achieve full containment. "
    "In regulated financial jurisdictions governed by the Gramm-Leach-Bliley Act (GLBA § 501b), Sarbanes-Oxley (SOX § 404), "
    "and the SWIFT Customer Security Programme (CSP), an uncontained breach of this duration exposes institutions to severe "
    "legal, financial, and reputational damage."
)

add_subsec_head("B. Limitations of Legacy Security Controls")
add_p(
    "Three structural deficiencies undermine traditional enterprise defense stacks:\n"
    "1) The Fallacy of Static Volumetric Thresholds: Conventional DLP policies enforce rigid tripwires, such as alerting on "
    "file transfers exceeding 2 GB. In banking environments, loan officers routinely bundle multi-gigabyte loan portfolios during "
    "quarter-end closings, whereas quantitative analysts export high-frequency tick databases. Hardcoded thresholds produce "
    "unmanageable alert fatigue or are effortlessly bypassed by attackers staging 1.9 GB over consecutive nights.\n"
    "2) Blindness to Multi-Day Temporal Sequences: Insider attacks are chronological narratives rather than single-moment anomalies. "
    "An employee logging in at 2:00 AM is uncommon; downloading an SSN table is sensitive; connecting an unauthorized USB drive is "
    "suspicious. Occurring individually across separate shifts, legacy SIEM correlation rules treat each action as benign noise. "
    "However, chained sequentially over 72 hours, they constitute an unmistakable exfiltration signature.\n"
    "3) The Containment Latency Gap: Detecting an ongoing breach provides little defense if the remediation decision sits in an "
    "analyst's ticket queue over a weekend. By the time a human investigator evaluates the incident, proprietary databases have "
    "already exited the organization."
)

add_subsec_head("C. Principal Contributions")
add_p(
    "To eliminate these vulnerabilities, this project—developed by Patil Mrunali Deepak, Shirke Abhijeet Pandurang, and "
    "Laddha Tilak Suresh under the mentorship of Prof. Swati Singh at MIT ADT University—makes four primary contributions:\n"
    "• Dense 12D Behavioral Feature Extraction: An aggregation engine ingesting heterogeneous raw logs (Logon, Devices, "
    "File Operations, Email, HTTP Proxy, Active Directory) conforming to CMU CERT specifications into daily 12-dimensional behavioral vectors.\n"
    "• Dual-Baseline Cohort & Self Profiling: Directional positive Z-scores evaluated against both individual historical baselines "
    "and peer departmental cohorts (Retail, Trading, IT/DBA, Wealth Management), boosted by compound nexus multipliers.\n"
    "• Temporal Sequence Autoencoding with Zero-Dependency Fallback: A 5-day sliding sequence autoencoder capable of running via "
    "PyTorch Bi-LSTM or a pure NumPy vectorized implementation engineered for air-gapped financial server enclaves.\n"
    "• Agentic Multi-Role Deliberation & Autonomous Containment: An autonomous SOC collective using the OODA loop paradigm "
    "(AlertTriageAgent, BehavioralProfilerAgent, ForensicHunterAgent, ActiveDeceptionAgent, and AutonomousResponseAgent) that "
    "revokes credentials in 142 ms and drafts formal FinCEN Form 111 SAR filing packages."
)

# ── Section II: Threat Environment & Problem Formulation ─────────────────
add_sec_head("II. THREAT ENVIRONMENT AND PROBLEM FORMULATION")
add_subsec_head("A. Telemetry Channels")
add_p(
    "We structure the enterprise observation environment across six standardized data feeds conforming to CMU CERT specifications:\n"
    "1) Authentication Telemetry (T_logon): Captures timestamp, User ID, Workstation, Authentication Protocol (Kerberos, NTLM), and Outcome.\n"
    "2) Removable Media Telemetry (T_device): Captures USB connect/disconnect events, Vendor/Product Serial Numbers, and transferred volume in MB.\n"
    "3) File System Audit Telemetry (T_file): Records file path, operation type (Read, Copy, Modify, Delete), data sensitivity, and file size.\n"
    "4) Electronic Messaging Telemetry (T_email): Evaluates internal vs. external recipient routing, attachment volumes, and encryption flags.\n"
    "5) Web Proxy Egress Telemetry (T_http): Ingests destination URIs, domain categories, and upload payloads.\n"
    "6) Directory & HR Metadata (T_ldap): Captures organizational hierarchy, department, PIP review flags, and active resignation notices."
)

add_subsec_head("B. Attack Archetypes in the Evaluation Benchmark")
add_p(
    "The architecture was evaluated against four canonical financial insider attack vectors:\n"
    "• Scenario 1 (Pre-Resignation Customer Data Exfiltration): Senior Loan Officer Alice Walker (USR_RET_04) in Retail Banking "
    "submits resignation. Over the weekend, she accesses 18 confidential loan databases, writes 3,850 MB to a SanDisk USB drive, "
    "and emails encrypted backup archives to ProtonMail.\n"
    "• Scenario 2 (Rogue Trading & Accounting Ledger Manipulation): Derivatives Trader Marcus Vance (USR_TRD_02) in Capital Markets "
    "incurs large unhedged trading deficits. At 2:45 AM, he authenticates via NTLM from an unassigned backup terminal (PC-TRD-BACKUP-09), "
    "places write locks on core_ledger_positions.db, and tampers with Value-at-Risk (risk_limits_var.conf) limits.\n"
    "• Scenario 3 (Privileged System Sabotage & Audit Trail Erasure): Lead Database Administrator Devon Reed (USR_IT_01) in Core IT, "
    "placed on a formal disciplinary review, uses root credentials to access the SWIFT wire gateway server, wipes transaction log "
    "files (db_transaction_audit.log), and stages encrypted wire access keys.\n"
    "• Scenario 4 (Private Client Poaching via Cloud Storage): Vice President Sophia Chen (USR_WLT_03) in Wealth Management, in "
    "discussions with a rival hedge fund, systematically downloads high-net-worth customer portfolios and transfers 850 MB to an "
    "external file locker via multipart HTTP POST uploads."
)

# ── Section III: System Architecture & Methodology ───────────────────────
add_sec_head("III. SYSTEM ARCHITECTURE AND METHODOLOGY")
add_subsec_head("A. The 12-Dimensional Behavioral Feature Vector")
add_p("For every monitored user identity u on observation day t, raw records aggregate into a normalized 12-dimensional vector:")

# Clean Equation 1
add_eq("x(u, t) = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12]^T", "(1)")

p_t1 = doc.add_paragraph()
p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_t1.paragraph_format.space_before = Pt(6)
p_t1.paragraph_format.space_after = Pt(2)
r_t1 = p_t1.add_run("TABLE I\nTHE 12-DIMENSIONAL BEHAVIORAL FEATURE SPACE")
r_t1.font.name = "Times New Roman"
r_t1.font.size = Pt(8.5)
r_t1.font.bold = True

t1_headers = ["Feature", "Var", "Description", "Primary Risk Correlation"]
t1_rows = [
    ["Total Logons", "x1", "Successful authentication count per 24h", "General activity volume"],
    ["Off-Hours Logons", "x2", "Logons prior to 07:00 or after 19:00", "Unsupervised reconnaissance"],
    ["Distinct Workstations", "x3", "Unique hostnames authenticated", "Lateral traversal"],
    ["USB Connects", "x4", "Removable storage mount events", "Physical exfiltration"],
    ["USB Data Volume", "x5", "Megabytes written to removable storage", "Bulk data exfiltration"],
    ["File Operations", "x6", "Total read, copy, write actions", "Broad data harvesting"],
    ["Sensitive Files", "x7", "Access count to confidential/PII files", "Direct PII compromise"],
    ["File Mod/Delete", "x8", "File deletion & content modification", "Sabotage / ledger tampering"],
    ["External Emails", "x9", "Emails routed to external domains", "Electronic data dispatch"],
    ["Email Attachments", "x10", "MB transferred via attachments", "Attachment exfiltration"],
    ["Cloud Uploads", "x11", "MB uploaded to external storage", "Cloud exfiltration"],
    ["Abnormal Host Flag", "x12", "Binary: login from unassigned host", "Unauthorized terminal access"],
]

t1 = doc.add_table(rows=len(t1_rows)+1, cols=4)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t1)

for j, h in enumerate(t1_headers):
    cell = t1.cell(0, j)
    cell.text = h
    set_cell_background(cell, "EAEAEA")
    set_cell_margins(cell, 60, 60, 60, 60)
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
            r.font.bold = True

for i, row in enumerate(t1_rows):
    for j, val in enumerate(row):
        cell = t1.cell(i+1, j)
        cell.text = val
        set_cell_margins(cell, 40, 40, 50, 50)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(7.5)

add_p("", space_after=6)

add_subsec_head("B. Statistical UEBA Engine with Peer Group Baselines")
add_p(
    "Dual reference distributions are maintained: Self Historical (mean_self, std_self) and Peer Cohort (mean_peer, std_peer). "
    "Positive directional standardized scores are computed as:"
)

# Clean Equations 2, 3, 4
add_eq("Z_self = max(0, [x(u,t,j) - mean_self] / [std_self + 1e-5])", "(2a)")
add_eq("Z_peer = max(0, [x(u,t,j) - mean_peer] / [std_peer + 1e-5])", "(2b)")
add_eq("Z_comp(u, t, j) = 0.6 * Z_self + 0.4 * Z_peer", "(3)")
add_p(
    "To capture non-linear synergies between individually moderate anomalies, we define three compound indicator conditions:\n"
    "• Staging & Exfiltration Nexus (N1): Triggered when any of {Z(x5), Z(x10), Z(x11)} >= 2.5 AND Z(x7) >= 2.5.\n"
    "• Off-Hours Ledger/System Manipulation (N2): Triggered when Z(x2) >= 2.0 AND [Z(x8) >= 2.5 OR Z(x12) == 1.0].\n"
    "• Privileged Sabotage Nexus (N3): Triggered when Z(x12) == 1.0 AND Z(x8) >= 3.0.\n"
    "The overall UEBA risk score incorporates these directly:"
)
add_eq("S_UEBA(u, t) = min(100, SUM_j [w_j * Z_comp(u,t,j)] + 15*N1 + 18*N2 + 20*N3)", "(4)")

add_subsec_head("C. Deep Sequence Autoencoder Engine")
add_p(
    "While UEBA captures cross-sectional daily anomalies, our sequence autoencoder analyzes behavioral trajectories over rolling "
    "5-day windows. Continuous sequence tensor X(u,t) in R^(5x12) is compressed through a 16-dimensional bottleneck vector z in R^16 "
    "using either a PyTorch Bidirectional LSTM or a zero-dependency vectorized NumPy feedforward network. The reconstruction error is:"
)

# Clean Equations 5, 6
add_eq("L_recon(X(u, t)) = (1 / 60) * SUM_i SUM_j [X(u,t,i,j) - X_hat(u,t,i,j)]^2", "(5)")
add_eq("S_DL(u, t) = min(100, 100 / [1 + exp(-15 * (L_recon - 0.034))])", "(6)")

add_subsec_head("D. Hybrid Risk Fusion & Organizational Context")
# Clean Equation 7
add_eq("Score_final(u, t) = 0.55 * S_UEBA(u, t) + 0.45 * S_DL(u, t) + Delta_context(u)", "(7)")
add_p(
    "Contextual adjustments: Resignation (+12.0), PIP Review (+8.0), Privileged DBA (+6.0), Trading Authority (+5.0)."
)

# ── Section IV: Agentic AI Autonomous Response ───────────────────────────
add_sec_head("IV. AGENTIC AI AUTONOMOUS RESPONSE (OODA LOOP)")
add_p(
    "Critical incidents (Score >= 80.0) are dispatched to an autonomous Security Operations Center (SOC) agent swarm operating "
    "within an Observe-Orient-Decide-Act (OODA) loop:"
)

p_t2 = doc.add_paragraph()
p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_t2.paragraph_format.space_before = Pt(6)
p_t2.paragraph_format.space_after = Pt(2)
r_t2 = p_t2.add_run("TABLE II\nAGENTIC AI OODA LOOP DECISION SEQUENCE")
r_t2.font.name = "Times New Roman"
r_t2.font.size = Pt(8.5)
r_t2.font.bold = True

t2_rows = [
    ["1. OBSERVE", "AlertTriageAgent", "Ingests multi-modal alert data; checks IT maintenance calendar.", "Priority escalated to P1_CRITICAL."],
    ["2. ORIENT", "BehavioralProfilerAgent", "Cross-references Active Directory LDAP; flags resignation date.", "Discovers 6.4 sigma USB drift; attributes flight risk."],
    ["3. DECIDE", "ForensicHunter & ActiveDeception", "Correlates timestamps; verifies honeypot decoy interactions.", "Corroborates kill-chain (MITRE T1078, T1052)."],
    ["4. ACT", "AutonomousResponseAgent", "Issues machine-speed API containment across identity & network.", "Kerberos revoked (142ms), host isolated (310ms), SAR filed."],
]

t2 = doc.add_table(rows=len(t2_rows)+1, cols=4)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t2)

for j, h in enumerate(["OODA Stage", "Agent Persona", "Reasoning Logic", "Operational Output"]):
    cell = t2.cell(0, j)
    cell.text = h
    set_cell_background(cell, "EAEAEA")
    set_cell_margins(cell, 60, 60, 60, 60)
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
            r.font.bold = True

for i, row in enumerate(t2_rows):
    for j, val in enumerate(row):
        cell = t2.cell(i+1, j)
        cell.text = val
        set_cell_margins(cell, 40, 40, 50, 50)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 0 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(7.5)

add_p("", space_after=6)

add_subsec_head("A. Dynamic Honeypot Verification & FinCEN Form 111 SAR")
add_p(
    "When an identity generates borderline risk (70 <= Score < 80), our ActiveDeceptionAgent dynamically deploys decoy files "
    "(e.g., Q4_Executive_Bonuses_CONFIDENTIAL.xlsx). Accessing the decoy elevates the confidence score to 99.9, converting statistical "
    "suspicion into verified adversarial intent. The AutonomousResponseAgent compiles complete FinCEN Form 111 Suspicious Activity "
    "Report (SAR) narratives in under 700 ms, satisfying 31 CFR § 1020.320 federal filing mandates."
)

# ── Section V: Experimental Evaluation and Results ───────────────────────
add_sec_head("V. EXPERIMENTAL EVALUATION AND RESULTS")
add_subsec_head("A. Anomaly Detection Benchmarks")
add_p(
    "The platform was evaluated on a 30-day simulation modeling 25 financial professionals across Retail Banking, Trading, Core IT, "
    "Wealth Management, and Compliance, benchmarked against four industry baselines across all four planted threat archetypes:"
)

p_t3 = doc.add_paragraph()
p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_t3.paragraph_format.space_before = Pt(6)
p_t3.paragraph_format.space_after = Pt(2)
r_t3 = p_t3.add_run("TABLE III\nCOMPARATIVE DETECTION PERFORMANCE ACROSS ATTACK ARCHETYPES")
r_t3.font.name = "Times New Roman"
r_t3.font.size = Pt(8.5)
r_t3.font.bold = True

t3_rows = [
    ["Static Threshold DLP", "Missed (<4GB)", "Missed (Valid creds)", "Missed (Valid admin)", "Missed (HTTP ok)", "0.0%", "14.8%"],
    ["Standard SIEM Rules", "Partial Alert", "Missed", "Missing audit log", "Missed", "25.0%", "18.2%"],
    ["Isolation Forest (12D)", "Detected", "Delayed (Day 28)", "Detected", "Marginal", "75.0%", "6.4%"],
    ["One-Class SVM (RBF)", "Detected", "Missed", "Detected", "Detected", "75.0%", "5.8%"],
    ["Our Hybrid Platform", "Detected (92.5)", "Detected (95.8)", "Detected (91.0)", "Detected (99.9*)", "100.0%", "0.8%"],
]

t3 = doc.add_table(rows=len(t3_rows)+1, cols=7)
t3.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t3)

t3_headers = ["System", "Scen 1", "Scen 2", "Scen 3", "Scen 4", "Recall", "FP Rate"]
for j, h in enumerate(t3_headers):
    cell = t3.cell(0, j)
    cell.text = h
    set_cell_background(cell, "EAEAEA")
    set_cell_margins(cell, 50, 50, 40, 40)
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(7.5)
            r.font.bold = True

for i, row in enumerate(t3_rows):
    for j, val in enumerate(row):
        cell = t3.cell(i+1, j)
        cell.text = val
        if i == len(t3_rows)-1:
            set_cell_background(cell, "EBF5FB")
        set_cell_margins(cell, 35, 35, 40, 40)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(7)
                if i == len(t3_rows)-1:
                    r.font.bold = True

add_p("*Elevated to 99.9 via ActiveDeceptionAgent honeypot touch confirmation.", space_after=6, italic=True)

add_subsec_head("B. Sequence Reconstruction Dynamics & Latency Benchmarks")
add_p(
    "During normal operation (Days 1–20), baseline reconstruction loss remained tightly bound (L_recon <= 0.034). "
    "In Scenario 1 (Alice Walker), loss climbed from 0.025 to 0.510 on Day 25 as after-hours login coincided with bulk USB copying. "
    "In Scenario 2 (Marcus Vance), unauthorized terminal authentication with database write locks drove loss to 0.740.\n"
    "Compared to the human-dependent industry benchmark of 85 days, our autonomous response pipeline executed closed-loop containment "
    "across all infrastructure points in less than 1.4 seconds (Identity Session Revocation: 142 ms, Endpoint Network Isolation: 310 ms, "
    "Ledger Access Freeze: 205 ms, FinCEN SAR Auto-Filing Generation: 680 ms, Total Closed-Loop Containment: 1,337 ms)."
)

# ── Section VI: Regulatory Compliance Alignment ──────────────────────────
add_sec_head("VI. REGULATORY COMPLIANCE ALIGNMENT")
add_p(
    "The platform enforces direct alignment with statutory banking mandates:\n"
    "• GLBA § 501(b): Protects non-public consumer financial information by tracking USB volumes and enforcing sub-second Kerberos invalidation.\n"
    "• SOX § 404: Maintains auditable internal controls over financial records by isolating unauthorized terminal ledger tampering.\n"
    "• PCI-DSS 10.2: Continuously correlates multi-modal events to verified employee IDs; flags abnormal terminal access.\n"
    "• SWIFT CSP 2.1: Enforces privileged access controls and immediately blocks attempts to wipe system audit trails.\n"
    "• FinCEN 31 CFR § 1020.320: Generates formatted Form 111 electronic SAR narrative filing packages ready for compliance sign-off."
)

# ── Section VII: Conclusion & Acknowledgement ────────────────────────────
add_sec_head("VII. CONCLUSION AND ACKNOWLEDGEMENT")
add_p(
    "Insider threats exploit implicit trust in authorized credentials. By combining dense 12-dimensional telemetry aggregation, "
    "dual-baseline UEBA Z-score profiling, temporal sequence autoencoders, and an Agentic AI team executing structured OODA loops, "
    "our platform detected 100% of planted CMU CERT insider threat scenarios with an 0.8% false positive rate while compressing "
    "containment from 85 days to under 1.4 seconds.\n\n"
    "The authors gratefully acknowledge the guidance, technical insights, and institutional support provided by Prof. Swati Singh, "
    "Department of Information Technology, School of Computing, MIT ADT University, Pune, throughout the course of this research project."
)

# ── References ───────────────────────────────────────────────────────────
add_sec_head("REFERENCES")
refs = [
    "[1] Computer Emergency Response Team (CERT), \"The CERT Guide to Insider Threats,\" SEI, Carnegie Mellon University, Tech. Rep., 2021.",
    "[2] Ponemon Institute, \"Cost of Insider Threats Global Report,\" Ponemon Institute LLC & Proofpoint, Research Benchmark, 2024.",
    "[3] S. Hochreiter and J. Schmidhuber, \"Long Short-Term Memory,\" Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.",
    "[4] P. Malhotra et al., \"LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection,\" in Proc. ICML Workshop, 2016.",
    "[5] FFIEC, \"Information Security IT Examination Handbook,\" FFIEC Regulatory Guidelines, 2023.",
    "[6] FinCEN, \"Advisory to Financial Institutions on Cyber-Events and Cyber-Enabled Crime,\" U.S. Dept. of the Treasury, 2016.",
    "[7] SWIFT, \"Customer Security Controls Framework (CSCF) v2024,\" SWIFT Standards, 2024.",
    "[8] MITRE Corporation, \"MITRE ATT&CK for Enterprise,\" MITRE Technical Documentation, 2023.",
    "[9] D. E. Denning, \"An Intrusion-Detection Model,\" IEEE Trans. Software Eng., vol. SE-13, no. 2, pp. 222–232, 1987.",
    "[10] A. Vaswani et al., \"Attention Is All You Need,\" in Advances in Neural Information Processing Systems (NeurIPS), 2017.",
    "[11] FTC, \"Standards for Safeguarding Customer Information (GLBA 16 CFR Part 314),\" FTC Final Rule, 2022.",
    "[12] U.S. SEC, \"Management's Report on Internal Control Over Financial Reporting (SOX § 404),\" SEC Final Rules, 2002.",
]

for ref in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    run = p.add_run(ref)
    run.font.name = "Times New Roman"
    run.font.size = Pt(8)

doc.save(OUTPUT)
doc.save(DOWNLOADS_COPY)
print(f"IEEE DOCX regenerated with clean 100% visible formulas and no Leader tag!")
print(f"Saved to: {OUTPUT} and {DOWNLOADS_COPY}")
