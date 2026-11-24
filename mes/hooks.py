# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "mes"
app_title = "Erpnext Mes Shop Floor Execution"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Mes Shop Floor Execution - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/mes/css/mes.bundle.css"
app_include_js = "/assets/mes/js/mes.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Mes Shop Floor Execution Entry": {
        "validate": "mes.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "mes.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "mes.tasks.hourly_sync"
    ],
    "daily": [
        "mes.tasks.daily_reconciliation"
    ],
    "weekly": [
        "mes.tasks.weekly_digest"
    ]
}
