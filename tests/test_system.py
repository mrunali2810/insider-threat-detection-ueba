"""
Unit & Integration Test Suite for Banking Insider Threat Detection Platform.

Tests:
1. CERT Schema & Banking Generator Integrity
2. UEBA Feature Extraction & Behavioral Vectorization
3. UEBA Profiling Engine & Multivariate Deviation Scoring
4. Deep Learning Sequence Anomaly Detector Convergence & Scoring
5. Hybrid Risk Fusion & Regulatory Mapping
6. Multi-Agent AI Incident Response & SAR Generation
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.banking_cert_generator import BankingCertDatasetGenerator
from ueba.features import UebaFeatureExtractor, FEATURE_NAMES
from ueba.engine import UebaProfilingEngine
from models.deep_anomaly_detector import DeepAnomalyDetector, PurePySequenceAutoencoder
from models.hybrid_scorer import HybridRiskScorer
from agents.soc_agents import (
    AlertTriageAgent,
    BehavioralProfilerAgent,
    ForensicHunterAgent,
    AutonomousResponseAgent,
    SOCOrchestrator
)


class TestBankingInsiderThreatPlatform(unittest.TestCase):
    """Integration and unit test cases for the entire platform."""

    @classmethod
    def setUpClass(cls):
        """Set up synthetic dataset once for test efficiency."""
        cls.generator = BankingCertDatasetGenerator(seed=42)
        cls.container, cls.ground_truth = cls.generator.generate(days=10)
        cls.extractor = UebaFeatureExtractor(cls.container)
        cls.daily_records = cls.extractor.extract_daily_vectors()

    def test_cert_dataset_generation(self):
        """Verify CERT dataset generation integrity and schema compliance."""
        summary = self.container.summary()
        self.assertGreater(summary["users"], 15, "Should generate enterprise banking identities")
        self.assertGreater(summary["logon_events"], 50, "Should generate logon/logoff events")
        self.assertGreater(summary["file_events"], 50, "Should generate file access events")
        self.assertGreater(summary["email_events"], 30, "Should generate email events")
        self.assertGreater(summary["http_events"], 30, "Should generate HTTP events")

        # Verify ground truth scenarios exist
        self.assertIn("USR_RET_04", self.ground_truth)
        self.assertIn("USR_TRD_02", self.ground_truth)
        self.assertIn("USR_IT_01", self.ground_truth)
        self.assertIn("USR_WLT_03", self.ground_truth)

    def test_ueba_feature_extraction(self):
        """Verify raw logs are correctly transformed into daily behavioral feature vectors."""
        self.assertGreater(len(self.daily_records), 0)
        first_rec = self.daily_records[0]
        self.assertIn("user_id", first_rec)
        self.assertIn("date", first_rec)
        self.assertIn("features", first_rec)
        self.assertEqual(len(first_rec["features"]), len(FEATURE_NAMES))

        # Check that feature vector contains non-negative values
        for fname in FEATURE_NAMES:
            self.assertGreaterEqual(first_rec["features"][fname], 0.0)

    def test_ueba_profiling_engine(self):
        """Verify statistical baselining and anomaly scoring."""
        engine = UebaProfilingEngine()
        engine.fit_baselines(self.daily_records)
        self.assertTrue(engine.is_fitted)

        # Baseline record scoring (should be low/moderate score)
        normal_rec = self.daily_records[0]
        normal_score = engine.score_record(normal_rec)
        self.assertLess(normal_score["ueba_score"], 60.0, "Normal activity should have moderate/low score")

        # Synthetic extreme anomaly record
        anomalous_rec = {
            "user_id": normal_rec["user_id"],
            "date": "2025-05-15",
            "department": normal_rec["department"],
            "role": normal_rec["role"],
            "features": {
                "total_logons": 5.0,
                "after_hours_logons": 4.0,
                "distinct_workstations": 2.0,
                "usb_connect_events": 3.0,
                "usb_data_volume_mb": 4500.0,
                "files_accessed_count": 30.0,
                "sensitive_files_accessed": 20.0,
                "file_mod_del_events": 2.0,
                "external_emails_sent": 5.0,
                "email_attachments_mb": 50.0,
                "cloud_storage_uploads_mb": 1200.0,
                "abnormal_workstation_used": 1.0
            }
        }
        anom_score = engine.score_record(anomalous_rec)
        self.assertGreater(anom_score["ueba_score"], 70.0, "Severe insider anomaly should score >= 70")
        self.assertGreater(len(anom_score["nexus_triggers"]), 0, "Nexus compound triggers should be tripped")

    def test_deep_sequence_autoencoder(self):
        """Verify deep learning sequence anomaly detector works and detects sequence deviations."""
        dl_detector = DeepAnomalyDetector(sequence_window=3, feature_dim=12)
        dl_detector.fit(self.daily_records, epochs=15)
        self.assertGreater(dl_detector.baseline_reconstruction_error, 0.0)

        scored = dl_detector.score_sequences(self.daily_records[:10])
        self.assertEqual(len(scored), 10)
        for s in scored:
            self.assertIn("dl_reconstruction_error", s)
            self.assertIn("dl_score", s)
            self.assertGreaterEqual(s["dl_score"], 0.0)
            self.assertLessEqual(s["dl_score"], 100.0)

    def test_hybrid_risk_scorer(self):
        """Verify hybrid fusion of UEBA, DL, and banking contextual risk modifiers."""
        scorer = HybridRiskScorer(ueba_weight=0.55)
        ueba_res = {
            "user_id": "USR_RET_04",
            "date": "2025-05-25",
            "department": "Retail Banking",
            "role": "Senior Loan Officer",
            "ueba_score": 85.0,
            "high_risk_drivers": ["usb_data_volume_mb (Z=5.2)"],
            "nexus_triggers": ["Sensitive Data Staging & Exfiltration Nexus"],
            "raw_features": {
                "sensitive_files_accessed": 15,
                "usb_data_volume_mb": 3800.0,
                "file_mod_del_events": 0
            }
        }
        dl_res = {
            "dl_score": 88.0,
            "dl_reconstruction_error": 0.45,
            "dl_error_ratio": 4.5
        }
        user_meta = self.container.users.get("USR_RET_04")

        result = scorer.compute_hybrid_risk(ueba_res, dl_res, user_meta)
        self.assertEqual(result["threat_tier"], "CRITICAL")
        self.assertGreater(result["hybrid_score"], 80.0)
        self.assertIn("GLBA 501(b) Customer Information Safeguards Rule", result["compliance_violations"])
        self.assertNotEqual(result["financial_impact_estimate"], "$0 (Negligible)")

    def test_agentic_soc_orchestration(self):
        """Verify multi-agent deliberation loop and FinCEN SAR generation."""
        threat_record = {
            "user_id": "USR_RET_04",
            "date": "2025-05-25",
            "employee_name": "Alice Walker",
            "department": "Retail Banking",
            "role": "Senior Loan Officer",
            "hybrid_score": 92.5,
            "ueba_score": 89.0,
            "dl_score": 94.0,
            "threat_tier": "CRITICAL",
            "compliance_violations": ["GLBA 501(b) Safeguards Rule"],
            "financial_impact_estimate": "$3,200,000"
        }
        user_meta = self.container.users.get("USR_RET_04")

        orchestrator = SOCOrchestrator()
        dossier = orchestrator.investigate(threat_record, self.container, user_meta)

        self.assertIn("investigation_id", dossier)
        self.assertEqual(len(dossier["agent_transcript"]), 4, "Should have transcripts from all 4 SOC agents")
        self.assertGreater(len(dossier["containment_summary"]), 0, "Should contain automated containment orders")
        self.assertIn("filing_institution", dossier["regulatory_filing"])
        self.assertIn("Alice Walker", dossier["regulatory_filing"]["narrative"])


if __name__ == "__main__":
    unittest.main()
