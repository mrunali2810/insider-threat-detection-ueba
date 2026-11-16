"""
Banking & Finance Synthetic CERT Dataset Generator.

Generates realistic enterprise logs conforming to CMU CERT schemas with
ground-truth insider threat scenarios specifically crafted for Banking & Capital Markets.
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any

from .cert_schema import (
    LdapRecord,
    LogonRecord,
    DeviceRecord,
    FileRecord,
    EmailRecord,
    HttpRecord,
    CertDatasetContainer
)


# Bank Org Chart & Identity Specs
DEPARTMENTS = {
    "Retail Banking": {
        "roles": ["Teller", "Senior Loan Officer", "Branch Manager", "Credit Analyst"],
        "normal_files": ["retail_ops_manual.pdf", "loan_application_forms.docx", "branch_cash_audit.xlsx"],
        "sensitive_files": ["customer_ssn_database.parquet", "wealth_credit_bureau_dump.csv", "kyc_passports_2025.zip"],
        "allowed_pcs": ["PC-RET-01", "PC-RET-02", "PC-RET-03", "PC-RET-04", "PC-RET-05"],
    },
    "Trading & Markets": {
        "roles": ["FX Trader", "Derivatives Trader", "Fixed Income Clerk", "Quantitative Analyst"],
        "normal_files": ["fx_spot_rates.pdf", "bloomberg_macro_bulletin.pdf", "daily_trade_blotter.xlsx"],
        "sensitive_files": ["core_ledger_positions.db", "risk_limits_var.conf", "counterparty_credit_limits.json"],
        "allowed_pcs": ["PC-TRD-01", "PC-TRD-02", "PC-TRD-03", "PC-TRD-04", "PC-TRD-05"],
    },
    "Wealth Management": {
        "roles": ["Private Banker", "Portfolio Advisor", "VP Wealth Management", "Trust Officer"],
        "normal_files": ["market_outlook_q3.pdf", "asset_allocation_models.xlsx", "investment_prospectus.pdf"],
        "sensitive_files": ["hnw_client_family_trusts.pdf", "offshore_asset_holdings_2025.xlsx", "client_tax_returns_all.zip"],
        "allowed_pcs": ["PC-WLT-01", "PC-WLT-02", "PC-WLT-03", "PC-WLT-04", "PC-WLT-05"],
    },
    "Core IT & Infrastructure": {
        "roles": ["Lead Database Administrator", "DevOps Engineer", "Network Architect", "Security Analyst"],
        "normal_files": ["server_patch_schedule.docx", "terraform_configs.tf", "network_topology.vsdx"],
        "sensitive_files": ["swift_wire_credentials.enc", "db_transaction_audit.log", "root_kerberos_keytab.key"],
        "allowed_pcs": ["PC-IT-01", "PC-IT-02", "PC-IT-03", "PC-IT-04", "PC-IT-05"],
    },
    "Compliance & Legal": {
        "roles": ["AML Investigator", "Compliance Officer", "Internal Auditor", "Legal Counsel"],
        "normal_files": ["aml_guidelines_2025.pdf", "regulatory_filing_calendar.xlsx", "audit_checklists.docx"],
        "sensitive_files": ["fincen_sar_drafts_confidential.docx", "whistleblower_reports_internal.pdf"],
        "allowed_pcs": ["PC-CMP-01", "PC-CMP-02", "PC-CMP-03", "PC-CMP-04"],
    },
}

NORMAL_DOMAINS = [
    ("https://intranet.meridian-bank.internal/dashboard", "Intranet"),
    ("https://bloomberg.com/markets", "Financial News"),
    ("https://reuters.com/finance", "Financial News"),
    ("https://federalreserve.gov/reports", "Financial News"),
    ("https://support.meridian-bank.internal/tickets", "Intranet"),
]

SUSPICIOUS_DOMAINS = [
    ("https://mega.nz/upload/personal-vault", "Cloud Storage"),
    ("https://dropbox.com/upload/client-data", "Cloud Storage"),
    ("https://proton.me/mail/secure-inbox", "Personal Webmail"),
    ("https://darkweb-paste-dump.onion/upload", "Dark Web"),
    ("https://temp-file-share.cc/v1/store", "Cloud Storage"),
]


class BankingCertDatasetGenerator:
    """Generates synthetic CERT datasets with realistic enterprise banking patterns."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        self.container = CertDatasetContainer()
        self.ground_truth_threats: Dict[str, Dict[str, Any]] = {}

    def _generate_identities(self) -> List[LdapRecord]:
        """Creates realistic banking users across departments."""
        users = []
        user_counter = 1

        dept_specs = [
            ("Retail Banking", 6),
            ("Trading & Markets", 5),
            ("Wealth Management", 5),
            ("Core IT & Infrastructure", 5),
            ("Compliance & Legal", 4),
        ]

        names = [
            ("Alice", "Walker"), ("Marcus", "Vance"), ("Sophia", "Chen"), ("Devon", "Reed"),
            ("James", "Sterling"), ("Elena", "Rostova"), ("Arthur", "Pendleton"), ("Chloe", "Bennett"),
            ("Nikhil", "Patel"), ("Hannah", "Schmidt"), ("Carlos", "Mendoza"), ("Fatima", "Al-Mansoor"),
            ("David", "Kim"), ("Rebecca", "Torres"), ("Lucas", "Vanderbilt"), ("Aaliyah", "Jackson"),
            ("Oliver", "Huxley"), ("Grace", "Sinclair"), ("Vikram", "Malhotra"), ("Zoe", "Kowalski"),
            ("Ethan", "Cross"), ("Maya", "Lin"), ("Julian", "Banks"), ("Naomi", "Nagata"), ("Liam", "O'Connor")
        ]

        name_idx = 0
        for dept_name, count in dept_specs:
            dept_info = DEPARTMENTS[dept_name]
            for i in range(count):
                first, last = names[name_idx % len(names)]
                name_idx += 1
                dept_prefixes = {
                    "Retail Banking": "RET",
                    "Trading & Markets": "TRD",
                    "Wealth Management": "WLT",
                    "Core IT & Infrastructure": "IT",
                    "Compliance & Legal": "CMP",
                }
                prefix = dept_prefixes.get(dept_name, "USR")
                uid = f"USR_{prefix}_{i+1:02d}"
                role = dept_info["roles"][i % len(dept_info["roles"])]
                pc = dept_info["allowed_pcs"][i % len(dept_info["allowed_pcs"])]
                
                # Assign clearance
                clearance = "Confidential"
                if "Trader" in role or "VP" in role or "Administrator" in role:
                    clearance = "Restricted / Secret"
                elif "Compliance" in role or "Auditor" in role:
                    clearance = "Executive Compliance"

                record = LdapRecord(
                    user_id=uid,
                    employee_name=f"{first} {last}",
                    email=f"{first.lower()}.{last.lower()}@meridian-bank.com",
                    role=role,
                    department=dept_name,
                    clearance_level=clearance,
                    supervisor="Executive Director J. Holloway",
                    workstation=pc,
                    is_resigned=False,
                    performance_rating="Exceeds Expectations" if i == 0 else "Meets Expectations"
                )
                users.append(record)
                self.container.users[uid] = record

        return users

    def generate(self, days: int = 30) -> Tuple[CertDatasetContainer, Dict[str, Any]]:
        """Generates baseline logs plus 4 planted realistic banking insider threats."""
        users = self._generate_identities()
        start_date = datetime(2025, 5, 1, 8, 0, 0)

        # Plan planted threat profiles
        # Scenario 1: Alice Walker (USR_RET_04) - Pre-resignation Customer PII Exfiltration
        target_ret = [u for u in users if u.user_id == "USR_RET_04"][0]
        target_ret.is_resigned = True
        target_ret.resignation_effective_date = "2025-05-28"
        target_ret.performance_rating = "Needs Improvement"
        self.ground_truth_threats["USR_RET_04"] = {
            "name": "Pre-resignation Mass Customer PII Exfiltration",
            "scenario": "CERT Scenario 1 (Financial Variant)",
            "threat_actor": target_ret.employee_name,
            "department": target_ret.department,
            "attack_days": list(range(23, 29)),
            "tactics": ["After-hours Reconnaissance", "Bulk PII Staging", "USB Data Theft", "External Encrypted Exfiltration"],
            "mitre_ids": ["T1078", "T1052", "T1567", "T1005"],
            "severity": "CRITICAL",
            "regulatory_violation": "GLBA 501(b) / PCI-DSS 10.2 / NYDFS 500"
        }

        # Scenario 2: Marcus Vance (USR_TRD_02) - Rogue Trading Off-Hours Ledger Tampering
        target_trd = [u for u in users if u.user_id == "USR_TRD_02"][0]
        self.ground_truth_threats["USR_TRD_02"] = {
            "name": "Rogue Trader Off-Hours Ledger Override",
            "scenario": "CERT Scenario 2 (Financial Variant)",
            "threat_actor": target_trd.employee_name,
            "department": target_trd.department,
            "attack_days": [24, 25, 26, 27],
            "tactics": ["Abnormal Terminal Logon", "Off-hours Core Ledger Query", "Risk Limits Tampering"],
            "mitre_ids": ["T1078", "T1565.001", "T1083"],
            "severity": "CRITICAL",
            "regulatory_violation": "SOX 404 / FINRA Rule 3110 / Basel III Operational Risk"
        }

        # Scenario 3: Devon Reed (USR_IT_01) - DBA Privilege Escalation & Audit Log Deletion
        target_it = [u for u in users if u.user_id == "USR_IT_01"][0]
        target_it.performance_rating = "Under PIP Review"
        self.ground_truth_threats["USR_IT_01"] = {
            "name": "IT Administrator Sabotage & Credential Staging",
            "scenario": "CERT Scenario 3 (Financial Variant)",
            "threat_actor": target_it.employee_name,
            "department": target_it.department,
            "attack_days": [21, 22, 25],
            "tactics": ["Lateral Movement to SWIFT Gateway", "Audit Log Clearing", "Shadow Account Creation"],
            "mitre_ids": ["T1078", "T1070.001", "T1136.001", "T1552"],
            "severity": "CRITICAL",
            "regulatory_violation": "SWIFT CSP (Customer Security Programme) / FFIEC Core Security"
        }

        # Scenario 4: Sophia Chen (USR_WLT_03) - HNW Client Poaching via Cloud Upload
        target_wlt = [u for u in users if u.user_id == "USR_WLT_03"][0]
        self.ground_truth_threats["USR_WLT_03"] = {
            "name": "High-Net-Worth Client Portfolio Poaching via Web Storage",
            "scenario": "CERT Scenario 4 (Financial Variant)",
            "threat_actor": target_wlt.employee_name,
            "department": target_wlt.department,
            "attack_days": [19, 20, 21, 22],
            "tactics": ["Bulk Confidential Portfolio Harvesting", "Encrypted Cloud Storage Upload"],
            "mitre_ids": ["T1005", "T1567.002", "T1074.001"],
            "severity": "HIGH",
            "regulatory_violation": "SEC Regulation S-P / Gramm-Leach-Bliley Act (GLBA)"
        }

        event_id_seq = 10000

        # Simulate day by day
        for day in range(1, days + 1):
            current_day_dt = start_date + timedelta(days=day - 1)
            is_weekend = current_day_dt.weekday() >= 5  # 5 = Saturday, 6 = Sunday

            for user in users:
                uid = user.user_id
                dept_info = DEPARTMENTS[user.department]

                # Check if user is carrying out planted malicious activity today
                is_scen_1 = (uid == "USR_RET_04" and day in self.ground_truth_threats["USR_RET_04"]["attack_days"])
                is_scen_2 = (uid == "USR_TRD_02" and day in self.ground_truth_threats["USR_TRD_02"]["attack_days"])
                is_scen_3 = (uid == "USR_IT_01" and day in self.ground_truth_threats["USR_IT_01"]["attack_days"])
                is_scen_4 = (uid == "USR_WLT_03" and day in self.ground_truth_threats["USR_WLT_03"]["attack_days"])

                # Normal Weekend Behavior: 98% of users do not log in
                if is_weekend and not (is_scen_1 or is_scen_2 or is_scen_3):
                    if random.random() > 0.03:
                        continue  # No weekend activity

                # --- 1. LOGON / LOGOFF EVENTS ---
                if is_scen_2:
                    # Scenario 2: Rogue Trader logs in at 02:45 AM from an abnormal backup PC
                    logon_time = current_day_dt.replace(hour=2, minute=random.randint(35, 55), second=random.randint(0, 59))
                    logoff_time = logon_time + timedelta(hours=random.uniform(1.5, 3.0))
                    pc = "PC-TRD-BACKUP-09"  # Rogue abnormal PC
                    self.container.logon_logs.append(LogonRecord(
                        event_id=f"EVT-LGN-{event_id_seq}",
                        timestamp=logon_time.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation=pc,
                        activity="Logon",
                        auth_method="NTLM-Fallback",
                        source_ip="10.20.99.144"
                    ))
                    event_id_seq += 1
                    self.container.logon_logs.append(LogonRecord(
                        event_id=f"EVT-LGN-{event_id_seq}",
                        timestamp=logoff_time.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation=pc,
                        activity="Logoff",
                        auth_method="NTLM-Fallback",
                        source_ip="10.20.99.144"
                    ))
                    event_id_seq += 1

                elif is_scen_1:
                    # Scenario 1: Alice Walker logs in during normal hours AND off-hours (22:45 PM)
                    # Normal shift
                    l_in = current_day_dt.replace(hour=8, minute=random.randint(30, 55))
                    l_out = current_day_dt.replace(hour=17, minute=random.randint(15, 45))
                    self._add_logon_pair(l_in, l_out, uid, user.workstation, event_id_seq)
                    event_id_seq += 2

                    # Suspicious Late Night Shift
                    night_in = current_day_dt.replace(hour=22, minute=random.randint(15, 40))
                    night_out = night_in + timedelta(hours=random.uniform(2.5, 3.5))
                    self._add_logon_pair(night_in, night_out, uid, user.workstation, event_id_seq)
                    event_id_seq += 2

                elif is_scen_3:
                    # Scenario 3: DBA Devon Reed connects to SWIFT server after hours (23:15)
                    normal_in = current_day_dt.replace(hour=9, minute=random.randint(0, 15))
                    normal_out = current_day_dt.replace(hour=18, minute=random.randint(0, 30))
                    self._add_logon_pair(normal_in, normal_out, uid, user.workstation, event_id_seq)
                    event_id_seq += 2

                    # Lateral move to SWIFT terminal
                    swift_in = current_day_dt.replace(hour=23, minute=random.randint(10, 25))
                    swift_out = swift_in + timedelta(hours=1.8)
                    self._add_logon_pair(swift_in, swift_out, uid, "PC-SWIFT-SRV-01", event_id_seq, auth="Admin-Elevation")
                    event_id_seq += 2

                else:
                    # Standard Normal employee day
                    in_h = random.randint(8, 9)
                    in_m = random.randint(10, 55)
                    out_h = random.randint(17, 18)
                    out_m = random.randint(5, 50)
                    l_in = current_day_dt.replace(hour=in_h, minute=in_m)
                    l_out = current_day_dt.replace(hour=out_h, minute=out_m)
                    self._add_logon_pair(l_in, l_out, uid, user.workstation, event_id_seq)
                    event_id_seq += 2

                # --- 2. FILE ACCESS EVENTS ---
                if is_scen_1:
                    # Mass customer PII extraction
                    for _ in range(random.randint(15, 25)):
                        t_stamp = current_day_dt.replace(hour=23, minute=random.randint(5, 55))
                        sens_file = random.choice(dept_info["sensitive_files"])
                        self.container.file_logs.append(FileRecord(
                            event_id=f"EVT-FIL-{event_id_seq}",
                            timestamp=t_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                            user_id=uid,
                            workstation=user.workstation,
                            filename=sens_file,
                            file_path=f"D:\\CorporateBanking\\Restricted\\{sens_file}",
                            activity="Copy",
                            content_length_bytes=random.randint(50_000_000, 350_000_000),
                            is_sensitive=True,
                            classification="Confidential / PII"
                        ))
                        event_id_seq += 1

                elif is_scen_2:
                    # Rogue trader modifies risk ledger at 03:00 AM
                    for sens_file in dept_info["sensitive_files"]:
                        t_stamp = current_day_dt.replace(hour=3, minute=random.randint(5, 45))
                        self.container.file_logs.append(FileRecord(
                            event_id=f"EVT-FIL-{event_id_seq}",
                            timestamp=t_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                            user_id=uid,
                            workstation="PC-TRD-BACKUP-09",
                            filename=sens_file,
                            file_path=f"C:\\TradingEngine\\Config\\{sens_file}",
                            activity="Modify",
                            content_length_bytes=random.randint(5_000_000, 20_000_000),
                            is_sensitive=True,
                            classification="Banking-Secret / Core Ledger"
                        ))
                        event_id_seq += 1

                elif is_scen_3:
                    # DBA deletes audit log files and extracts SWIFT keys
                    t_stamp = current_day_dt.replace(hour=23, minute=45)
                    self.container.file_logs.append(FileRecord(
                        event_id=f"EVT-FIL-{event_id_seq}",
                        timestamp=t_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation="PC-SWIFT-SRV-01",
                        filename="db_transaction_audit.log",
                        file_path="C:\\Windows\\System32\\winevt\\Logs\\db_transaction_audit.log",
                        activity="Delete",
                        content_length_bytes=0,
                        is_sensitive=True,
                        classification="System-Integrity"
                    ))
                    event_id_seq += 1
                    t_stamp2 = current_day_dt.replace(hour=23, minute=52)
                    self.container.file_logs.append(FileRecord(
                        event_id=f"EVT-FIL-{event_id_seq}",
                        timestamp=t_stamp2.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation="PC-SWIFT-SRV-01",
                        filename="swift_wire_credentials.enc",
                        file_path="E:\\Vault\\Keys\\swift_wire_credentials.enc",
                        activity="Read",
                        content_length_bytes=1048576,
                        is_sensitive=True,
                        classification="Banking-Secret"
                    ))
                    event_id_seq += 1

                elif is_scen_4:
                    # Wealth manager copies HNW client portfolios
                    for sens_file in dept_info["sensitive_files"]:
                        t_stamp = current_day_dt.replace(hour=13, minute=random.randint(10, 45))
                        self.container.file_logs.append(FileRecord(
                            event_id=f"EVT-FIL-{event_id_seq}",
                            timestamp=t_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                            user_id=uid,
                            workstation=user.workstation,
                            filename=sens_file,
                            file_path=f"S:\\Wealth\\Portfolios\\{sens_file}",
                            activity="Read",
                            content_length_bytes=random.randint(10_000_000, 80_000_000),
                            is_sensitive=True,
                            classification="Restricted Client PII"
                        ))
                        event_id_seq += 1

                else:
                    # Normal file activities (1-4 per day)
                    for _ in range(random.randint(1, 4)):
                        t_stamp = current_day_dt.replace(hour=random.randint(10, 16), minute=random.randint(0, 59))
                        norm_file = random.choice(dept_info["normal_files"])
                        self.container.file_logs.append(FileRecord(
                            event_id=f"EVT-FIL-{event_id_seq}",
                            timestamp=t_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                            user_id=uid,
                            workstation=user.workstation,
                            filename=norm_file,
                            file_path=f"C:\\Users\\{user.employee_name.replace(' ', '.')}\\Documents\\{norm_file}",
                            activity="Read",
                            content_length_bytes=random.randint(10_000, 2_000_000),
                            is_sensitive=False,
                            classification="Internal"
                        ))
                        event_id_seq += 1

                # --- 3. DEVICE (USB) EVENTS ---
                if is_scen_1:
                    # Connects unapproved SanDisk 64GB drive late night and transfers 3.8GB
                    conn_t = current_day_dt.replace(hour=23, minute=48)
                    self.container.device_logs.append(DeviceRecord(
                        event_id=f"EVT-DEV-{event_id_seq}",
                        timestamp=conn_t.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation=user.workstation,
                        activity="Connect",
                        device_vendor="SanDisk Extreme PRO",
                        device_serial="SN-EXT-9981-USB",
                        data_transferred_mb=3850.5
                    ))
                    event_id_seq += 1
                    disconn_t = conn_t + timedelta(minutes=18)
                    self.container.device_logs.append(DeviceRecord(
                        event_id=f"EVT-DEV-{event_id_seq}",
                        timestamp=disconn_t.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation=user.workstation,
                        activity="Disconnect",
                        device_vendor="SanDisk Extreme PRO",
                        device_serial="SN-EXT-9981-USB",
                        data_transferred_mb=0.0
                    ))
                    event_id_seq += 1
                elif user.department == "Core IT & Infrastructure" and random.random() < 0.05:
                    # Legitimate IT backup drive
                    conn_t = current_day_dt.replace(hour=14, minute=20)
                    self.container.device_logs.append(DeviceRecord(
                        event_id=f"EVT-DEV-{event_id_seq}",
                        timestamp=conn_t.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation=user.workstation,
                        activity="Connect",
                        device_vendor="Kingston Encrypted IronKey",
                        device_serial="IK-SEC-0044",
                        data_transferred_mb=120.0
                    ))
                    event_id_seq += 1

                # --- 4. EMAIL EXFILTRATION & COMMUNICATION ---
                if is_scen_1:
                    # Sends encrypted attachments to external personal email
                    mail_t = current_day_dt.replace(hour=23, minute=58)
                    self.container.email_logs.append(EmailRecord(
                        event_id=f"EVT-EML-{event_id_seq}",
                        timestamp=mail_t.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation=user.workstation,
                        sender=user.email,
                        to_recipients=["alice.personal.archive@proton.me"],
                        subject="Personal Backup Archives [PW: 12345]",
                        size_bytes=48_500_000,
                        attachment_count=3,
                        attachments=["customer_ssn_database.zip.gpg", "kyc_passports.zip.gpg"],
                        is_external=True
                    ))
                    event_id_seq += 1
                else:
                    # Normal internal emails (2-5 per day)
                    for _ in range(random.randint(2, 5)):
                        mail_t = current_day_dt.replace(hour=random.randint(9, 17), minute=random.randint(0, 59))
                        colleague = random.choice(users)
                        self.container.email_logs.append(EmailRecord(
                            event_id=f"EVT-EML-{event_id_seq}",
                            timestamp=mail_t.strftime("%Y-%m-%d %H:%M:%S"),
                            user_id=uid,
                            workstation=user.workstation,
                            sender=user.email,
                            to_recipients=[colleague.email],
                            subject=f"RE: {user.department} Operations Update",
                            size_bytes=random.randint(12_000, 250_000),
                            attachment_count=1 if random.random() < 0.2 else 0,
                            attachments=["status_report.pdf"] if random.random() < 0.2 else [],
                            is_external=False
                        ))
                        event_id_seq += 1

                # --- 5. HTTP & CLOUD UPLOAD EVENTS ---
                if is_scen_4:
                    # Wealth manager uploads client files to Mega.nz
                    http_t = current_day_dt.replace(hour=13, minute=25)
                    url, cat = SUSPICIOUS_DOMAINS[0]  # mega.nz
                    self.container.http_logs.append(HttpRecord(
                        event_id=f"EVT-HTP-{event_id_seq}",
                        timestamp=http_t.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id=uid,
                        workstation=user.workstation,
                        url=url,
                        domain="mega.nz",
                        category=cat,
                        bytes_uploaded=850_000_000,
                        bytes_downloaded=12_000,
                        http_method="POST"
                    ))
                    event_id_seq += 1
                else:
                    # Normal web browsing (3-6 sessions per day)
                    for _ in range(random.randint(3, 6)):
                        http_t = current_day_dt.replace(hour=random.randint(9, 17), minute=random.randint(0, 59))
                        url, cat = random.choice(NORMAL_DOMAINS)
                        domain = url.split("/")[2]
                        self.container.http_logs.append(HttpRecord(
                            event_id=f"EVT-HTP-{event_id_seq}",
                            timestamp=http_t.strftime("%Y-%m-%d %H:%M:%S"),
                            user_id=uid,
                            workstation=user.workstation,
                            url=url,
                            domain=domain,
                            category=cat,
                            bytes_uploaded=random.randint(2000, 40_000),
                            bytes_downloaded=random.randint(50_000, 1_500_000),
                            http_method="GET"
                        ))
                        event_id_seq += 1

        return self.container, self.ground_truth_threats

    def _add_logon_pair(self, l_in: datetime, l_out: datetime, uid: str, pc: str,
                        seq: int, auth: str = "Kerberos"):
        self.container.logon_logs.append(LogonRecord(
            event_id=f"EVT-LGN-{seq}",
            timestamp=l_in.strftime("%Y-%m-%d %H:%M:%S"),
            user_id=uid,
            workstation=pc,
            activity="Logon",
            auth_method=auth,
            source_ip="10.20.4.15"
        ))
        self.container.logon_logs.append(LogonRecord(
            event_id=f"EVT-LGN-{seq+1}",
            timestamp=l_out.strftime("%Y-%m-%d %H:%M:%S"),
            user_id=uid,
            workstation=pc,
            activity="Logoff",
            auth_method=auth,
            source_ip="10.20.4.15"
        ))
