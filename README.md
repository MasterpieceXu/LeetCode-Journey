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

## 🌟 项目简介

本仓库是我的个人算法知识库。为了避免手动复制粘贴代码的繁琐，我开发了这个自动化同步工具。它会定期通过 LeetCode 的 GraphQL API 拉取我所有已通过 (`Accepted`) 的提交记录，并自动同步到这个仓库中。

这不仅是一个备份工具，更是我在**自动化运维**、**API 接口调用**以及**幂等性数据同步**方面的一次工程实践。

### 核心特性
* **全自动同步**：依托 GitHub Actions 定时任务（Cron），实现真正的无人值守。
* **时光穿梭提交**：通过底层修改 `GIT_AUTHOR_DATE`，精准保留每次提交在 LeetCode 上的原始时间戳，完美还原 GitHub 绿墙上的学习时间线。
* **智能增量更新**：引入本地状态文件 (`synced_ids.txt`) 记录已处理的 Submission ID，避免重复发包，实现秒级跳过。
* **强健的容错机制**：针对 LeetCode 的反爬虫与频率限制（Rate Limiting），内置了跳过与重试逻辑，支持断点续传。

---

## ⚙️ 开发者使用指南

如果你想复刻这个工具用于你自己的力扣账号，请按以下步骤操作：

**1. 获取 Cookie**
* 登录力扣中国站，按下 `F12` 打开开发者工具，切换到 **Network (网络)** 面板。
* 筛选 `graphql` 请求，查看 Request Headers (请求头)。
* 提取出 `LEETCODE_SESSION` 和 `csrftoken` 的值。

**2. 配置 Secrets**
进入 GitHub 仓库的 **Settings -> Secrets and variables -> Actions**，添加以下环境变量：
* `LEETCODE_SESSION` (必填)
* `LEETCODE_CSRF_TOKEN` (必填)
* `LEETCODE_REGION` (选填)：如果你使用海外全球站 (`leetcode.com`)，请设为 `US`。如果不填，默认抓取中国站数据。

**3. 设置身份邮箱**
在 `sync_leetcode.py` 中，将 `GIT_EMAIL` 变量修改为你绑定 GitHub 的真实邮箱或隐私邮箱，这是点亮主页绿墙的关键要素。

**4. 运行脚本**
* 配置完成后，你可以手动触发一次 Action 测试运行。
* 之后脚本会在每天的 UTC 时间 16:00 自动执行。

> ⚠️ **注意事项**
> 
> * **适用区域**：当前脚本的 API 接口默认指向**力扣中国区 (`leetcode.cn`)**。全球站用户请务必配置 `LEETCODE_REGION`。
> * **防爬虫限流**：如果你正处于“初次历史数据大迁移”阶段（例如一次性同步上百道题），极大概率会触发力扣的接口限流。脚本已内置容错机制，遇到限流会自动跳过。你只需在冷却后多次点击 `Run workflow`，脚本会根据 `synced_ids.txt` 进行断点续传，直到全部补齐。
