import requests
import os
import time
import subprocess
import sys

def log(msg):
    print(msg, flush=True)

SESSION = os.getenv('LEETCODE_SESSION', '').strip()
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN', '').strip()
OUTPUT_DIR = "solutions"

# 构造 Headers
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};",
    "X-CSRFToken": CSRF_TOKEN,
    "Origin": "https://leetcode.cn",
    "Referer": "https://leetcode.cn/progress/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def get_all_accepted_submissions():
    submissions = []
    offset, limit = 0, 20
    log("🚀 正在检索历史提交记录...")
    
    while True:
        # 核心改动：使用最简单的单行查询字符串，不使用 variables
        payload = {
            "query": f"{{ submissionList(offset: {offset}, limit: {limit}) {{ submissions {{ id title titleSlug statusDisplay lang timestamp }} hasNext }} }}"
        }
        
        resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS)
        
        if resp.status_code != 200:
            log(f"❌ 翻页抓取失败，状态码: {resp.status_code}")
            log(f"服务器反馈: {resp.text[:100]}")
            break
            
        data = resp.json().get('data', {}).get('submissionList', {})
        new_subs = data.get('submissions', [])
        
        if not new_subs:
            break
            
        for s in new_subs:
            if s['statusDisplay'] == 'Accepted':
                submissions.append(s)
        
        if not data.get('hasNext') or offset > 2000:
            break
            
        offset += limit
        log(f"已扫描到第 {offset} 条记录...")
        time.sleep(1)
    
    return submissions

def get_submission_code(sub_id):
    # 同样使用最简单的字符串格式
    payload = {
        "query": f"{{ submissionDetail(submissionId: \"{sub_id}\") {{ code }} }}"
    }
    resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get('data', {}).get('submissionDetail', {}).get('code')
    return None

def main():
    if not SESSION or not CSRF_TOKEN:
        log("❌ 缺失 Secrets，请检查配置。")
        sys.exit(1)

    all_subs = get_all_accepted_submissions()
    log(f"✅ 检索完成！共找到 {len(all_subs)} 条通过记录。")
    
    if not all_subs:
        log("⚠️ 未发现任何 Accepted 记录。")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    all_subs.sort(key=lambda x: int(x['timestamp']))

    subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])

    seen = set()
    for s in all_subs:
        if s['titleSlug'] in seen: continue
        
        ext = "py" if "python" in s['lang'].lower() else "cpp" if "cpp" in s['lang'].lower() else "java"
        filepath = os.path.join(OUTPUT_DIR, f"{s['titleSlug']}.{ext}")

        log(f"📦 正在同步: {s['title']}")
        code = get_submission_code(s['id'])
        
        if code:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s['timestamp'])))
            subprocess.run(['git', 'add', filepath])
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"], env["GIT_COMMITTER_DATE"] = dt, dt
            subprocess.run(['git', 'commit', '-m', f"Sync: {s['title']} ({dt})"], env=env)
            seen.add(s['titleSlug'])
            time.sleep(1)

    log("🏁 任务完成！")

if __name__ == "__main__":
    main()
