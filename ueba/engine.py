"""
UEBA Profiling and Statistical Anomaly Engine.

Computes dynamic user baselines, peer group cohort norms, multivariate Z-scores,
and domain-weighted risk metrics for enterprise banking security.
"""

from collections import defaultdict
import math
from typing import Dict, List, Any, Tuple

from .features import FEATURE_NAMES


# Financial threat risk weights per feature
FEATURE_WEIGHTS = {
    "total_logons": 0.5,
    "after_hours_logons": 2.5,
    "distinct_workstations": 1.5,
    "usb_connect_events": 2.5,
    "usb_data_volume_mb": 4.0,
    "files_accessed_count": 1.0,
    "sensitive_files_accessed": 3.5,
    "file_mod_del_events": 3.5,
    "external_emails_sent": 2.0,
    "email_attachments_mb": 3.0,
    "cloud_storage_uploads_mb": 4.0,
    "abnormal_workstation_used": 3.0
}


class UebaProfilingEngine:
    """Calculates statistical baselines and anomaly deviation scores."""

    def __init__(self):
        self.peer_baselines: Dict[str, Dict[str, Tuple[float, float]]] = {}  # dept -> {feat: (mean, std)}
        self.user_baselines: Dict[str, Dict[str, Tuple[float, float]]] = {}  # uid -> {feat: (mean, std)}
        self.is_fitted = False

    def fit_baselines(self, historical_records: List[Dict[str, Any]]):
        """Learns baseline distributions per peer group (department) and per user."""
        dept_samples = defaultdict(lambda: defaultdict(list))
        user_samples = defaultdict(lambda: defaultdict(list))

        for rec in historical_records:
            dept = rec["department"]
            uid = rec["user_id"]
            feats = rec["features"]

            for fname in FEATURE_NAMES:
                val = float(feats.get(fname, 0.0))
                dept_samples[dept][fname].append(val)
                user_samples[uid][fname].append(val)

        # Compute Peer (Department) Baselines
        for dept, fmap in dept_samples.items():
            self.peer_baselines[dept] = {}
            for fname, values in fmap.items():
                mean, std = self._calc_mean_std(values)
                self.peer_baselines[dept][fname] = (mean, max(std, 0.05))  # Min std to avoid div by zero

        # Compute User Baselines
        for uid, fmap in user_samples.items():
            self.user_baselines[uid] = {}
            for fname, values in fmap.items():
                mean, std = self._calc_mean_std(values)
                self.user_baselines[uid][fname] = (mean, max(std, 0.05))

        self.is_fitted = True

    def _calc_mean_std(self, vals: List[float]) -> Tuple[float, float]:
        if not vals:
            return 0.0, 1.0
        n = len(vals)
        mean = sum(vals) / n
        if n < 2:
            return mean, 1.0
        variance = sum((x - mean) ** 2 for x in vals) / (n - 1)
        return mean, math.sqrt(variance)

    def score_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes the UEBA risk score and behavioral deviations for a single user-day record.
        Returns detailed risk breakdowns, Z-scores, and co-occurrence flags.
        """
        if not self.is_fitted:
            raise RuntimeError("UEBA engine must be fitted with historical records before scoring.")

        uid = record["user_id"]
        dept = record["department"]
        feats = record["features"]

        peer_baseline = self.peer_baselines.get(dept, {})
        user_baseline = self.user_baselines.get(uid, peer_baseline)

        feature_zscores: Dict[str, float] = {}
        weighted_z_sum = 0.0
        total_weight = sum(FEATURE_WEIGHTS.values())
        high_risk_drivers: List[str] = []

        for fname in FEATURE_NAMES:
            val = float(feats.get(fname, 0.0))
            p_mean, p_std = peer_baseline.get(fname, (0.0, 1.0))
            u_mean, u_std = user_baseline.get(fname, (p_mean, p_std))

            # Z-score deviations (only positive deviations represent threat spikes)
            z_peer = max(0.0, (val - p_mean) / p_std)
            z_self = max(0.0, (val - u_mean) / u_std)

            # Blended Z-score: 40% peer deviation, 60% individual baseline drift
            blended_z = 0.4 * z_peer + 0.6 * z_self
            feature_zscores[fname] = round(blended_z, 3)

            w = FEATURE_WEIGHTS[fname]
            weighted_z_sum += (blended_z * w)

            if blended_z >= 2.5 and val > 0:
                high_risk_drivers.append(f"{fname} (Z={blended_z:.1f}, Val={val:.1f})")

        # Base composite score
        base_score = (weighted_z_sum / total_weight) * 20.0

        # Non-linear Compound Threat Multiplier:
        # Check classic insider threat nexus (After-hours + Data Extraction + Exfiltration)
        has_off_hours = feats.get("after_hours_logons", 0) > 0
        has_sens_files = feats.get("sensitive_files_accessed", 0) > 0
        has_exfil = (feats.get("usb_data_volume_mb", 0) > 100 or
                     feats.get("cloud_storage_uploads_mb", 0) > 100 or
                     feats.get("email_attachments_mb", 0) > 20)
        has_sabotage = feats.get("file_mod_del_events", 0) > 0
        has_abnormal_pc = feats.get("abnormal_workstation_used", 0) > 0

        multiplier = 1.0
        nexus_triggers = []

        if has_off_hours and has_sens_files:
            multiplier += 0.4
            nexus_triggers.append("Off-Hours Sensitive Data Access")
        if has_sens_files and has_exfil:
            multiplier += 0.6
            nexus_triggers.append("Sensitive Data Staging & Exfiltration Nexus")
        if has_off_hours and has_abnormal_pc:
            multiplier += 0.5
            nexus_triggers.append("Off-Hours Abnormal Terminal Access")
        if has_sabotage and has_off_hours:
            multiplier += 0.5
            nexus_triggers.append("Off-Hours Ledger/Log Manipulation")

        final_ueba_score = min(100.0, base_score * multiplier)

        return {
            "user_id": uid,
            "date": record["date"],
            "department": dept,
            "role": record["role"],
            "ueba_score": round(final_ueba_score, 2),
            "feature_zscores": feature_zscores,
            "high_risk_drivers": high_risk_drivers,
            "nexus_triggers": nexus_triggers,
            "raw_features": feats
        }
