import requests
import os
import time
import subprocess
import sys

def log(msg):
    print(msg, flush=True)

SESSION = os.getenv('LEETCODE_SESSION', '').strip()
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN', '').strip()
# github 认证的邮箱
GIT_EMAIL = 'kakayuankaka@gmail.com' 
OUTPUT_DIR = "solutions"
SYNC_LOG = "synced_ids.txt" # 增量同步

HEADERS = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};",
    "X-CSRFToken": CSRF_TOKEN,
    "Origin": "https://leetcode.cn",
    "Referer": "https://leetcode.cn/progress/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def get_synced_ids():
    """读取已经同步过的 ID 清单"""
    if os.path.exists(SYNC_LOG):
        with open(SYNC_LOG, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_synced_id(sub_id):
    """保存同步成功的 ID"""
    with open(SYNC_LOG, 'a') as f:
        f.write(f"{sub_id}\n")

def get_all_accepted_submissions():
    submissions = []
    offset, limit = 0, 20
    log("🚀 正在检索历史记录...")
    while True:
        payload = {"query": f"{{ submissionList(offset: {offset}, limit: {limit}) {{ submissions {{ id title statusDisplay lang timestamp }} hasNext }} }}"}
        try:
            resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS, timeout=10)
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
        except: break
    return submissions

def get_detail(sub_id):
    payload = {"query": f"{{ submissionDetail(submissionId: \"{sub_id}\") {{ code question {{ titleSlug }} }} }}"}
    try:
        resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get('data', {})
            if data and data.get('submissionDetail'):
                detail = data['submissionDetail']
                return detail.get('code'), detail.get('question', {}).get('titleSlug')
    except: pass
    return None, None

def main():
    if not SESSION or not CSRF_TOKEN:
        log("❌ 缺失 Secrets"); sys.exit(1)
    
    synced_ids = get_synced_ids()
    all_subs = get_all_accepted_submissions()
    log(f"✅ 共找到 {len(all_subs)} 条通过记录。")
    
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    # 按时间升序排序（保证最后留在文件夹里的是最新的代码）
    all_subs.sort(key=lambda x: int(x['timestamp']))
    
    subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
    subprocess.run(['git', 'config', '--global', 'user.email', GIT_EMAIL])

    count = 0
    for s in all_subs:
        sub_id = str(s['id'])
        
        # 如果这个提交 ID 已经在txt里，直接跳过
        if sub_id in synced_ids:
            continue
        
        log(f"📦 正在同步新记录: {s['title']} (ID: {sub_id})")
        code, slug = get_detail(sub_id)
        
        if code and slug:
            ext = "py" if "python" in s['lang'].lower() else "cpp" if "cpp" in s['lang'].lower() else "java"
            filepath = os.path.join(OUTPUT_DIR, f"{slug}.{ext}")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            
            # 设置 Git 时间戳
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s['timestamp'])))
            subprocess.run(['git', 'add', filepath])
            # 同时把txt也加进去
            save_synced_id(sub_id)
            subprocess.run(['git', 'add', SYNC_LOG])
            
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"], env["GIT_COMMITTER_DATE"] = dt, dt
            subprocess.run(['git', 'commit', '-m', f"Sync: {s['title']} (ID: {sub_id})"], env=env)
            
            count += 1
            time.sleep(2.0) # 稍微慢一点，稳

    log(f"🏁 任务完成！本次新点亮了 {count} 个绿点。")

if __name__ == "__main__":
    main()
