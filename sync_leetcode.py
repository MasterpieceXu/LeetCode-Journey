import requests
import os
import time

# 配置
SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')
OUTPUT_DIR = "solutions"

def get_submissions():
    url = "https://leetcode.cn/graphql/"
    headers = {
        "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN}",
        "X-CSRFToken": CSRF_TOKEN,
        "Referer": "https://leetcode.cn/progress/",
    }
    # 获取最近20条通过的记录
    payload = {
        "query": """
        query submissions($offset: Int, $limit: Int) {
            submissionList(offset: $offset, limit: $limit) {
                submissions {
                    id
                    title
                    titleSlug
                    statusDisplay
                    lang
                    timestamp
                }
            }
        }
        """,
        "variables": {"offset": 0, "limit": 20}
    }
    
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 200:
        return resp.json()['data']['submissionList']['submissions']
    return []

def save_solution(sub):
    if sub['statusDisplay'] != 'Accepted':
        return
        
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # 文件名格式：题目-语言.ext
    ext = "py" if "python" in sub['lang'].lower() else "cpp"
    filename = f"{sub['titleSlug']}.{ext}"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 注意：这里为了演示简单只存了标记。
    # 真正的源码需要再调一次 graphql 获取，先跑通流程
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Title: {sub['title']}\n")
        f.write(f"# Language: {sub['lang']}\n")
        f.write(f"# Timestamp: {time.ctime(int(sub['timestamp']))}\n")
        f.write("\n# 此处后续可扩展抓取源码逻辑\n")
    print(f"已保存: {filename}")

if __name__ == "__main__":
    submissions = get_submissions()
    for s in submissions:
        save_solution(s)
