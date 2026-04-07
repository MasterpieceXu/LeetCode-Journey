import requests
import os
import time
import subprocess
import sys

def log(msg):
    print(msg, flush=True)

# 从 Secrets 获取
SESSION = os.getenv('LEETCODE_SESSION', '').strip()
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN', '').strip()
GIT_EMAIL = os.getenv('GIT_EMAIL', '你的隐私邮箱@users.noreply.github.com') # 建议用 Secret 传入
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
    
    all_subs = get_all_accepted_submissions()
    log(f"✅ 共找到 {len(all_subs)} 条通过记录。")
    if not all_subs: return

    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    # 【关键】按时间从旧到新排序，确保最新的代码在最后一次提交
    all_subs.sort(key=lambda x: int(x['timestamp']))
    
    subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
    subprocess.run(['git', 'config', '--global', 'user.email', kakayuankaka@gmail.com])

    # 记录已经在这个“当前批次”中提交过的 ID，防止死循环
    processed_ids = set()
    
    for s in all_subs:
        # 获取这道题的文件路径
        # 注意：为了拿 slug，还是得调一下 detail 接口
        log(f"📦 正在处理: {s['title']} (提交 ID: {s['id']})")
        
        # 我们可以通过简单的 Git 检查来判断“这一秒的这次提交”是否已经做过了
        code, slug = get_detail(s['id'])
        
        if code and slug:
            ext = "py" if "python" in s['lang'].lower() else "cpp" if "cpp" in s['lang'].lower() else "java"
            filepath = os.path.join(OUTPUT_DIR, f"{slug}.{ext}")
            
            # 不再检查文件是否存在，直接覆盖写入！
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            
            # 盖上当年的邮戳
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s['timestamp'])))
            subprocess.run(['git', 'add', filepath])
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"], env["GIT_COMMITTER_DATE"] = dt, dt
            
            # 即使文件名一样，只要日期不同，这就是一个新的 Commit
            subprocess.run(['git', 'commit', '-m', f"Sync: {s['title']} ({dt})"], env=env)
            
            # 适当延时防止限流
            time.sleep(1.5)

    log("🏁 顺利拉取！")

if __name__ == "__main__":
    main()
