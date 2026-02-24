# GitHub PR Review Stats

A simple Python script to determine how many pull request reviews each contributor has written in a repository. This tool helps teams ensure that reviews are **properly distributed** and no one is overloaded or overlooked. It generates a clear bar chart showing each reviewer’s contribution.

---

## Requirements

- Python 3.8+
- GNU make

---

## Features

- Counts reviews per contributor (including approvals, comments, and change requests)  
- Excludes bot accounts like GitHub Copilot automatically  
- Configurable repository via `config.json`  
- Uses a `.env` file to safely store your GitHub Personal Access Token (PAT)  
- Automatically installs dependencies when running via `make run`  
- Visualizes results with a clean, soft-purple bar chart  

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/github-review-stats.git
cd github-review-stats
```

### 2. Configure the Requirements

Copy the example configuration files.  
You will need to remove `.dist` and save them in the `config` folder.  

You can use the `cp` command from the terminal in the root folder (`/github-pull-review-stats`):
```bash
cp config/config.json.dist config/config.json
cp config/.env.dist config/.env
```

Then edit them with the appropriate information.

- `config/config.json`

```json
{
  "owner": "your-org-or-username",
  "repo": "your-repo-name"
}
```

- `config/.env`

```text
GITHUB_TOKEN=ghp_yourPersonalAccessTokenHere
```

> Note: The GitHub token should have read access to pull requests.
> For public repositories, a token is optional, but recommended to avoid hitting rate limits.
> If no token is provided, the script will raise a RunTimeError.

### 3. Run the Script

All the setup is handled by the `Makefile`, hence you only need to execute the command below from the root folder:

```bash
make run
```

> Linux users might need to run it in a virtual environment

This will:

1. Install Python dependencies (if not already installed)
2. Execute the script
3. Show a bar chart with the number of reviews completed per contributor
