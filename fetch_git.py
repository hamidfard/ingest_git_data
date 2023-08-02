import json
import requests
import sys

api_url = "https://api.github.com"

def get_commits(owner, repo, token, path):
  page = 1
  request_url =  f"{api_url}/repos/{owner}/{repo}/commits"
  more = True

  get_response(request_url, f"{path}/commits", token)


def get_contributors(owner, repo, token, path):
  page = 1
  request_url =  f"{api_url}/repos/{owner}/{repo}/contributors"
  more = True

  get_response(request_url, f"{path}/contributors", token)


def get_response(request_url, path, token):
  page = 1
  more = True

  while more:
    response = requests.get(request_url, params={'page': page}, headers={'Authorization': "token " + token})
    if response.text != "[]":
      write(path + "/records-" + str(page) + ".json", response.text)
      page += 1
    else:
      more = False


def write(filename, contents):
  dbutils.fs.put(filename, contents)


def main():
  args = sys.argv[1:]
  if len(args) < 6:
    print("Usage: github-api.py owner repo request output-dir secret-scope secret-key")
    sys.exit(1)

  owner = sys.argv[1]
  repo = sys.argv[2]
  request = sys.argv[3]
  output_path = sys.argv[4]
  secret_scope = sys.argv[5]
  secret_key = sys.argv[6]

  token = dbutils.secrets.get(scope=secret_scope, key=secret_key)

  if (request == "commits"):
    get_commits(owner, repo, token, output_path)
  elif (request == "contributors"):
    get_contributors(owner, repo, token, output_path)


if __name__ == "__main__":
    main()