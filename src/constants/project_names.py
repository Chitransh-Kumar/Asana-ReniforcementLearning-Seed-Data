# Project name templates conditioned on project type 
# to produce realistic, non-uniform naming patterns

PROJECT_NAME_TEMPLATES = {
    "Sprint": [
        "Sprint Q{q} – Week {w}",
        "Sprint {w}",
    ],
    "Bug Tracking": [
        "Bug Backlog",
        "Stability & Fixes"
    ],
    "Roadmap": [
        "Product Roadmap {year}",
        "Platform Roadmap"
    ],
    "Marketing Campaign": [
        "{quarter} Growth Campaign",
        "Launch Campaign – {product}"
    ],
    "Ops Initiative": [
        "Operational Improvements",
        "Process Optimization"
    ]
}
