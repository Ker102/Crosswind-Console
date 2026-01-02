# Jobs Tool Guidance

Use this document to determine which tool to use for job-related queries.

## Job Search Tools

| User Query Pattern | Tool to Use | Key Parameters |
|-------------------|-------------|----------------|
| "Find jobs in X" | `search_jobs` | query, location |
| "Remote jobs for X" | `search_jobs` | query, remote=true |
| "Salary for X role" | `get_salary_info` | job_title, location |

## Intent Mapping

When the user says:
- **"remote"** → Set remote=true
- **"entry level"** → experience_level=entry
- **"senior"** → experience_level=senior
- **"full time"** → job_type=full_time
- **"contract"** → job_type=contract

## Placeholder

> **Note**: Add more job search API parameter guidance here as you integrate job-related MCP tools.
