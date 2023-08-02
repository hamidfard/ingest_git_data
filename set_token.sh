#!/bin/sh

#This is a shell script file to set secret scope by Databricks CLI for storing and managing secrets securely.

#Replace <scope-name> with the name of a Databricks secret scope to store the token.
#Replace <token-key> with the name of a key to assign to the token.
#Replace <token> with the value of the GitHub personal access token.

databricks secrets create-scope --scope <scope-name>
databricks secrets put --scope <scope-name> --key <token-key> --string-value <token>