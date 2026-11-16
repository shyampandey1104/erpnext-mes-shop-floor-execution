# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "mes"
app_title = "Erpnext Mes Shop Floor Execution"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Mes Shop Floor Execution for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/mes/css/mes.bundle.css"
app_include_js = "/assets/mes/js/mes.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "mes.engine.on_document_submit",
        "on_cancel": "mes.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "mes.engine.daily_scheduled_sync"
    ]
}
