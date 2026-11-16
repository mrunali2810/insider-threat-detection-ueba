"""
Hybrid Risk Fusion Scorer for Banking Insider Threats.

Synthesizes UEBA statistical profile deviations, Deep Learning temporal reconstruction
errors, and financial contextual risk factors (role privileges, HR status, critical asset access)
into a unified threat score with regulatory compliance impact assessment.
"""

from typing import Dict, Any, List, Optional
from data.cert_schema import LdapRecord


class HybridRiskScorer:
    """Combines statistical UEBA and deep sequence modeling with banking domain heuristics."""

    def __init__(self, ueba_weight: float = 0.55):
        self.ueba_weight = ueba_weight
        self.dl_weight = 1.0 - ueba_weight

    def compute_hybrid_risk(
        self,
        ueba_result: Dict[str, Any],
        dl_result: Dict[str, Any],
        user_meta: Optional[LdapRecord] = None
    ) -> Dict[str, Any]:
        """
        Merges UEBA and DL scores, computes contextual banking risk multipliers,
        and determines threat classification tier.
        """
        u_score = ueba_result.get("ueba_score", 0.0)
        d_score = dl_result.get("dl_score", 0.0)

        # Baseline linear blend
        blended_score = (self.ueba_weight * u_score) + (self.dl_weight * d_score)

        # Contextual Banking Risk Modifiers
        context_boost = 0.0
        context_flags = []

        if user_meta:
            # HR Risk Indicators (Flight Risk / Disgruntled Insider)
            if user_meta.is_resigned:
                context_boost += 12.0
                context_flags.append(f"Flight Risk: Pending Resignation ({user_meta.resignation_effective_date})")
            if "PIP" in user_meta.performance_rating or "Needs Improvement" in user_meta.performance_rating:
                context_boost += 8.0
                context_flags.append(f"Disciplinary Flag: {user_meta.performance_rating}")

            # Privilege Level Multipliers
            if "Administrator" in user_meta.role or "DBA" in user_meta.role:
                context_boost += 6.0
                context_flags.append("High-Value Privilege: Core Infrastructure / DBA Root")
            elif "Trader" in user_meta.role:
                context_boost += 5.0
                context_flags.append("High-Value Privilege: Capital Markets Trading Authority")

        # Co-detection Nexus Boost: If both UEBA and DL agree on extreme anomaly
        if u_score >= 60.0 and d_score >= 60.0:
            context_boost += 8.0
            context_flags.append("Multi-Model Consensus: Both UEBA & Deep Learning Confirmed Anomaly")

        final_score = min(100.0, blended_score + context_boost)

        # Threat Tier Assignment
        if final_score >= 80.0:
            threat_tier = "CRITICAL"
        elif final_score >= 60.0:
            threat_tier = "HIGH_RISK"
        elif final_score >= 40.0:
            threat_tier = "SUSPICIOUS"
        else:
            threat_tier = "BENIGN"

        # Financial Exposure & Compliance Assessment
        compliance_violations = []
        financial_impact_estimate = "$0 (Negligible)"

        raw_feats = ueba_result.get("raw_features", {})
        sensitive_count = raw_feats.get("sensitive_files_accessed", 0)
        usb_mb = raw_feats.get("usb_data_volume_mb", 0)
        cloud_mb = raw_feats.get("cloud_storage_uploads_mb", 0)
        mod_del = raw_feats.get("file_mod_del_events", 0)

        if sensitive_count > 0 and (usb_mb > 0 or cloud_mb > 0):
            compliance_violations.append("GLBA 501(b) Customer Information Safeguards Rule")
            compliance_violations.append("PCI-DSS Req 10.2 (Cardholder Data Protection)")
            est_records = int(sensitive_count * 1250)
            financial_impact_estimate = f"${est_records * 165:,} (Estimated Data Breach & Legal Liabilities)"

        if mod_del > 0:
            compliance_violations.append("SOX Section 404 (Internal Control over Financial Reporting)")
            compliance_violations.append("FINRA Rule 3110 (Books and Records Integrity)")
            if financial_impact_estimate == "$0 (Negligible)":
                financial_impact_estimate = "$500,000 - $2,500,000 (Regulatory Sanctions & Audit Recalibration)"

        return {
            "user_id": ueba_result["user_id"],
            "date": ueba_result["date"],
            "department": ueba_result["department"],
            "role": ueba_result["role"],
            "employee_name": user_meta.employee_name if user_meta else "Unknown",
            "hybrid_score": round(final_score, 1),
            "ueba_score": u_score,
            "dl_score": d_score,
            "dl_reconstruction_error": dl_result.get("dl_reconstruction_error", 0.0),
            "dl_error_ratio": dl_result.get("dl_error_ratio", 0.0),
            "threat_tier": threat_tier,
            "context_flags": context_flags,
            "high_risk_drivers": ueba_result.get("high_risk_drivers", []),
            "nexus_triggers": ueba_result.get("nexus_triggers", []),
            "compliance_violations": compliance_violations,
            "financial_impact_estimate": financial_impact_estimate,
            "raw_features": raw_feats
        }
