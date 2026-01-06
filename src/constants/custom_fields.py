# Project-type–specific custom field templates to mirror 
# Asana’s per-project customization model

CUSTOM_FIELD_TEMPLATES = {
    "Sprint": [
        ("Priority", "enum", ["Low", "Medium", "High"]),
        ("Story Points", "number", None),
        ("Status", "enum", ["Todo", "In Progress", "Done"])
    ],
    "Bug Tracking": [
        ("Severity", "enum", ["Minor", "Major", "Critical"]),
        ("Status", "enum", ["Open", "Investigating", "Resolved"]),
    ],
    "Roadmap": [
        ("Confidence", "enum", ["Low", "Medium", "High"]),
        ("Notes", "text", None)
    ],
    "Marketing Campaign": [
        ("Channel", "enum", ["Email", "Paid", "Organic", "Social"]),
        ("Owner Notes", "text", None)
    ],
    "Ops Initiative": [
        ("Risk Level", "enum", ["Low", "Medium", "High"]),
        ("Effort", "number", None)
    ]
}
