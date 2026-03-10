# 🔐 IAM Connection Governance Pipeline

> **Enterprise-scale Identity & Access Management governance simulation — 75 applications · 255 connections · 14 departments · 96 governance gaps detected · 69 critical items flagged**

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat&logo=pandas)
![YAML](https://img.shields.io/badge/YAML-Config%20Engine-orange?style=flat)
![HTML](https://img.shields.io/badge/HTML-Dashboard-red?style=flat)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat)

---

## 📌 What This Project Does

In large organisations, information about which applications connect to which IAM products is scattered across multiple systems — application inventories, IAM registries, connection logs, and manual spreadsheets. This data is incomplete, inconsistently structured, and not maintained to any defined standard.

The result is a governance gap: nobody has a clear, current picture of which applications have the right IAM coverage, which connections are stale or undocumented, and where the highest risk exposures are.

**This pipeline addresses that directly** — ingesting from three scattered data sources, consolidating into a unified risk-classified governance map, detecting violations, and producing structured outputs for audit systems and management stakeholders.

---

## 🏢 Enterprise Use Case

This project simulates the type of governance analysis required in large organisations where hundreds of applications integrate with multiple IAM products such as Azure AD, PAM, MFA, and IGA.

The goal is to create a reliable, maintainable connection map that allows security and risk teams to:

- Identify applications missing required IAM coverage
- Detect stale, undocumented, or unreviewed connections
- Understand risk exposure by application, department, and region
- Prioritise remediation with structured deadlines and ownership
- Support audit and compliance reporting with a full audit trail

At CMA CGM scale — 155,000 employees, 160 countries, 70+ critical applications — this type of governance map is not optional. It is the difference between a controlled access environment and one that fails an audit.

---

## 🏗️ Architecture

```
+-------------------------------------------------------------+
|                     DATA SOURCES (3)                        |
|                                                             |
|  application_inventory.csv   iam_product_registry.json      |
|  (75 apps, owners,           (5 IAM products, coverage      |
|   sensitivity, region)        requirements per sensitivity) |
|                                                             |
|              connection_log.csv                             |
|              (255 records, status, review dates)            |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
|                    pipeline.py                              |
|                                                             |
|  [1] Ingest      -- load from all 3 repositories            |
|  [2] Clean       -- standardise, fill gaps, flag stale      |
|  [3] Map         -- merge into unified connection model     |
|  [4] Classify    -- risk range + gap detection              |
|  [5] Expose      -- outputs + audit log                     |
+----------------------------+--------------------------------+
                             |
                             v
+-------------------------------------------------------------+
|                      OUTPUTS (6)                            |
|                                                             |
|  iam_connection_master_map.csv   --> GRC / audit systems    |
|  governance_gaps.csv             --> application owners     |
|  department_risk_scorecard.csv   --> IAM manager            |
|  remediation_priority_queue.csv  --> ServiceNow / owners    |
|  iam_governance_report.html      --> Control Tower / CISO   |
|  pipeline_run_log.txt            --> audit trail            |
+-------------------------------------------------------------+
```

---

## 📂 Project Structure

```
iam-connection-governance-pipeline/
|
+-- data/
|   +-- application_inventory.csv       # 75 enterprise applications
|   +-- iam_product_registry.json       # 5 IAM products + coverage requirements
|   +-- connection_log.csv              # 255 connection records
|
+-- src/
|   +-- risk_classifier.py              # Risk classification & gap detection
|   +-- report_generator.py             # HTML dashboard & CSV export
|   +-- scorecard.py                    # Department scorecard & remediation queue
|   +-- __init__.py
|
+-- output/                             # Regenerated on every pipeline run
|   +-- iam_connection_master_map.csv
|   +-- governance_gaps.csv
|   +-- department_risk_scorecard.csv
|   +-- remediation_priority_queue.csv
|   +-- iam_governance_report.html
|   +-- pipeline_run_log.txt
|
+-- feeding_rules.yaml                  # Authoritative sources, SLAs, conflict rules
+-- pipeline.py                         # Main entry point
+-- requirements.txt
+-- README.md
```

---

## 🗂️ Data Sources

| Source | Format | Records | Description |
|--------|--------|---------|-------------|
| `application_inventory.csv` | CSV | 75 apps | Owner, department, sensitivity, environment, region |
| `iam_product_registry.json` | JSON | 5 products | Azure AD, PAM, RBAC, MFA, IGA with requirements per sensitivity level |
| `connection_log.csv` | CSV | 255 records | Connections with realistic gaps — stale, undocumented, unknown reviewers |

**Departments:** Finance · HR · Operations · Logistics · Compliance · Legal · IT · Air Cargo · Sustainability · Executive · Strategy

**Regions:** Global · EMEA · APAC · Americas

---

## ⚙️ Pipeline Steps

### Step 1 — Ingest
Loads all three source files independently, simulating the real-world problem of scattered, inconsistent repositories with varying formats and missing fields.

### Step 2 — Clean & Standardise
- Fills missing application owners flagged as UNKNOWN
- Standardises sensitivity and connection status fields
- Parses and validates all date fields across sources
- Flags connections exceeding the 180-day review threshold as stale

### Step 3 — Build Unified Connection Map
Merges all three sources into a single structured data model with feeding rules governing which source is authoritative for each field.

| Field | Authoritative Source | Update Mode |
|-------|---------------------|-------------|
| App metadata | application_inventory | Manual |
| IAM product requirements | iam_product_registry | Scheduled — 180 days |
| Connection status | connection_log | Manual — post access review |
| Risk range | Pipeline (calculated) | Automatic — every run |

### Step 4 — Classify Risk & Detect Gaps

**Risk Classification:**

| Risk | Criteria |
|------|----------|
| HIGH | HIGH sensitivity + business critical + Production environment |
| MEDIUM | MEDIUM sensitivity OR stale review OR pending/undocumented status |
| LOW | LOW sensitivity, Development environment, non-critical |

**5 Gap Types Detected:**

| Gap Type | Description |
|----------|-------------|
| `MISSING_CONNECTION` | Required IAM product not connected for the app's sensitivity level |
| `STALE_REVIEW` | Connection not reviewed within the defined review cycle |
| `UNDOCUMENTED_CONNECTION` | Connection exists with no documented status |
| `UNKNOWN_OWNER` | Application has no registered owner |
| `MISSING_REVIEW_DATE` | Active connection with no review date on record |

### Step 5 — Expose & Maintain
Generates all 6 outputs, writes a timestamped audit log entry, and prints a run summary to the terminal.

---

## 🎯 Remediation SLAs

Defined in `feeding_rules.yaml` and applied automatically to every detected gap:

| Gap Type | HIGH | MEDIUM | LOW |
|----------|------|--------|-----|
| Missing Connection | 7 days | 30 days | 90 days |
| Stale Review | 3 days | 14 days | 30 days |
| Undocumented Connection | 24 hours | 7 days | 30 days |
| Unknown Owner | 48 hours | 7 days | 30 days |
| Missing Review Date | 3 days | 14 days | 30 days |

---

## 🔧 Feeding Rules Engine

`feeding_rules.yaml` is the governance configuration layer for the entire pipeline. It defines:

- **Authoritative source** per field — which system owns the data
- **Conflict resolution procedures** — reject, flag for review, use most recent, or escalate
- **Update modes** — automatic, manual, or scheduled with defined cycle
- **Remediation SLAs** — deadlines and responsible owner per gap type and risk level
- **Communication channels** — how each output reaches its intended audience

This separates governance rules from pipeline logic — rules can be updated without touching code.

---

## 🔄 Data Maintenance Model

### Automatic — every pipeline run
- Refreshes connection map from all source systems
- Recalculates risk classifications and detects new gaps
- Rebuilds department scorecard and remediation priority queue
- Regenerates all output files
- Appends timestamped entry to audit log

### Manual — defined process
- Application owners update connection_log.csv after each access review
- Data Protection Officer confirms sensitivity classifications quarterly
- IAM team updates iam_product_registry.json when products are added or retired
- Unknown owners resolved within 7 days of gap detection
- Feeding rules reviewed annually by IAM governance team

---

## 📊 Output Channels

| Output | Audience | Channel |
|--------|----------|---------|
| `iam_connection_master_map.csv` | GRC / audit systems | Automated integration |
| `governance_gaps.csv` | Application owners | Weekly email — Monday 08:00 |
| `department_risk_scorecard.csv` | IAM Manager | Internal reporting |
| `remediation_priority_queue.csv` | Owners + IAM team | ServiceNow tickets |
| `iam_governance_report.html` | Control Tower / CISO | Intranet SharePoint |
| `pipeline_run_log.txt` | Audit trail | Retained in output directory |

---

## 🚀 Setup & Run

```bash
# Clone the repository
git clone https://github.com/pavansri8886/iam-connection-governance-pipeline.git
cd iam-connection-governance-pipeline

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python pipeline.py
```

Open `output/iam_governance_report.html` in any browser to view the governance dashboard.

---

## 📈 Sample Run Output

```
============================================================
  IAM CONNECTION GOVERNANCE PIPELINE
  Run date: 2026-03-09
============================================================

[1/5] Loading data sources...
  ✓ Application inventory: 75 records loaded
  ✓ IAM product registry: 5 products loaded
  ✓ Connection log: 255 connection records loaded

[2/5] Cleaning and standardising data...
  ✓ Missing owners filled: 4 apps
  ✓ Undocumented connections flagged: 10
  ✓ Stale connections flagged: 44

[3/5] Building unified connection map...
  ✓ Unified map built: 255 connection records across 75 applications

[4/5] Classifying risk and detecting gaps...
  ✓ HIGH: 180  |  MEDIUM: 69  |  LOW: 6
  ✓ Governance gaps detected: 96

[5/5] Generating outputs and exposing data...
  ✓ Master map, gap report, scorecard, remediation queue, HTML dashboard
  ✓ 69 CRITICAL items requiring immediate action

============================================================
  PIPELINE COMPLETE -- 6 outputs written to ./output/
============================================================
```

---

## 👤 Author

**Pavan Kumar Naganaboina**
MSc Data Management & AI — ECE Paris

[![LinkedIn](https://img.shields.io/badge/LinkedIn-pavankumarn01-blue?style=flat&logo=linkedin)](https://linkedin.com/in/pavankumarn01)
[![GitHub](https://img.shields.io/badge/GitHub-pavansri8886-black?style=flat&logo=github)](https://github.com/pavansri8886)

---

> *Built to demonstrate enterprise IAM governance methodology — data consolidation from scattered sources, unified connection mapping, risk classification, gap detection, feeding rules design, and structured stakeholder reporting at scale.*
