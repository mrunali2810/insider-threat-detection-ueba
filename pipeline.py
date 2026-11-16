"""
End-to-End Pipeline for Insider Threat Detection in Banking & Finance.

Integrates:
1. CERT Multi-Modal Dataset Generation (Logon, Device, File, Email, HTTP, LDAP)
2. UEBA Analytical Profiling & Multivariate Z-Score Baseline Engine
3. Deep Learning Sequence Anomaly Detection (Bi-LSTM / Deep Autoencoder)
4. Contextual Banking Risk Fusion & Regulatory Impact Scoring
5. Agentic AI Autonomous Incident Response & Triage Team
6. Dashboard Data Export
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, Any, List

from data.banking_cert_generator import BankingCertDatasetGenerator
from ueba.features import UebaFeatureExtractor
from ueba.engine import UebaProfilingEngine
from models.deep_anomaly_detector import DeepAnomalyDetector, HAS_TORCH
from models.hybrid_scorer import HybridRiskScorer
from agents.soc_agents import SOCOrchestrator


def run_pipeline(days: int = 30, output_dir: str = "./output") -> Dict[str, Any]:
    """Executes the full pipeline and returns complete structured analysis."""
    print("=" * 80)
    print("  FINANCIAL INSIDER THREAT DETECTION & AUTONOMOUS RESPONSE PLATFORM")
    print("  UEBA + CERT + Deep Learning + Agentic AI Architecture")
    print("=" * 80)

    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------
    # Step 1: Synthesize / Load CERT Banking Dataset
    # -------------------------------------------------------------
    print("\n[*] Step 1: Generating 30-Day Multi-Modal CERT Banking Dataset...")
    generator = BankingCertDatasetGenerator(seed=42)
    container, ground_truth = generator.generate(days=days)
    summary = container.summary()
    print(f"    [+] Identities Monitored: {summary['users']} employees across 5 banking units")
    print(f"    [+] Ingested Events: {summary['logon_events']} logons, {summary['device_events']} USB events, "
          f"{summary['file_events']} file accesses, {summary['email_events']} emails, {summary['http_events']} HTTP requests")
    print(f"    [+] Planted CERT Banking Scenarios: {len(ground_truth)} ground-truth threat actors")

    # Export raw CSVs for CERT compatibility
    csv_dir = os.path.join(output_dir, "cert_csv")
    container.export_to_csv(csv_dir)
    print(f"    [+] Exported standard CERT CSV logs to: {csv_dir}")

    # -------------------------------------------------------------
    # Step 2: Extract Daily UEBA Behavioral Vectors
    # -------------------------------------------------------------
    print("\n[*] Step 2: Extracting UEBA Behavioral Feature Vectors...")
    extractor = UebaFeatureExtractor(container)
    daily_records = extractor.extract_daily_vectors()
    print(f"    [+] Compiled {len(daily_records)} user-day behavioral vectors across {len(generator.container.users)} identities")

    # Split into Baseline (Days 1-18) and Active Monitoring (Days 19-30)
    baseline_records = [r for r in daily_records if int(r["date"].split("-")[2]) <= 18]
    eval_records = daily_records  # Score all days for comprehensive timeline

    # -------------------------------------------------------------
    # Step 3: UEBA Baseline Profiling & Statistical Scoring
    # -------------------------------------------------------------
    print("\n[*] Step 3: Training UEBA Statistical Baselines & Peer Cohort Norms...")
    ueba_engine = UebaProfilingEngine()
    ueba_engine.fit_baselines(baseline_records)
    print(f"    [+] Calibrated baselines for {len(ueba_engine.peer_baselines)} peer groups & {len(ueba_engine.user_baselines)} users")

    ueba_scored = [ueba_engine.score_record(r) for r in eval_records]

    # -------------------------------------------------------------
    # Step 4: Deep Learning Sequence Anomaly Detection
    # -------------------------------------------------------------
    print(f"\n[*] Step 4: Training Deep Sequence Autoencoder (Backend: {'PyTorch Bi-LSTM' if HAS_TORCH else 'Vectorized NumPy DL'})...")
    dl_detector = DeepAnomalyDetector(sequence_window=5, feature_dim=12)
    dl_detector.fit(baseline_records, epochs=35)
    print(f"    [+] Autoencoder converged. Baseline reconstruction error threshold: {dl_detector.baseline_reconstruction_error:.4f}")

    dl_scored = dl_detector.score_sequences(eval_records)

    # -------------------------------------------------------------
    # Step 5: Hybrid Risk Fusion & Compliance Impact Analysis
    # -------------------------------------------------------------
    print("\n[*] Step 5: Computing Hybrid Risk Fusion & Regulatory Exposure...")
    hybrid_scorer = HybridRiskScorer(ueba_weight=0.55)
    hybrid_results = []

    for i in range(len(eval_records)):
        u_res = ueba_scored[i]
        d_res = dl_scored[i]
        user_meta = container.users.get(u_res["user_id"])
        h_res = hybrid_scorer.compute_hybrid_risk(u_res, d_res, user_meta)
        hybrid_results.append(h_res)

    # Filter High & Critical Alerts
    critical_alerts = [r for r in hybrid_results if r["threat_tier"] in ["CRITICAL", "HIGH_RISK"]]
    print(f"    [+] Total Anomaly Alerts Identified: {len(critical_alerts)} high/critical risk events")

    # Group by user to find highest risk incident per user
    user_top_incidents: Dict[str, Dict[str, Any]] = {}
    for r in critical_alerts:
        uid = r["user_id"]
        if uid not in user_top_incidents or r["hybrid_score"] > user_top_incidents[uid]["hybrid_score"]:
            user_top_incidents[uid] = r

    # -------------------------------------------------------------
    # Step 6: Agentic AI Autonomous SOC Investigation Team
    # -------------------------------------------------------------
    print("\n[*] Step 6: Deploying Agentic AI Autonomous Incident Response Team...")
    orchestrator = SOCOrchestrator()
    investigation_dossiers = []

    for uid, top_alert in user_top_incidents.items():
        print(f"\n    [>>>] Commencing Multi-Agent Deliberation for {top_alert['employee_name']} ({uid})")
        print(f"          Department: {top_alert['department']} | Risk Score: {top_alert['hybrid_score']}/100 ({top_alert['threat_tier']})")
        user_meta = container.users.get(uid)
        dossier = orchestrator.investigate(top_alert, container, user_meta)
        investigation_dossiers.append(dossier)

        # Print Agent Deliberation Summary
        for step in dossier["agent_transcript"]:
            print(f"          • [{step['agent']}]: {step['thought'][:90]}...")
        print(f"          • [Containment Action]: {len(dossier['containment_summary'])} automated zero-trust actions enforced.")

    # -------------------------------------------------------------
    # Step 7: Ground-Truth Verification & Detection Metrics
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("  VERIFICATION & DETECTION PERFORMANCE AGAINST GROUND-TRUTH SCENARIOS")
    print("=" * 80)

    detected_targets = set(user_top_incidents.keys())
    ground_truth_targets = set(ground_truth.keys())
    true_positives = detected_targets.intersection(ground_truth_targets)
    false_positives = detected_targets - ground_truth_targets
    false_negatives = ground_truth_targets - detected_targets

    recall = (len(true_positives) / len(ground_truth_targets)) * 100
    precision = (len(true_positives) / max(1, len(detected_targets))) * 100

    print(f"  Target Scenarios Injected: {len(ground_truth_targets)}")
    print(f"  Target Scenarios Detected: {len(true_positives)} / {len(ground_truth_targets)} ({recall:.1f}% Recall)")
    print(f"  Precision: {precision:.1f}% | False Positives: {len(false_positives)}")

    for uid, info in ground_truth.items():
        status = "DETECTED [CONFIRMED]" if uid in true_positives else "MISSED"
        top_score = user_top_incidents[uid]["hybrid_score"] if uid in user_top_incidents else 0.0
        print(f"    - {uid} ({info['threat_actor']}): {info['name']} -> {status} (Max Score: {top_score}/100)")

    # -------------------------------------------------------------
    # Step 8: Export Full Analysis JSON for Interactive Dashboard
    # -------------------------------------------------------------
    dashboard_payload = {
        "metadata": {
            "title": "Meridian Bank Cyber SOC - Insider Threat Intelligence",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_users": len(container.users),
            "total_events": sum(summary.values()),
            "days_monitored": days,
            "deep_learning_backend": "PyTorch Bi-LSTM" if HAS_TORCH else "Vectorized NumPy Deep Autoencoder",
            "detection_recall": round(recall, 1),
            "detection_precision": round(precision, 1),
            "ground_truth_scenarios": ground_truth
        },
        "critical_incidents": list(user_top_incidents.values()),
        "investigations": investigation_dossiers,
        "all_daily_scores": [
            {
                "user_id": r["user_id"],
                "name": r["employee_name"],
                "date": r["date"],
                "department": r["department"],
                "hybrid_score": r["hybrid_score"],
                "ueba_score": r["ueba_score"],
                "dl_score": r["dl_score"],
                "dl_reconstruction_error": r["dl_reconstruction_error"],
                "threat_tier": r["threat_tier"]
            }
            for r in hybrid_results if r["threat_tier"] != "BENIGN" or int(r["date"].split("-")[2]) >= 20
        ]
    }

    json_path = os.path.join(output_dir, "threat_intelligence.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_payload, f, indent=2)
    print(f"\n[+] Saved full threat intelligence payload to: {json_path}")

    return dashboard_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Financial Insider Threat Detection Pipeline")
    parser.add_argument("--days", type=int, default=30, help="Number of simulation days (default: 30)")
    parser.add_argument("--output-dir", type=str, default="./output", help="Directory to save output logs & reports")
    args = parser.parse_args()

    run_pipeline(days=args.days, output_dir=args.output_dir)
