def generate_report(entitlements, findings):

    total_users = entitlements['user_id'].nunique()
    total_apps = entitlements['application_id'].nunique()
    total_assignments = len(entitlements)

    high = len(findings[findings['severity'] == "HIGH"])
    medium = len(findings[findings['severity'] == "MEDIUM"])
    low = len(findings[findings['severity'] == "LOW"])

    rows = ""

    for _, r in findings.iterrows():

        color = "#e74c3c" if r["severity"] == "HIGH" else "#f39c12"

        rows += f"""
        <tr>
        <td>{r['gap_type']}</td>
        <td>{r['user']}</td>
        <td>{r['application']}</td>
        <td>{r['role']}</td>
        <td><span style='color:white;background:{color};padding:4px 8px;border-radius:6px'>
        {r['severity']}
        </span></td>
        </tr>
        """

    html = f"""
    <html>
    <head>
    <title>IAM Governance Dashboard</title>

    <style>

    body {{
        font-family: Arial;
        background:#f4f6fa;
        margin:40px;
    }}

    h1 {{
        color:#003087;
    }}

    .cards {{
        display:flex;
        gap:20px;
        margin-bottom:30px;
    }}

    .card {{
        background:white;
        padding:20px;
        border-radius:10px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.1);
        width:200px;
    }}

    table {{
        border-collapse: collapse;
        width:100%;
        background:white;
    }}

    th {{
        background:#003087;
        color:white;
        padding:12px;
        text-align:left;
    }}

    td {{
        padding:10px;
        border-bottom:1px solid #ddd;
    }}

    tr:hover {{
        background:#f1f3f8;
    }}

    </style>

    </head>

    <body>

    <h1>IAM Access Governance Dashboard</h1>

    <div class="cards">

        <div class="card">
        <b>Total Users</b>
        <h2>{total_users}</h2>
        </div>

        <div class="card">
        <b>Applications</b>
        <h2>{total_apps}</h2>
        </div>

        <div class="card">
        <b>Assignments</b>
        <h2>{total_assignments}</h2>
        </div>

        <div class="card">
        <b>High Risk</b>
        <h2 style="color:#e74c3c">{high}</h2>
        </div>

        <div class="card">
        <b>Medium Risk</b>
        <h2 style="color:#f39c12">{medium}</h2>
        </div>

    </div>

    <h2>Governance Findings</h2>

    <table>

    <tr>
        <th>Gap Type</th>
        <th>User</th>
        <th>Application</th>
        <th>Role</th>
        <th>Severity</th>
    </tr>

    {rows}

    </table>

    <br><br>

    <h3>Data Maintenance Model</h3>

    <p>
    Automatic updates would typically come from identity providers,
    HR systems and IAM platforms. Manual review occurs during
    periodic access certification campaigns.
    </p>

    </body>
    </html>
    """

    with open("output/access_governance_dashboard.html","w") as f:
        f.write(html)