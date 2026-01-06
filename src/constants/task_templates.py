# Task title templates conditioned on project type 
# to produce realistic, domain-specific phrasing

TASK_TITLES = {
    "Sprint": [
        "Implement {component} changes",
        "Refactor {component} logic",
        "Add tests for {component}"
    ],
    "Bug Tracking": [
        "Fix {component} bug",
        "Investigate {component} issue",
        "Resolve crash in {component}"
    ],
    "Roadmap": [
        "Design {component} roadmap",
        "Align on {component} milestones"
    ],
    "Marketing Campaign": [
        "Prepare {component} content",
        "Launch {component} campaign"
    ],
    "Ops Initiative": [
        "Optimize {component} workflow",
        "Document {component} process"
    ]
}

COMPONENTS = [
    "auth flow",
    "API layer",
    "integration pipeline",
    "dashboard",
    "reporting module",
    "billing system"
]

TASK_DESCRIPTIONS = [
    None,  
    "This task needs to be completed as part of the current initiative.",
    "Coordinate with relevant stakeholders before completion.",
    "- Review requirements\n- Implement changes\n- Validate outcome"
]
