"""
UEBA (User & Entity Behavior Analytics) Feature Extraction Engine.

Aggregates raw multi-modal CERT enterprise logs into behavioral time-series
vectors representing individual user activity per day.
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any, Tuple
import math

from data.cert_schema import CertDatasetContainer


FEATURE_NAMES = [
    "total_logons",
    "after_hours_logons",
    "distinct_workstations",
    "usb_connect_events",
    "usb_data_volume_mb",
    "files_accessed_count",
    "sensitive_files_accessed",
    "file_mod_del_events",
    "external_emails_sent",
    "email_attachments_mb",
    "cloud_storage_uploads_mb",
    "abnormal_workstation_used"
]


class UebaFeatureExtractor:
    """Transforms raw CERT log streams into daily behavioral feature vectors."""

    def __init__(self, container: CertDatasetContainer):
        self.container = container
        self.users = container.users

    def _is_after_hours(self, dt: datetime) -> bool:
        """Returns True if event timestamp is on weekend or outside 08:00 - 18:00."""
        if dt.weekday() >= 5:  # Saturday or Sunday
            return True
        if dt.hour < 8 or dt.hour >= 18:
            return True
        return False

    def extract_daily_vectors(self) -> List[Dict[str, Any]]:
        """
        Processes all logs in container and aggregates by (user_id, date).
        Returns a list of daily feature dictionaries.
        """
        # Intermediate aggregation map: (user_id, date_str) -> metric_dict
        daily_map = defaultdict(lambda: {
            "total_logons": 0,
            "after_hours_logons": 0,
            "workstations": set(),
            "usb_connect_events": 0,
            "usb_data_volume_mb": 0.0,
            "files_accessed_count": 0,
            "sensitive_files_accessed": 0,
            "file_mod_del_events": 0,
            "external_emails_sent": 0,
            "email_attachments_mb": 0.0,
            "cloud_storage_uploads_mb": 0.0,
            "abnormal_workstation_used": 0,
        })

        # 1. Process Logon Logs
        for r in self.container.logon_logs:
            if r.activity != "Logon":
                continue
            dt = datetime.strptime(r.timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
            entry = daily_map[(r.user_id, date_str)]
            entry["total_logons"] += 1
            if self._is_after_hours(dt):
                entry["after_hours_logons"] += 1
            entry["workstations"].add(r.workstation)

            # Check if workstation is abnormal for this user
            assigned_pc = self.users.get(r.user_id).workstation if r.user_id in self.users else None
            if assigned_pc and r.workstation != assigned_pc:
                entry["abnormal_workstation_used"] = 1

        # 2. Process Device (USB) Logs
        for r in self.container.device_logs:
            dt = datetime.strptime(r.timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
            entry = daily_map[(r.user_id, date_str)]
            if r.activity == "Connect":
                entry["usb_connect_events"] += 1
            entry["usb_data_volume_mb"] += r.data_transferred_mb

        # 3. Process File Logs
        for r in self.container.file_logs:
            dt = datetime.strptime(r.timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
            entry = daily_map[(r.user_id, date_str)]
            entry["files_accessed_count"] += 1
            if r.is_sensitive:
                entry["sensitive_files_accessed"] += 1
            if r.activity in ["Modify", "Delete"]:
                entry["file_mod_del_events"] += 1

        # 4. Process Email Logs
        for r in self.container.email_logs:
            dt = datetime.strptime(r.timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
            entry = daily_map[(r.user_id, date_str)]
            if r.is_external:
                entry["external_emails_sent"] += 1
            entry["email_attachments_mb"] += (r.size_bytes / (1024 * 1024))

        # 5. Process HTTP Logs
        for r in self.container.http_logs:
            dt = datetime.strptime(r.timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
            entry = daily_map[(r.user_id, date_str)]
            if r.category in ["Cloud Storage", "Personal Webmail", "Dark Web"] or r.bytes_uploaded > 5_000_000:
                entry["cloud_storage_uploads_mb"] += (r.bytes_uploaded / (1024 * 1024))

        # Flatten into final feature vectors
        records = []
        for (user_id, date_str), data in daily_map.items():
            user_meta = self.users.get(user_id)
            dept = user_meta.department if user_meta else "Unknown"
            role = user_meta.role if user_meta else "Unknown"

            feat_vector = [
                float(data["total_logons"]),
                float(data["after_hours_logons"]),
                float(len(data["workstations"])),
                float(data["usb_connect_events"]),
                float(data["usb_data_volume_mb"]),
                float(data["files_accessed_count"]),
                float(data["sensitive_files_accessed"]),
                float(data["file_mod_del_events"]),
                float(data["external_emails_sent"]),
                float(data["email_attachments_mb"]),
                float(data["cloud_storage_uploads_mb"]),
                float(data["abnormal_workstation_used"]),
            ]

            records.append({
                "user_id": user_id,
                "date": date_str,
                "department": dept,
                "role": role,
                "features": dict(zip(FEATURE_NAMES, feat_vector)),
                "raw_vector": feat_vector
            })

        # Sort chronologically by date and user
        records.sort(key=lambda x: (x["date"], x["user_id"]))
        return records
