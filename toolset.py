tools = [
    {
        "tool_name": "who_am_i",
        "tool_description": "Returns the id of the current user",
        "args": [],
        "output": {"arg_type": "str", "is_array": False, "is_required": True},
    },
    {
        "tool_name": "get_sprint_id",
        "tool_description": "Returns the ID\nof the current\nsprint",
        "args": [],
        "output": {"arg_type": "str", "is_array": False, "is_required": True},
    },
    {
        "tool_name": "works_list",
        "tool_description": "Returns a list of work items matching the request",
        "args": [
            {
                "arg_name": "applies_to_part",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for work belonging to any of the provided parts",
                "example": ["FEAT-123", "ENH-123", "PROD-123", "CAPL-123"],
            },
            {
                "arg_name": "created_by",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for work created by any of these users",
                "example": ["DEVU-123"],
            },
            {
                "arg_name": "issue_priority",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for issues with any of the provided priorities. Allowed values: p0, p1, p2, p3",
            },
            {
                "arg_name": "issue.rev_orgs",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for issues with any of the provided Rev organizations, using their ID",
                "example": ["REV-123"],
            },
            {
                "arg_name": "limit",
                "arg_type": "int",
                "is_array": False,
                "is_required": False,
                "arg_description": "The maximum number of works to return. The default is '50'",
            },
            {
                "arg_name": "owned_by",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for work owned by any of these users",
                "example": ["DEVU-123"],
            },
            {
                "arg_name": "stage_name",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for records in the provided stage(s) by name",
            },
            {
                "arg_name": "ticket_need_response",
                "arg_type": "boolean",
                "is_array": False,
                "is_required": False,
                "arg_description": "Filters for tickets that need a response",
            },
            {
                "arg_name": "ticket_rev_org",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for tickets associated with any of the provided Rev organizations (customers)",
                "example": ["REV-123"],
            },
            {
                "arg_name": "ticket_severity",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for tickets with any of the provided severities. Allowed values: blocker, high, low, medium",
            },
            {
                "arg_name": "ticket_source_channel",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for tickets with any of the provided source channels",
            },
            {
                "arg_name": "type",
                "arg_type": "str",
                "is_array": True,
                "is_required": False,
                "arg_description": "Filters for work of the provided types. Allowed values: issue, ticket, task. Must be used, if arguments referencing tickets, issues or tasks are being used.",
            },
        ],
        "output": {"arg_type": "any", "is_array": False, "is_required": True},
    },
    {
        "tool_name": "summarize_objects",
        "tool_description": "Summarizes a list of objects. The logic of how to summarize a particular object type is an internal implementation detail.",
        "args": [
            {
                "arg_name": "objects",
                "arg_type": "any",
                "is_array": True,
                "is_required": True,
                "arg_description": "List of objects to summarize",
            }
        ],
        "output": {"arg_type": "any", "is_array": False, "is_required": True},
    },
    {
        "tool_name": "prioritize_objects",
        "tool_description": "Returns a list of objects sorted by priority. The logic of what constitutes priority for a given object is an internal implementation detail",
        "args": [
            {
                "arg_name": "objects",
                "arg_type": "any",
                "is_array": False,
                "is_required": False,
                "arg_description": "A list of objects to be prioritized",
            }
        ],
        "output": {"arg_type": "any", "is_array": True, "is_required": True},
    },
    {
        "tool_name": "add_work_items_to_sprint",
        "tool_description": "Adds the given work items to the sprint",
        "args": [
            {
                "arg_name": "work_ids",
                "arg_type": "str",
                "is_array": True,
                "is_required": True,
                "arg_description": " A list of work item IDs to be added to the sprint.",
            },
            {
                "arg_name": "sprint_id",
                "arg_type": "str",
                "is_array": False,
                "is_required": True,
                "arg_description": "The ID of the sprint to which the work items should be added",
            },
        ],
        "output": {"arg_type": "boolean", "is_array": False, "is_required": True},
    },
    {
        "tool_name": "get_similar_work_items",
        "tool_description": "Returns a list of work items that are similar to the given work item",
        "args": [
            {
                "arg_name": "work_id",
                "arg_type": "str",
                "is_array": False,
                "is_required": True,
                "arg_description": " The ID of the work item for which you want to find similar items",
            }
        ],
        "output": {"arg_type": "str", "is_array": True, "is_required": True},
    },
    {
        "tool_name": "search_object_by_name",
        "tool_description": "Given a search string, returns the id of a matching object in the system of record. If multiple matches are found, it returns the one where the confidence is highest",
        "args": [
            {
                "arg_name": "query",
                "arg_type": "str",
                "is_array": False,
                "is_required": True,
                "arg_description": "The search string, could be for example customer (rev) name, part name, user name. Work items are not counted as objects",
            }
        ],
        "output": {"arg_type": "any", "is_array": False, "is_required": True},
    },
    {
        "tool_name": "create_actionable_tasks_from_text",
        "tool_description": "Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item.",
        "args": [
            {
                "arg_name": "text",
                "arg_type": "str",
                "is_array": False,
                "is_required": True,
                "arg_description": "The text from which the actionable insights need to be created.",
            }
        ],
        "output": {"arg_type": "str", "is_array": True, "is_required": True},
    },
]
