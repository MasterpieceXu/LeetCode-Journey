import requests
import os
import time
import subprocess
import sys

# 强制实时刷新日志
def log(msg):
    print(msg, flush=True)

# 密钥（Secrets 里只填乱码！）
SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')
OUTPUT_DIR = "solutions"

log("--- 脚本开始运行 ---")

if __name__ == "__main__":
    if not SESSION or not CSRF_TOKEN:
        log("❌ 错误：Secrets 没设置好！请检查 LEETCODE_SESSION 和 LEETCODE_CSRF_TOKEN")
        sys.exit(1)

    log("🚀 正在尝试连接力扣...")
    
    headers = {
        "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN}",
        "X-CSRFToken": CSRF_TOKEN,
        "Referer": "https://leetcode.cn/progress/",
        "User-Agent": "Mozilla/5.0"
    }
    
    payload = {
        "query": "query s($o: Int, $l: Int) { submissionList(offset: $o, limit: $l) { submissions { id title titleSlug statusDisplay timestamp } hasNext } }",
        "variables": {"o": 0, "l": 20}
    }

    try:
        resp = requests.post("https://leetcode.cn/graphql/", json=payload, headers=headers)
        if resp.status_code != 200:
            log(f"❌ 登录失败，HTTP 状态码: {resp.status_code}")
            sys.exit(0)
            
        data = resp.json().get('data', {}).get('submissionList', {})
        raw_subs = data.get('submissions', [])
        
        if not raw_subs:
            log("⚠️ 登录上去了，但没抓到题。大概率是 Cookie 没填对！")
            sys.exit(0)

        subs = [s for s in raw_subs if s['statusDisplay'] == 'Accepted']
        log(f"✅ 成功！发现 {len(subs)} 道通过的题目。")

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        for s in subs:
            filepath = os.path.join(OUTPUT_DIR, f"{s['titleSlug']}.py")
            with open(filepath, "w") as f:
                f.write(f"# {s['title']}\n# Date: {time.ctime(int(s['timestamp']))}")
            
            # 回溯时间 Commit
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(s['timestamp'])))
            log(f"📦 提交: {s['title']} ({dt})")
            
            subprocess.run(['git', 'add', filepath])
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"], env["GIT_COMMITTER_DATE"] = dt, dt
            subprocess.run(['git', 'config', '--global', 'user.name', 'MasterpieceXu'])
            subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])
            subprocess.run(['git', 'commit', '-m', f"Sync: {s['title']}"], env=env)

    except Exception as e:
        log(f"❌ 运行报错: {e}")

    log("--- 任务结束 ---")
