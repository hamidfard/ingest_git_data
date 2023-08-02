# Databricks Workflow to ingest metrics for GitHub contributions

This repository includes the following files:

**set_token.sh**: Stores the GitHub token in a secret. This must be run in Databricks CLI.

**fetch_git.py**: Fetches GitHub data using the GitHub REST APIs. This must be run locally.

**define_dlt.py**: Create a Delta Live Tables pipeline to process the GitHub data. This should be wrapped using a DLT pipeline and a workflow job in Databricks. To define the workflow, in the Target field, enter a target database, for example, github_tables. In the configuration of workflow add the following key and values:
- `commits-path = <the DBFS path where the GitHub records will be written>`
- `contribs-path = <the DBFS path where the GitHub records will be written>`
