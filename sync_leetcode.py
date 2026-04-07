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

HEADERS = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};",
    "X-CSRFToken": CSRF_TOKEN,
    "Origin": "https://leetcode.cn",
    "Referer": "https://leetcode.cn/progress/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def get_all_accepted_submissions():
    submissions = []
    offset, limit = 0, 20
    log("🚀 正在检索历史提交记录（修正版）...")
    
    while True:
        # 修正：去掉了导致报错的 titleSlug 字段
        payload = {
            "query": f"{{ submissionList(offset: {offset}, limit: {limit}) {{ submissions {{ id title statusDisplay lang timestamp }} hasNext }} }}"
        }
        
        resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS)
        if resp.status_code != 200:
            log(f"❌ 列表抓取失败: {resp.status_code}")
            break
            
        data = resp.json().get('data', {}).get('submissionList', {})
        new_subs = data.get('submissions', [])
        if not new_subs: break
            
        for s in new_subs:
            if s['statusDisplay'] == 'Accepted':
                submissions.append(s)
        
        if not data.get('hasNext') or offset > 2000: break
        offset += limit
        log(f"已扫描 {offset} 条记录...")
        time.sleep(0.5)
    
    return submissions

def get_detail(sub_id):
    """同时获取代码和题目英文名"""
    # 修正：在详情里拿 question 的 titleSlug
    payload = {
        "query": f"{{ submissionDetail(submissionId: \"{sub_id}\") {{ code question {{ titleSlug }} }} }}"
    }
    resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS)
    if resp.status_code == 200:
        detail = resp.json().get('data', {}).get('submissionDetail', {})
        return detail.get('code'), detail.get('question', {}).get('titleSlug')
    return None, None

def main():
    if not SESSION or not CSRF_TOKEN:
        log("❌ 缺失 Secrets"); sys.exit(1)

    all_subs = get_all_accepted_submissions()
    log(f"✅ 检索完成！共找到 {len(all_subs)} 条通过记录。")
    if not all_subs: return

    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    all_subs.sort(key=lambda x: int(x['timestamp']))
    subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])

    seen = set()
    for s in all_subs:
        # 使用题目显示名称去重，因为这一步还没拿到 slug
        if s['title'] in seen: continue
        
        log(f"📦 正在同步: {s['title']}")
        code, slug = get_detail(s['id'])
        
        if code and slug:
            ext = "py" if "python" in s['lang'].lower() else "cpp" if "cpp" in s['lang'].lower() else "java"
            filepath = os.path.join(OUTPUT_DIR, f"{slug}.{ext}")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s['timestamp'])))
            subprocess.run(['git', 'add', filepath])
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"], env["GIT_COMMITTER_DATE"] = dt, dt
            subprocess.run(['git', 'commit', '-m', f"Sync: {s['title']} ({dt})"], env=env)
            seen.add(s['title'])
            time.sleep(1.2) # 稍微慢一点，防止被 LeetCode 限流

    log("🏁 任务大功告成！")

if __name__ == "__main__":
    main()
