- name: Commit and push if changed
  run: |
    git config user.name github-actions
    git config user.email github-actions@github.com
    git add data.json
    git diff --quiet && git diff --staged --quiet || git commit -m "Auto-update data"
    git pull --rebase origin main
    git push
