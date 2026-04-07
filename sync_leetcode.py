import requests
import os
import time
import subprocess

# 配置（记得在 GitHub Secrets 里只填乱码，不带冒号！）
SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')
OUTPUT_DIR = "solutions"
GRAPHQL_URL = "https://leetcode.cn/graphql/"

HEADERS = {
    "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN}",
    "X-CSRFToken": CSRF_TOKEN,
    "Referer": "https://leetcode.cn/progress/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def get_all_accepted_submissions():
    submissions = []
    offset, limit = 0, 20
    while True:
        payload = {
            "query": """
            query submissions($offset: Int, $limit: Int) {
                submissionList(offset: $offset, limit: $limit) {
                    submissions { id title titleSlug statusDisplay lang timestamp }
                    hasNext
                }
            }
            """,
            "variables": {"offset": offset, "limit": limit}
        }
        resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
        if resp.status_code != 200: break
        data = resp.json().get('data', {}).get('submissionList', {})
        for s in data.get('submissions', []):
            if s['statusDisplay'] == 'Accepted': submissions.append(s)
        if not data.get('hasNext') or offset > 1000: break # 限制翻页深度
        offset += limit
        time.sleep(0.5)
    return submissions

def get_submission_code(submission_id):
    payload = {
        "query": "query s($id: ID!) { submissionDetail(submissionId: $id) { code } }",
        "variables": {"id": submission_id}
    }
    resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    return resp.json().get('data', {}).get('submissionDetail', {}).get('code') if resp.status_code == 200 else None

def git_commit_with_date(filepath, submission_time, title):
    """关键逻辑：强行指定 Git 提交时间"""
    # 将力扣的时间戳转为 Git 需要的格式
    formatted_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(submission_time)))
    
    # 执行 Git 命令
    subprocess.run(['git', 'add', filepath])
    # 通过环境变量修改作者和提交时间
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = formatted_date
    env["GIT_COMMITTER_DATE"] = formatted_date
    
    subprocess.run(['git', 'commit', '-m', f"Sync LeetCode: {title}"], env=env)

if __name__ == "__main__":
    if not SESSION or not CSRF_TOKEN:
        print("Error: Missing credentials in Secrets")
        exit(1)
    
    subs = get_all_accepted_submissions()
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    # 配置 Git 用户信息（Action 运行时需要）
    subprocess.run(['git', 'config', '--global', 'user.name', 'GitHub Action'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])

    seen_problems = set()
