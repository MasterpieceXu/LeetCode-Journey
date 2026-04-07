name: My Custom LeetCode Sync
on:
  workflow_dispatch:
  schedule:
    - cron: '0 16 * * *'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests

      - name: Run sync script
        env:
          LEETCODE_SESSION: ${{ secrets.LEETCODE_SESSION }}
          LEETCODE_CSRF_TOKEN: ${{ secrets.LEETCODE_CSRF_TOKEN }}
        run: python sync_leetcode.py

      - name: Commit and Push changes
        run: |
          git config --global user.name "MasterpieceXu"
          git config --global user.email "your-email@example.com"
          git add .
          # 如果没有文件变化，不执行 commit，防止报错
          git diff --quiet && git diff --staged --quiet || (git commit -m "Auto sync leetcode solutions" && git push)
