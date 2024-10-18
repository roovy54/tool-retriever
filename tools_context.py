tool_descriptions_context = """
Tool Descriptions and Arguments:

1. works_list
   Description: Returns a list of work items matching the request
   Arguments:
   - applies_to_part (array of strings):
     Description: Filters for work belonging to any of the provided parts
     Example: ["FEAT-123", "ENH-123", "PROD-123", "CAPL-123"]
   - created_by (array of strings):
     Description: Filters for work created by any of these users
     Example: ["DEVU-123"]
   - issue.priority (array of strings):
     Description: Filters for issues with any of the provided priorities
     Allowed values: p0, p1, p2, p3
   - issue.rev_orgs (array of strings):
     Description: Filters for issues with any of the provided Rev organizations
     Example: ["REV-123"]
   - limit (integer):
     Description: The maximum number of works to return (default: 50)
   - owned_by (array of strings):
     Description: Filters for work owned by any of these users
     Example: ["DEVU-123"]
   - stage.name (array of strings):
     Description: Filters for records in the provided stage(s) by name
   - ticket.needs_response (boolean):
     Description: Filters for tickets that need a response
   - ticket.rev_org (array of strings):
     Description: Filters for tickets associated with any of the provided Rev organizations
     Example: ["REV-123"]
   - ticket.severity (array of strings):
     Description: Filters for tickets with any of the provided severities
     Allowed values: blocker, high, low, medium
   - ticket.source_channel (array of strings):
     Description: Filters for tickets with any of the provided source channels
   - type (array of strings):
     Description: Filters for work of the provided types
     Allowed values: issue, ticket, task

2. summarize_objects
   Description: Summarizes a list of objects (internal implementation detail)
   Arguments:
   - objects (array of objects):
     Description: List of objects to summarize

3. prioritize_objects
   Description: Returns a list of objects sorted by priority (internal implementation detail)
   Arguments:
   - objects (array of objects):
     Description: A list of objects to be prioritized

4. add_work_items_to_sprint
   Description: Adds the given work items to the sprint
   Arguments:
   - work_ids (array of strings):
     Description: A list of work item IDs to be added to the sprint
   - sprint_id (string):
     Description: The ID of the sprint to which the work items should be added

5. get_sprint_id
   Description: Returns the ID of the current sprint

6. get_similar_work_items
   Description: Returns a list of work items that are similar to the given work item
   Arguments:
   - work_id (string):
     Description: The ID of the work item for which you want to find similar items

7. search_object_by_name
   Description: Given a search string, returns the id of a matching object in the system of record
   Arguments:
   - query (string):
     Description: The search string (e.g., customer's name, part name, user name)

8. create_actionable_tasks_from_text
   Description: Given a text, extracts actionable insights and creates tasks for them
   Arguments:
   - text (string):
     Description: The text from which the actionable insights need to be created

9. who_am_i
   Description: Returns the string ID of the current user
"""
