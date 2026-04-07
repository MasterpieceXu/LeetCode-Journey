import requests
import os
import time
import subprocess
import sys

# 强制实时输出日志
def log(msg):
    print(msg, flush=True)

# 密钥配置
SESSION = os.getenv('LEETCODE_SESSION', '').strip()
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN', '').strip()
OUTPUT_DIR = "solutions"
GRAPHQL_URL = "https://leetcode.cn/graphql/"

# 采用刚才测试成功的标准 Headers
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};",
    "X-CSRFToken": CSRF_TOKEN,
    "Origin": "https://leetcode.cn",
    "Referer": "https://leetcode.cn/progress/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def get_all_accepted_submissions():
    """获取所有已通过的提交记录（包含历史记录）"""
    submissions = []
    offset, limit = 0, 20
    log("🚀 正在检索历史提交记录...")
    
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
        if resp.status_code != 200:
            log(f"❌ 翻页抓取失败: {resp.status_code}")
            break
            
        data = resp.json().get('data', {}).get('submissionList', {})
        new_subs = data.get('submissions', [])
        
        for s in new_subs:
            if s['statusDisplay'] == 'Accepted':
                submissions.append(s)
        
        if not data.get('hasNext') or offset > 2000: # 100道题完全没问题
            break
        offset += limit
        log(f"已检索 {offset} 条记录...")
        time.sleep(0.5)
    
    return submissions

def get_submission_code(submission_id):
    """抓取单道题的源代码"""
    payload = {
        "query": "query s($id: ID!) { submissionDetail(submissionId: $id) { code } }",
        "variables": {"id": submission_id}
    }
    resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get('data', {}).get('submissionDetail', {}).get('code')
    return None

def main():
    if not SESSION or not CSRF_TOKEN:
        log("❌ 缺失 Secrets，请检查配置。")
        sys.exit(1)

    all_subs = get_all_accepted_submissions()
    log(f"✅ 检索完成！共找到 {len(all_subs)} 条通过记录。")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 按时间从远到近排序（重要：为了绿墙的生成顺序）
    all_subs.sort(key=lambda x: int(x['timestamp']))

    # 配置 Git 用户（Action 运行时需要）
    subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])

    seen_problems = set()
    for s in all_subs:
        if s['titleSlug'] in seen_problems:
            continue
        
        ext = "py" if "python" in s['lang'].lower() else "cpp" if "cpp" in s['lang'].lower() else "java"
        filename = f"{s['titleSlug']}.{ext}"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # 抓取代码
        log(f"📦 正在同步题目: {s['title']}")
        code = get_submission_code(s['id'])
        
        if code:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            
            # --- 关键：回溯时间点提交 ---
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s['timestamp'])))
            subprocess.run(['git', 'add', filepath])
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"], env["GIT_COMMITTER_DATE"] = dt, dt
            subprocess.run(['git', 'commit', '-m', f"Sync: {s['title']} (Submitted on {dt})"], env=env)
            
            seen_problems.add(s['titleSlug'])
            time.sleep(1) # 频率控制，防止被封

    log("🏁 本地同步及 Commit 已完成，准备推送至 GitHub 主页！")

if __name__ == "__main__":
    main()
