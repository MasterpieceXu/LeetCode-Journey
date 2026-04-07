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
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def get_all_accepted_submissions():
    submissions = []
    offset, limit = 0, 20
    log("🚀 正在检索历史提交记录...")
    while True:
        payload = {"query": f"{{ submissionList(offset: {offset}, limit: {limit}) {{ submissions {{ id title statusDisplay lang timestamp }} hasNext }} }}"}
        resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS)
        if resp.status_code != 200: break
        data = resp.json().get('data', {}).get('submissionList', {})
        new_subs = data.get('submissions', [])
        if not new_subs: break
        for s in new_subs:
            if s['statusDisplay'] == 'Accepted': submissions.append(s)
        if not data.get('hasNext') or offset > 2000: break
        offset += limit
        log(f"已扫描 {offset} 条记录...")
        time.sleep(0.5)
    return submissions

def get_detail(sub_id):
    """【健壮版】获取详情，增加安全检查"""
    payload = {"query": f"{{ submissionDetail(submissionId: \"{sub_id}\") {{ code question {{ titleSlug }} }} }}"}
    try:
        resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS)
        if resp.status_code == 200:
            res_json = resp.json()
            # 关键防御：层层检查 data 是否存在
            data = res_json.get('data')
            if data and data.get('submissionDetail'):
                detail = data['submissionDetail']
                return detail.get('code'), detail.get('question', {}).get('titleSlug')
        log(f"⚠️ 无法获取提交详情 (ID: {sub_id})，可能是频率限制，跳过此题。")
    except Exception as e:
        log(f"❌ 详情请求异常: {e}")
    return None, None

def main():
    if not SESSION or not CSRF_TOKEN:
        log("❌ 缺失 Secrets"); sys.exit(1)
    
    all_subs = get_all_accepted_submissions()
    log(f"✅ 共找到 {len(all_subs)} 条记录。")
    if not all_subs: return

    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    all_subs.sort(key=lambda x: int(x['timestamp']))
    
    subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])

    seen = set()
    for s in all_subs:
        if s['title'] in seen: continue
        log(f"📦 正在同步: {s['title']}")
        code, slug = get_detail(s['id'])
        
        # 核心逻辑：只有拿到了代码和名字才进行保存和提交
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
            time.sleep(1.5) # 稍微多等一会儿，对力扣温柔一点

    log("🏁 任务大功告成！")

if __name__ == "__main__":
    main()
