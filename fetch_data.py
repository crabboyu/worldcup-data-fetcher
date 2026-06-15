name: Fetch World Cup Data

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  fetch-data:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0          # 获取完整历史，便于 rebase
          ref: main               # 明确拉取 main 分支

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install sports-skills

      - name: Run data fetch script
        run: python fetch_data.py

      - name: Commit and push if changed
        run: |
          # 配置 Git 用户（使用你的真实用户名和邮箱）
          git config user.name "crabboyu"
          git config user.email "crabboyu@users.noreply.github.com"
          
          # 先拉取远程最新更改（使用 rebase 避免合并提交）
          git pull --rebase origin main
          
          # 如果有新的变更则提交
          git add data.json
          if ! git diff --cached --quiet; then
            git commit -m "Auto-update data"
            git push origin main
          else
            echo "No changes to commit"
          fi
