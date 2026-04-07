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
    log("🚀 正在检索历史提交记录...")
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
            time.sleep(1)
        except: break
    return submissions

def get_detail(sub_id):
    """【防弹版】绝对不会触发 AttributeError"""
    payload = {"query": f"{{ submissionDetail(submissionId: \"{sub_id}\") {{ code question {{ titleSlug }} }} }}"}
    try:
        resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            res_data = resp.json()
            # 采用极致保守的链式获取方式
            data = res_data.get('data', {})
            if data:
                detail = data.get('submissionDetail')
                if detail: # 只有确定 detail 不是 None 才会去拿里面的东西
                    code = detail.get('code')
                    question = detail.get('question', {})
                    slug = question.get('titleSlug') if question else None
                    return code, slug
        log(f"⚠️ 无法获取 ID 为 {sub_id} 的题目详情，可能被限流了，跳过。")
    except Exception as e:
        log(f"❌ 请求详情时发生网络错误: {e}")
    return None, None

def main():
    if not SESSION or not CSRF_TOKEN:
        log("❌ 缺失 Secrets"); sys.exit(1)
    
    all_subs = get_all_accepted_submissions()
    log(f"✅ 共找到 {len(all_subs)} 条通过记录。")
    if not all_subs: return

    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    all_subs.sort(key=lambda x: int(x['timestamp']))
    
    subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'kakayuankaka@gmail.com'])

    # 重点：如果是第一次同步，文件可能会很多，分批提交
    count = 0
    for s in all_subs:
        log(f"📦 正在同步: {s['title']}")
        code, slug = get_detail(s['id'])
        
        if code and slug:
            ext = "py" if "python" in s['lang'].lower() else "cpp" if "cpp" in s['lang'].lower() else "java"
            filepath = os.path.join(OUTPUT_DIR, f"{slug}.{ext}")
            
            # 如果文件已存在，说明这一题已经同步过了，跳过
            if os.path.exists(filepath):
                continue

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s['timestamp'])))
            subprocess.run(['git', 'add', filepath])
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"], env["GIT_COMMITTER_DATE"] = dt, dt
            subprocess.run(['git', 'commit', '-m', f"Sync: {s['title']} ({dt})"], env=env)
            count += 1
            time.sleep(2.0) # 增加到 2 秒，安全第一

    log(f"🏁 任务大功告成！本次新同步了 {count} 道题目。")

if __name__ == "__main__":
    main()
