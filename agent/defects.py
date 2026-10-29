# agent/defects.py

# Each defect is a named CSS snippet injected into the page at runtime.
# The healthy source files (App.jsx, App.css) are never modified.
DEFECTS = {
    "horizontal_overflow": """
        .features {
            grid-template-columns: repeat(3, 300px) !important;
            width: max-content !important;
        }
    """,
}