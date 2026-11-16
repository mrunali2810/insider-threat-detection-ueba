"""
Specialized Banking SOC Multi-Agent System for Autonomous Insider Threat Response.

Features:
1. AlertTriageAgent: First responder, fast classification, false-positive filtering.
2. BehavioralProfilerAgent: UEBA specialist, peer deviation, HR and motivation context.
3. ForensicHunterAgent: Multi-modal log correlation, attack timeline, MITRE ATT&CK mapping.
4. AutonomousResponseAgent: Incident containment commands, access revocation, SAR generation.
5. SOCOrchestrator: Multi-agent supervisor, debate synthesis, executive briefing generation.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseSOCAgent, AgentMessage


class AlertTriageAgent(BaseSOCAgent):
    """Tier-1 Banking SOC Intake & Triage Specialist."""

    def __init__(self):
        super().__init__(
            name="AlertTriageAgent",
            role="Senior Tier-1 Financial SOC Analyst",
            expertise="Real-time threat evaluation, regulatory prioritization, false-positive suppression."
        )

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        alert = context["threat_record"]
        h_score = alert["hybrid_score"]
        tier = alert["threat_tier"]
        user_id = alert["user_id"]

        thought = (
            f"Evaluating incoming anomaly telemetry for user {user_id} on {alert['date']}. "
            f"Hybrid threat score is {h_score}/100 ({tier}). "
            f"Checking whether activity coincides with pre-scheduled banking maintenance."
        )

        # False positive check: IT maintenance window on weekends for sysadmins
        is_false_positive = False
        if alert["department"] == "Core IT & Infrastructure" and not alert.get("nexus_triggers") and h_score < 65.0:
            is_false_positive = True
            triaged_verdict = "BENIGN_MAINTENANCE"
            priority = "P4_LOW"
        elif tier == "CRITICAL":
            triaged_verdict = "IMMEDIATE_THREAT_CONFIRMED"
            priority = "P1_CRITICAL"
        elif tier == "HIGH_RISK":
            triaged_verdict = "ELEVATED_THREAT"
            priority = "P2_HIGH"
        else:
            triaged_verdict = "SUSPICIOUS_MONITOR"
            priority = "P3_MEDIUM"

        findings = {
            "triaged_verdict": triaged_verdict,
            "priority": priority,
            "is_false_positive": is_false_positive,
            "initial_risk_score": h_score,
            "exposure_category": alert.get("compliance_violations", ["Internal Security Policy"])[0] if alert.get("compliance_violations") else "Operational Drift",
            "recommended_workflow": "DISPATCH_TO_PROFILER_AND_HUNTER" if not is_false_positive else "CLOSE_TICKET"
        }

        self.log_thought("SOCOrchestrator", "EVALUATION", thought, findings)
        return findings


class BehavioralProfilerAgent(BaseSOCAgent):
    """UEBA & Identity Behavioral Profiling Specialist."""

    def __init__(self):
        super().__init__(
            name="BehavioralProfilerAgent",
            role="UEBA Identity Analytics & Psychology Profiler",
            expertise="Peer-group cohort analysis, behavioral drift tracking, HR flight-risk indicators."
        )

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        alert = context["threat_record"]
        user_meta = context.get("user_meta")
        zscores = alert.get("raw_features", {})

        thought = (
            f"Conducting deep identity behavioral comparison for {alert['employee_name']} ({alert['user_id']}) "
            f"in {alert['department']}. Analyzing deviation from established peer group baselines."
        )

        # Analyze motive & stress factors
        hr_indicators = []
        if user_meta:
            if user_meta.is_resigned:
                hr_indicators.append(f"Resignation Notice Submitted: Departure effective {user_meta.resignation_effective_date}. Classic pre-departure data theft window.")
            if "PIP" in user_meta.performance_rating or "Needs" in user_meta.performance_rating:
                hr_indicators.append(f"Adverse Employment Event: Employee placed on {user_meta.performance_rating}.")

        # Identify anomalous behavioral dimensions
        anomalous_dimensions = []
        drivers = alert.get("high_risk_drivers", [])
        for d in drivers:
            anomalous_dimensions.append(d)

        profile_assessment = {
            "user_id": alert["user_id"],
            "department": alert["department"],
            "role": alert["role"],
            "flight_risk_level": "EXTREME" if user_meta and user_meta.is_resigned else ("MODERATE" if hr_indicators else "LOW"),
            "peer_deviation_summary": f"User deviated across {len(anomalous_dimensions)} critical parameters compared to {alert['department']} peers.",
            "stress_and_motive_factors": hr_indicators,
            "behavioral_drift_rating": "EXTREME_ANOMALOUS_SURGE" if alert["ueba_score"] >= 75 else "MODERATE_DRIFT",
            "deliberation_verdict": "INTENTIONAL_ANOMALOUS_ACTIVITY" if hr_indicators or alert["ueba_score"] > 60 else "POSSIBLE_UNINTENTIONAL_DRIFT"
        }

        self.log_thought("SOCOrchestrator", "EVALUATION", thought, profile_assessment)
        return profile_assessment


class ForensicHunterAgent(BaseSOCAgent):
    """Cyber Forensics & Multi-Modal Attack Graph Specialist."""

    def __init__(self):
        super().__init__(
            name="ForensicHunterAgent",
            role="Senior Forensic Threat Hunter",
            expertise="Multi-modal log stitching, kill-chain reconstruction, MITRE ATT&CK insider mapping."
        )

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        alert = context["threat_record"]
        container = context.get("container")
        uid = alert["user_id"]
        date = alert["date"]

        thought = (
            f"Stitching multi-modal forensic logs across Logon, File, Device, Email, and HTTP streams "
            f"for user {uid} on {date} to reconstruct the timeline."
        )

        timeline = []
        mitre_tactics = []
        evidence_artifacts = []

        # Find atomic events for this user on this day
        if container:
            # Logon events
            for r in container.logon_logs:
                if r.user_id == uid and r.timestamp.startswith(date):
                    timeline.append(f"[{r.timestamp}] LOGON: User authenticated via {r.auth_method} on {r.workstation} (IP: {r.source_ip})")
                    if "Backup" in r.workstation or "NTLM" in r.auth_method:
                        mitre_tactics.append("T1078 (Valid Accounts - Abnormal Credential/Terminal Use)")
                        evidence_artifacts.append(f"Abnormal terminal session: {r.workstation}")

            # File events
            for r in container.file_logs:
                if r.user_id == uid and r.timestamp.startswith(date):
                    timeline.append(f"[{r.timestamp}] FILE {r.activity.upper()}: {r.filename} ({r.classification}) - {r.file_path}")
                    if r.is_sensitive:
                        evidence_artifacts.append(f"Accessed sensitive bank asset: {r.filename}")
                        if r.activity in ["Modify", "Delete"]:
                            mitre_tactics.append("T1565.001 (Data Manipulation: Stored Data Manipulation / Audit Deletion)")
                        else:
                            mitre_tactics.append("T1005 (Data from Local System / Mass File Access)")

            # Device events
            for r in container.device_logs:
                if r.user_id == uid and r.timestamp.startswith(date):
                    timeline.append(f"[{r.timestamp}] DEVICE {r.activity.upper()}: Mounted {r.device_vendor} (SN: {r.device_serial}), Data: {r.data_transferred_mb:.1f} MB")
                    mitre_tactics.append("T1052 (Exfiltration Over Physical Medium - USB)")
                    evidence_artifacts.append(f"USB Transfer: {r.data_transferred_mb:.1f} MB to {r.device_vendor}")

            # Email events
            for r in container.email_logs:
                if r.user_id == uid and r.timestamp.startswith(date):
                    timeline.append(f"[{r.timestamp}] EMAIL: Sent to {', '.join(r.to_recipients)} | Subject: '{r.subject}' | Attachments: {r.attachments}")
                    if r.is_external:
                        mitre_tactics.append("T1567.001 (Exfiltration Over Web Service / Personal Webmail)")
                        evidence_artifacts.append(f"External Email Exfiltration: {r.to_recipients}")

            # HTTP events
            for r in container.http_logs:
                if r.user_id == uid and r.timestamp.startswith(date):
                    if r.bytes_uploaded > 5_000_000 or r.category in ["Cloud Storage", "Dark Web", "Personal Webmail"]:
                        timeline.append(f"[{r.timestamp}] HTTP POST: {r.url} ({r.category}) - Uploaded {r.bytes_uploaded / (1024*1024):.1f} MB")
                        mitre_tactics.append("T1567.002 (Exfiltration to Cloud Storage)")
                        evidence_artifacts.append(f"Cloud Storage Exfiltration: {r.domain}")

        # Deduplicate tactics
        mitre_tactics = list(dict.fromkeys(mitre_tactics))

        forensic_report = {
            "chronological_timeline": timeline[:8],  # Top chronological events
            "mitre_attck_techniques": mitre_tactics,
            "forensic_artifacts_recovered": evidence_artifacts,
            "attack_stage_reached": "EXFILTRATION_OR_IMPACT" if any("Exfiltration" in t or "Manipulation" in t for t in mitre_tactics) else "COLLECTION_STAGING",
            "forensic_confidence": "HIGH (Corroborated across multi-modal telemetry)" if len(timeline) >= 2 else "MEDIUM"
        }

        self.log_thought("SOCOrchestrator", "FORENSIC_EVIDENCE", thought, forensic_report)
        return forensic_report

class ActiveDeceptionAgent(BaseSOCAgent):
    """Active Defense & Honeypot Deployment Specialist."""

    def __init__(self):
        super().__init__(
            name="ActiveDeceptionAgent",
            role="Senior Active Defense & Deception Engineer",
            expertise="Dynamic honeypot deployment, adversary engagement, high-fidelity intent confirmation."
        )

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        alert = context["threat_record"]
        h_score = alert["hybrid_score"]
        uid = alert["user_id"]

        thought = (
            f"Evaluating deception strategy for {uid}. Current hybrid score is {h_score:.1f}/100. "
            f"Determining if active honeypot deployment is required to confirm malicious intent."
        )

        deception_report = {}
        
        # If the score is in the ambiguous "high risk" zone (e.g., 60-85), we deploy a honeypot.
        if 60.0 <= h_score < 85.0:
            honeypot_file = "Q4_Executive_Bonuses_CONFIDENTIAL.xlsx" if alert["department"] in ["Retail Banking", "Wealth Management"] else "Master_Admin_Passwords.kdbx"
            deception_report = {
                "action_taken": "HONEYPOT_DEPLOYED",
                "honeypot_type": "Decoy File Staging",
                "decoy_asset": honeypot_file,
                "target_directory": f"\\\\meridian-fs\\users\\{uid}\\private\\",
                "justification": f"Risk score {h_score:.1f} indicates probable threat. Deploying '{honeypot_file}' to bait the adversary and confirm intent with 100% fidelity before containment.",
                "status": "AWAITING_TRIGGER"
            }
            # For simulation purposes, let's assume the user bit the honeypot
            thought += f" Deployed {honeypot_file}. [SIMULATION UPDATE] Target accessed the decoy file! Malicious intent definitively confirmed. Escalating threat."
            deception_report["trigger_status"] = "HONEYPOT_ACCESSED"
            deception_report["escalation"] = True
            
            # Escalate the hybrid score so the Response Agent drops the hammer
            alert["hybrid_score"] = 99.9
            alert["threat_tier"] = "CRITICAL"
        else:
            deception_report = {
                "action_taken": "NO_DECEPTION_REQUIRED",
                "justification": "Threat is either BENIGN or already definitively CRITICAL. Bypassing deception layer."
            }

        self.log_thought("SOCOrchestrator", "ACTIVE_DEFENSE", thought, deception_report)
        return deception_report


class AutonomousResponseAgent(BaseSOCAgent):
    """Autonomous Incident Commander & Regulatory Compliance Remediation Specialist."""

    def __init__(self):
        super().__init__(
            name="AutonomousResponseAgent",
            role="Autonomous Incident Commander & Banking Compliance Officer",
            expertise="SOX/GLBA regulatory compliance, automated containment, FinCEN SAR drafting."
        )

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        alert = context["threat_record"]
        forensic = context.get("forensic_report", {})
        profiler = context.get("profiler_report", {})
        h_score = alert["hybrid_score"]

        thought = (
            f"Determining containment protocols and regulatory disclosure mandates for {alert['employee_name']} "
            f"(Score: {h_score}/100, Tier: {alert['threat_tier']}). Enforcing Zero-Trust policy."
        )

        automated_actions = []
        regulatory_actions = []

        if h_score >= 80.0:
            automated_actions.append({
                "action": "REVOKE_ACTIVE_SESSIONS",
                "target": f"Active Kerberos tickets & OAuth tokens for {alert['user_id']}",
                "status": "EXECUTED",
                "latency_ms": 142
            })
            automated_actions.append({
                "action": "HOST_NETWORK_ISOLATION",
                "target": f"Endpoint Workstation ({alert['role']})",
                "status": "EXECUTED",
                "latency_ms": 310
            })
            automated_actions.append({
                "action": "FREEZE_FINANCIAL_TRANSACTIONS",
                "target": "Core Banking Ledger & SWIFT Messaging Gateway",
                "status": "EXECUTED",
                "latency_ms": 205
            })

            # Formulate FinCEN SAR Filing
            sar_draft = self._generate_fincen_sar(alert, forensic, profiler)
            regulatory_actions.append("Draft FinCEN Suspicious Activity Report (SAR) Form 111")
            regulatory_actions.append("Trigger GLBA Safeguards Rule Customer Notification Procedure")

        elif h_score >= 60.0:
            automated_actions.append({
                "action": "STEP_UP_AUTHENTICATION_AND_MFA_CHALLENGE",
                "target": f"User {alert['user_id']}",
                "status": "EXECUTED",
                "latency_ms": 95
            })
            automated_actions.append({
                "action": "RESTRICT_REMOVABLE_STORAGE",
                "target": "Active Workstation DLP Enforcer",
                "status": "EXECUTED",
                "latency_ms": 180
            })
            sar_draft = "SAR Not Required at Current Threshold (Monitored for Escalation)"
        else:
            automated_actions.append({
                "action": "ENABLE_ENHANCED_SESSION_AUDITING",
                "target": f"Telemetry daemon for {alert['user_id']}",
                "status": "EXECUTED",
                "latency_ms": 80
            })
            sar_draft = "None"

        remediation_result = {
            "containment_orders": automated_actions,
            "regulatory_mandates": regulatory_actions,
            "fincen_sar_filing": sar_draft,
            "human_approval_required": True if h_score >= 80.0 else False,
            "incident_status": "CONTAINED_PENDING_EXECUTIVE_SIGNOFF" if h_score >= 80.0 else "ACTIVE_SURVEILLANCE"
        }

        self.log_thought("SOCOrchestrator", "COMMAND", thought, remediation_result)
        return remediation_result

    def _generate_fincen_sar(self, alert: Dict[str, Any], forensic: Dict[str, Any], profiler: Dict[str, Any]) -> Dict[str, Any]:
        """Generates formal draft of US Treasury FinCEN Suspicious Activity Report (SAR)."""
        artifacts = forensic.get("forensic_artifacts_recovered", ["Unauthorized Data Access"])
        tactics = forensic.get("mitre_attck_techniques", ["T1078"])

        narrative = (
            f"On {alert['date']}, the automated Meridian Bank UEBA and Deep Learning Security System detected "
            f"unauthorized high-risk activity initiated by employee {alert['employee_name']} (ID: {alert['user_id']}, "
            f"Title: {alert['role']}, Department: {alert['department']}). "
            f"The subject exhibited anomalous behavioral spikes (UEBA Score: {alert['ueba_score']}, "
            f"Deep Learning Anomaly Ratio: {alert.get('dl_error_ratio', 'N/A')}). "
            f"Forensic examination identified unauthorized staging and exfiltration indicators including: {'; '.join(artifacts[:3])}. "
            f"Tactics correspond to MITRE ATT&CK categories: {', '.join(tactics[:3])}. "
            f"Immediate automated containment was triggered to protect customer financial assets under GLBA 501(b) and SOX 404."
        )

        return {
            "filing_institution": "Meridian Bank & Trust N.A.",
            "filing_type": "FinCEN Form 111 - Suspicious Activity Report (SAR)",
            "subject_name": alert["employee_name"],
            "subject_id": alert["user_id"],
            "incident_date": alert["date"],
            "suspicious_activity_category": "Computer Intrusion / Unauthorized Data Exfiltration / Insider Sabotage",
            "estimated_exposure": alert.get("financial_impact_estimate", "Over $250,000"),
            "narrative": narrative
        }


class SOCOrchestrator:
    """Supervises and coordinates the multi-agent investigation lifecycle."""

    def __init__(self):
        self.triage_agent = AlertTriageAgent()
        self.profiler_agent = BehavioralProfilerAgent()
        self.forensic_agent = ForensicHunterAgent()
        self.deception_agent = ActiveDeceptionAgent()
        self.response_agent = AutonomousResponseAgent()

    def investigate(self, threat_record: Dict[str, Any], container: Any, user_meta: Any) -> Dict[str, Any]:
        """Executes full multi-agent collaborative investigation loop."""
        investigation_id = f"INV-{threat_record['user_id']}-{threat_record['date'].replace('-', '')}"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        context = {
            "threat_record": threat_record,
            "container": container,
            "user_meta": user_meta
        }

        # Step 1: Alert Triage
        triage_report = self.triage_agent.process(context)

        # Step 2: Behavioral Profiling
        profiler_report = self.profiler_agent.process(context)
        context["profiler_report"] = profiler_report

        # Step 3: Deep Forensic Hunting
        forensic_report = self.forensic_agent.process(context)
        context["forensic_report"] = forensic_report

        # Step 3.5: Active Deception & Honeypot Deployment
        deception_report = self.deception_agent.process(context)
        context["deception_report"] = deception_report

        # Step 4: Autonomous Response & Containment
        response_report = self.response_agent.process(context)

        # Step 5: Multi-agent Transcript Compilation
        agent_transcript = [
            {
                "agent": "AlertTriageAgent",
                "role": self.triage_agent.role,
                "step": "Intake & Priority Triage",
                "thought": self.triage_agent.memory[-1].thought,
                "findings": triage_report
            },
            {
                "agent": "BehavioralProfilerAgent",
                "role": self.profiler_agent.role,
                "step": "UEBA Identity & Peer Cohort Analysis",
                "thought": self.profiler_agent.memory[-1].thought,
                "findings": profiler_report
            },
            {
                "agent": "ForensicHunterAgent",
                "role": self.forensic_agent.role,
                "step": "Multi-Modal Forensic Log Correlation",
                "thought": self.forensic_agent.memory[-1].thought,
                "findings": forensic_report
            },
            {
                "agent": "ActiveDeceptionAgent",
                "role": self.deception_agent.role,
                "step": "Dynamic Honeypot Deployment",
                "thought": self.deception_agent.memory[-1].thought,
                "findings": deception_report
            },
            {
                "agent": "AutonomousResponseAgent",
                "role": self.response_agent.role,
                "step": "Zero-Trust Containment & Regulatory Filing",
                "thought": self.response_agent.memory[-1].thought,
                "findings": response_report
            }
        ]

        # Executive Incident Dossier
        dossier = {
            "investigation_id": investigation_id,
            "timestamp": start_time,
            "subject": {
                "user_id": threat_record["user_id"],
                "name": threat_record["employee_name"],
                "role": threat_record["role"],
                "department": threat_record["department"]
            },
            "threat_assessment": {
                "hybrid_score": threat_record["hybrid_score"],
                "threat_tier": threat_record["threat_tier"],
                "priority": triage_report["priority"],
                "financial_impact_estimate": threat_record.get("financial_impact_estimate", "$0")
            },
            "agent_transcript": agent_transcript,
            "containment_summary": response_report["containment_orders"],
            "regulatory_filing": response_report["fincen_sar_filing"]
        }

        return dossier
