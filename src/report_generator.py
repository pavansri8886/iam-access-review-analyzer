from collections import Counter

def generate_report(entitlements, findings):
    total_users = entitlements["user_id"].nunique()
    total_apps = entitlements["application_id"].nunique()
    total_assignments = len(entitlements)
    total_findings = len(findings)

    severity_counts = findings["severity"].value_counts().to_dict()
    high = severity_counts.get("HIGH", 0)
    medium = severity_counts.get("MEDIUM", 0)
    low = severity_counts.get("LOW", 0)

    gap_counts = Counter(findings["gap_type"])
    gap_rows = ""
    for gap, count in gap_counts.items():
        gap_rows += f"""
        <tr>
            <td>{gap.replace("_", " ")}</td>
            <td>{count}</td>
        </tr>
        """

    finding_rows = ""
    for _, row in findings.iterrows():
        sev = row["severity"]
        if sev == "HIGH":
            badge_class = "badge-high"
        elif sev == "MEDIUM":
            badge_class = "badge-medium"
        else:
            badge_class = "badge-low"

        finding_rows += f"""
        <tr>
            <td>{row['gap_type'].replace("_", " ")}</td>
            <td>{row['user']}</td>
            <td>{row['application']}</td>
            <td>{row['role']}</td>
            <td><span class="badge {badge_class}">{sev}</span></td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>IAM Access Governance Dashboard</title>
        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                color: #1f2937;
            }}

            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 32px;
            }}

            .header {{
                background: linear-gradient(135deg, #003087, #0b4db3);
                color: white;
                padding: 28px 32px;
                border-radius: 16px;
                margin-bottom: 28px;
                box-shadow: 0 8px 24px rgba(0, 48, 135, 0.18);
            }}

            .header h1 {{
                margin: 0 0 8px 0;
                font-size: 40px;
                font-weight: 700;
            }}

            .header p {{
                margin: 0;
                opacity: 0.92;
                font-size: 16px;
            }}

            .section-title {{
                font-size: 26px;
                font-weight: 700;
                margin: 0 0 18px 0;
                color: #0f172a;
            }}

            .cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 18px;
                margin-bottom: 30px;
            }}

            .card {{
                background: white;
                border-radius: 14px;
                padding: 20px 22px;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
                border: 1px solid #e5e7eb;
            }}

            .card .label {{
                font-size: 13px;
                color: #6b7280;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }}

            .card .value {{
                font-size: 30px;
                font-weight: 700;
                color: #111827;
            }}

            .card.high .value {{
                color: #b91c1c;
            }}

            .card.medium .value {{
                color: #b45309;
            }}

            .card.low .value {{
                color: #047857;
            }}

            .grid {{
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 24px;
                align-items: start;
                margin-bottom: 28px;
            }}

            .panel {{
                background: white;
                border-radius: 16px;
                padding: 22px;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
                border: 1px solid #e5e7eb;
            }}

            .panel h2 {{
                margin: 0 0 16px 0;
                font-size: 22px;
                color: #111827;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th {{
                text-align: left;
                background: #0f3d91;
                color: white;
                padding: 14px 16px;
                font-size: 14px;
                position: sticky;
                top: 0;
            }}

            td {{
                padding: 13px 16px;
                border-bottom: 1px solid #e5e7eb;
                font-size: 14px;
                vertical-align: top;
            }}

            tr:hover td {{
                background: #f8fafc;
            }}

            .table-wrapper {{
                max-height: 520px;
                overflow-y: auto;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }}

            .badge {{
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 700;
                color: white;
            }}

            .badge-high {{
                background: #dc2626;
            }}

            .badge-medium {{
                background: #f59e0b;
            }}

            .badge-low {{
                background: #10b981;
            }}

            .maintenance {{
                background: white;
                border-radius: 16px;
                padding: 22px;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
                border: 1px solid #e5e7eb;
            }}

            .maintenance h2 {{
                margin-top: 0;
                font-size: 22px;
            }}

            .maintenance-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 16px;
            }}

            .maintenance-box {{
                background: #f8fafc;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 16px;
            }}

            .maintenance-box h3 {{
                margin: 0 0 10px 0;
                font-size: 16px;
                color: #0f3d91;
            }}

            .maintenance-box ul {{
                margin: 0;
                padding-left: 18px;
                line-height: 1.7;
            }}

            @media (max-width: 980px) {{
                .grid {{
                    grid-template-columns: 1fr;
                }}

                .maintenance-grid {{
                    grid-template-columns: 1fr;
                }}

                .header h1 {{
                    font-size: 30px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">

            <div class="header">
                <h1>IAM Access Governance Dashboard</h1>
                <p>Simulated enterprise identity governance view for access review, entitlement risk, and certification oversight.</p>
            </div>

            <h2 class="section-title">IAM Governance Overview</h2>
            <div class="cards">
                <div class="card">
                    <div class="label">Total Users</div>
                    <div class="value">{total_users}</div>
                </div>
                <div class="card">
                    <div class="label">Applications</div>
                    <div class="value">{total_apps}</div>
                </div>
                <div class="card">
                    <div class="label">Role Assignments</div>
                    <div class="value">{total_assignments}</div>
                </div>
                <div class="card">
                    <div class="label">Governance Findings</div>
                    <div class="value">{total_findings}</div>
                </div>
                <div class="card high">
                    <div class="label">High Risk</div>
                    <div class="value">{high}</div>
                </div>
                <div class="card medium">
                    <div class="label">Medium Risk</div>
                    <div class="value">{medium}</div>
                </div>
                <div class="card low">
                    <div class="label">Low Risk</div>
                    <div class="value">{low}</div>
                </div>
            </div>

            <div class="grid">
                <div class="panel">
                    <h2>Governance Findings</h2>
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Gap Type</th>
                                    <th>User</th>
                                    <th>Application</th>
                                    <th>Role</th>
                                    <th>Severity</th>
                                </tr>
                            </thead>
                            <tbody>
                                {finding_rows}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="panel">
                    <h2>Findings by Gap Type</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Gap Type</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            {gap_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="maintenance">
                <h2>Data Maintenance Model</h2>
                <div class="maintenance-grid">
                    <div class="maintenance-box">
                        <h3>Automatic Maintenance</h3>
                        <ul>
                            <li>Identity provider feeds for active accounts and login activity</li>
                            <li>HR data sync for employee status and contractor expiry</li>
                            <li>IAM platform exports for role assignments and privilege levels</li>
                            <li>Scheduled ingestion of review records from certification tools</li>
                        </ul>
                    </div>
                    <div class="maintenance-box">
                        <h3>Manual Maintenance</h3>
                        <ul>
                            <li>Quarterly access certification by managers and application owners</li>
                            <li>Validation of toxic role exceptions and business justifications</li>
                            <li>Review of privileged roles requiring enhanced governance</li>
                            <li>Remediation tracking for unresolved governance findings</li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>
    </body>
    </html>
    """

    with open("output/access_governance_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)