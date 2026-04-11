# 🚀 LeetCode Journey Sync

> A fully automated pipeline for synchronizing LeetCode progress to GitHub, featuring incremental updates, time-travel commits, and robust rate-limit handling.
> 
> *[中文说明见下文 / Scroll down for Chinese version]*

## 🌟 Introduction

This repository serves as my personal algorithm knowledge base. Instead of manually copying and pasting solutions, I built this automated synchronization tool. It routinely pulls my `Accepted` submissions from LeetCode via its GraphQL API and commits them to this repository.

More than just a backup tool, this project is an exercise in **Automation**, **API Integration**, and **Idempotent Data Synchronization**. 

### Key Features
* **Automated Sync**: Runs daily via GitHub Actions (cron jobs) with zero manual intervention.
* **Time-Travel Commits**: Preserves the exact historical timestamp of the original LeetCode submission (`GIT_AUTHOR_DATE`), ensuring an accurate timeline of learning progress on the contribution graph.
* **Incremental Updates**: Uses local state tracking (`synced_ids.txt`) to avoid duplicate requests, skipping previously synced problems instantly.
* **Robust Error Handling**: Gracefully handles LeetCode's rate limiting (HTTP 429 / Empty Responses) through exponential backoff and resume capabilities.

---

## 🛠️ Technical Stack

* **Language**: Python 3
* **API**: LeetCode GraphQL API
* **CI/CD**: GitHub Actions
* **Version Control**: Git (Subprocess manipulation)

---

## 📂 Project Structure

```text
.
├── .github/workflows/
│   └── leetcode_sync.yml   # GitHub Actions automation pipeline
├── solutions/              # Auto-generated folder containing all accepted codes
├── synced_ids.txt          # Local state file for incremental sync tracking
├── sync_leetcode.py        # Core Python synchronization script
└── README.md               # You are here
```
# ⚙️ How It Works (For Developers)

**1. Retrieve Your LeetCode Cookies**
* Log into [LeetCode (CN)](https://leetcode.cn/).
* Open Developer Tools (`F12`) and navigate to the **Network** tab.
* Filter by `graphql` and inspect the Request Headers.
* Extract the following two values:
  * `LEETCODE_SESSION` (from the `Cookie` string)
  * `csrftoken` (from the `x-csrftoken` header)

**2. Configure GitHub Secrets**
Go to your repository settings -> **Secrets and variables** -> **Actions** and add:
* `LEETCODE_SESSION` (Required)
* `LEETCODE_CSRF_TOKEN` (Required)
* `LEETCODE_REGION` (Optional): Set to `US` for global leetcode.com. Defaults to `CN` (leetcode.cn) if omitted.

**3. Configure Email**
To ensure GitHub correctly attributes the commits to your account, update the `GIT_EMAIL` variable in `sync_leetcode.py` with your GitHub-associated email (or use your `no-reply` privacy email).

**4. Run the Pipeline**
* Once configured, the Action runs automatically every day at 16:00 UTC.
* You can also trigger it manually via the **Actions** tab -> **Run workflow**.

> ⚠️ **Important Precautions**
> 
> * **Region Note**: This script defaults to **LeetCode China (`leetcode.cn`)**. If you use the global version, set the `LEETCODE_REGION` secret to `US`.
> * **Rate Limiting**: If migrating a large amount of historical data (e.g., 100+ problems), LeetCode may temporarily rate-limit the requests. The script safely ignores these errors. Simply run the workflow a few more times; it will incrementally catch up.
# 🇨🇳 中文说明 (Chinese Version)

