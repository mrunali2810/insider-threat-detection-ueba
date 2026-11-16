"""
CERT Insider Threat Dataset Schema & Data Structures for Banking & Finance.

Standardized schemas representing multi-modal enterprise logs aligned with
CMU CERT Insider Threat dataset formats (r4.2, r5.2, r6.2) and tailored
specifically for Banking & Financial Institutions.
"""

import csv
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class LdapRecord:
    """Enterprise Employee Directory Record (HR / Active Directory)."""
    user_id: str
    employee_name: str
    email: str
    role: str
    department: str  # Retail Banking, Trading & Markets, Wealth Management, Core IT, Compliance
    clearance_level: str  # Confidential, Secret, Top Secret / Executive
    supervisor: str
    workstation: str
    is_resigned: bool = False
    resignation_effective_date: Optional[str] = None
    performance_rating: str = "Meets Expectations"  # Exceeds, Meets, Needs Improvement, PIP


@dataclass
class LogonRecord:
    """Logon / Logoff Event Record (logon.csv)."""
    event_id: str
    timestamp: str  # ISO Format: YYYY-MM-DD HH:MM:SS
    user_id: str
    workstation: str
    activity: str  # 'Logon' or 'Logoff'
    auth_method: str = "Kerberos"
    source_ip: str = "10.20.4.15"


@dataclass
class DeviceRecord:
    """Removable Storage / USB Activity Record (device.csv)."""
    event_id: str
    timestamp: str
    user_id: str
    workstation: str
    activity: str  # 'Connect' or 'Disconnect'
    device_vendor: str = "SanDisk"
    device_serial: str = "SN-9824-USB"
    data_transferred_mb: float = 0.0


@dataclass
class FileRecord:
    """File System Access & Staging Record (file.csv)."""
    event_id: str
    timestamp: str
    user_id: str
    workstation: str
    filename: str
    file_path: str
    activity: str  # 'Open', 'Read', 'Copy', 'Modify', 'Delete'
    content_length_bytes: int = 0
    is_sensitive: bool = False
    classification: str = "Internal"  # Public, Internal, Restricted, Confidential, Banking-Secret


@dataclass
class EmailRecord:
    """Corporate Email Record (email.csv)."""
    event_id: str
    timestamp: str
    user_id: str
    workstation: str
    sender: str
    to_recipients: List[str]
    cc_recipients: List[str] = field(default_factory=list)
    bcc_recipients: List[str] = field(default_factory=list)
    subject: str = ""
    size_bytes: int = 1024
    attachment_count: int = 0
    attachments: List[str] = field(default_factory=list)
    is_external: bool = False


@dataclass
class HttpRecord:
    """Web Proxy & Cloud Storage Navigation Record (http.csv)."""
    event_id: str
    timestamp: str
    user_id: str
    workstation: str
    url: str
    domain: str
    category: str  # Financial News, Intranet, Personal Webmail, Cloud Storage, Social Media, Dark Web
    bytes_uploaded: int = 0
    bytes_downloaded: int = 0
    http_method: str = "GET"


class CertDatasetContainer:
    """Holds collections of all multi-modal CERT enterprise logs."""

    def __init__(self):
        self.users: Dict[str, LdapRecord] = {}
        self.logon_logs: List[LogonRecord] = []
        self.device_logs: List[DeviceRecord] = []
        self.file_logs: List[FileRecord] = []
        self.email_logs: List[EmailRecord] = []
        self.http_logs: List[HttpRecord] = []

    def summary(self) -> Dict[str, int]:
        return {
            "users": len(self.users),
            "logon_events": len(self.logon_logs),
            "device_events": len(self.device_logs),
            "file_events": len(self.file_logs),
            "email_events": len(self.email_logs),
            "http_events": len(self.http_logs),
        }

    def export_to_csv(self, output_dir: str):
        """Export all data streams to standard CERT CSV format."""
        os.makedirs(output_dir, exist_ok=True)

        # 1. Export LDAP
        ldap_path = os.path.join(output_dir, "ldap.csv")
        with open(ldap_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "employee_name", "email", "role", "department",
                             "clearance_level", "supervisor", "workstation", "is_resigned",
                             "resignation_effective_date", "performance_rating"])
            for u in self.users.values():
                writer.writerow([u.user_id, u.employee_name, u.email, u.role, u.department,
                                 u.clearance_level, u.supervisor, u.workstation, u.is_resigned,
                                 u.resignation_effective_date or "", u.performance_rating])

        # 2. Export Logon
        logon_path = os.path.join(output_dir, "logon.csv")
        with open(logon_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "user", "pc", "activity", "auth_method", "source_ip"])
            for r in self.logon_logs:
                writer.writerow([r.event_id, r.timestamp, r.user_id, r.workstation,
                                 r.activity, r.auth_method, r.source_ip])

        # 3. Export Device
        device_path = os.path.join(output_dir, "device.csv")
        with open(device_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "user", "pc", "activity", "device_vendor",
                             "device_serial", "data_transferred_mb"])
            for r in self.device_logs:
                writer.writerow([r.event_id, r.timestamp, r.user_id, r.workstation,
                                 r.activity, r.device_vendor, r.device_serial, r.data_transferred_mb])

        # 4. Export File
        file_path = os.path.join(output_dir, "file.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "user", "pc", "filename", "file_path",
                             "activity", "content_length_bytes", "is_sensitive", "classification"])
            for r in self.file_logs:
                writer.writerow([r.event_id, r.timestamp, r.user_id, r.workstation,
                                 r.filename, r.file_path, r.activity, r.content_length_bytes,
                                 r.is_sensitive, r.classification])

        # 5. Export Email
        email_path = os.path.join(output_dir, "email.csv")
        with open(email_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "user", "pc", "from", "to", "cc", "bcc",
                             "subject", "size_bytes", "attachment_count", "attachments", "is_external"])
            for r in self.email_logs:
                writer.writerow([r.event_id, r.timestamp, r.user_id, r.workstation,
                                 r.sender, ";".join(r.to_recipients), ";".join(r.cc_recipients),
                                 ";".join(r.bcc_recipients), r.subject, r.size_bytes,
                                 r.attachment_count, ";".join(r.attachments), r.is_external])

        # 6. Export HTTP
        http_path = os.path.join(output_dir, "http.csv")
        with open(http_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "user", "pc", "url", "domain", "category",
                             "bytes_uploaded", "bytes_downloaded", "http_method"])
            for r in self.http_logs:
                writer.writerow([r.event_id, r.timestamp, r.user_id, r.workstation,
                                 r.url, r.domain, r.category, r.bytes_uploaded,
                                 r.bytes_downloaded, r.http_method])
