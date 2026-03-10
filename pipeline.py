import pandas as pd
from src.risk_analyzer import analyze_risks
from src.report_generator import generate_report

users = pd.read_csv("data/users.csv")
applications = pd.read_csv("data/applications.csv")
roles = pd.read_csv("data/roles.csv")
assignments = pd.read_csv("data/role_assignments.csv")
reviews = pd.read_csv("data/access_reviews.csv")

users['status'] = users['status'].fillna("ACTIVE")
reviews['reviewer'] = reviews['reviewer'].fillna("UNKNOWN")

assignments['last_login'] = pd.to_datetime(assignments['last_login'])
reviews['review_date'] = pd.to_datetime(reviews['review_date'], errors='coerce')

entitlements = assignments.merge(users, on="user_id")
entitlements = entitlements.merge(applications, on="application_id")
entitlements = entitlements.merge(roles, on=["role_id", "application_id"])
entitlements = entitlements.merge(reviews, on=["user_id", "application_id"], how="left")

findings = analyze_risks(entitlements)

findings.to_csv("output/access_review_findings.csv", index=False)
generate_report(entitlements, findings)

print("IAM Access Review Analysis Completed")
