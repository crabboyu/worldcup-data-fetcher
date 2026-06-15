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
          git config user.name "crabboyu"
          git config user.email "crabboyu@users.noreply.github.com"
          # 先拉取远程最新更改（避免冲突）
          git pull --rebase origin main
          # 添加数据文件
          git add data.json
          # 如果有变更则提交并推送
          if ! git diff --cached --quiet; then
            git commit -m "Auto-update data"
            git push origin main
          else
            echo "No changes to commit"
          fi
