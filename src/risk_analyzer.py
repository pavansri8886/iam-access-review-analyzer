import pandas as pd
from datetime import datetime, timedelta

def analyze_risks(df):
    findings = []
    today = datetime.today()
    stale_threshold = today - timedelta(days=180)

    for _, row in df.iterrows():
        if row['status'] == "TERMINATED" and row['assignment_status'] == "ACTIVE":
            findings.append({
                "gap_type": "ORPHANED_ACCOUNT",
                "user": row['full_name'],
                "application": row['application_name'],
                "role": row['role_name'],
                "severity": "HIGH"
            })

        if row['last_login'] < today - timedelta(days=120):
            findings.append({
                "gap_type": "DORMANT_ACCOUNT",
                "user": row['full_name'],
                "application": row['application_name'],
                "role": row['role_name'],
                "severity": "MEDIUM"
            })

        if row['privilege_level'] == "PRIVILEGED":
            if pd.isna(row['review_date']) or row['review_date'] < stale_threshold:
                findings.append({
                    "gap_type": "PRIVILEGED_ACCESS_WITHOUT_REVIEW",
                    "user": row['full_name'],
                    "application": row['application_name'],
                    "role": row['role_name'],
                    "severity": "HIGH"
                })

        if row['review_status'] in ["NOT_REVIEWED"]:
            findings.append({
                "gap_type": "MISSING_REVIEW",
                "user": row['full_name'],
                "application": row['application_name'],
                "role": row['role_name'],
                "severity": "MEDIUM"
            })

    return pd.DataFrame(findings)
