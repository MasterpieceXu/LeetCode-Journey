import requests
import os
import time

# 配置
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
    """获取所有已通过的提交记录"""
    submissions = []
    offset = 0
    limit = 20
    
    while True:
        print(f"正在获取第 {offset // limit + 1} 页记录...")
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
                    }
                    hasNext
                }
            }
            """,
            "variables": {"offset": offset, "limit": limit}
        }
        
        resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
        if resp.status_code != 200:
            print(f"请求失败: {resp.status_code}")
            break
            
        data = resp.json().get('data', {}).get('submissionList', {})
        new_subs = data.get('submissions', [])
        
        # 只保留 Accepted 的记录
        for s in new_subs:
            if s['statusDisplay'] == 'Accepted':
                submissions.append(s)
        
        if not data.get('hasNext') or offset > 500: # 安全阈值，防止死循环
            break
        offset += limit
        time.sleep(1) # 频率控制，防止被封
    
    return submissions

def get_submission_code(submission_id):
    """根据提交 ID 获取源代码"""
    payload = {
        "query": """
        query submissionDetails($submissionId: ID!) {
            submissionDetail(submissionId: $submissionId) {
                code
            }
        }
        """,
        "variables": {"submissionId": submission_id}
    }
    resp = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get('data', {}).get('submissionDetail', {}).get('code')
    return None

def main():
    if not SESSION or not CSRF_TOKEN:
        print("错误: 缺少环境变量 LEETCODE_SESSION 或 LEETCODE_CSRF_TOKEN")
        exit(1)

    subs = get_all_accepted_submissions()
    print(f"共找到 {len(subs)} 条已通过记录。")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 为了避免重复爬取同一题，我们可以按题目 titleSlug 去重，只拿最新的那次通过记录
    seen_problems = set()
    for s in subs:
        if s['titleSlug'] in seen_problems:
            continue
        
        print(f"正在抓取代码: {s['title']} ({s['lang']})")
        code = get_submission_code(s['id'])
        
        if code:
            ext = "py" if "python" in s['lang'].lower() else "cpp" if "cpp" in s['lang'].lower() else "java" if "java" in s['lang'].lower() else "txt"
            filename = f"{s['titleSlug']}.{ext}"
            with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                f.write(code)
            seen_problems.add(s['titleSlug'])
            time.sleep(1.5) # 爬取源码需要时间间隔

if __name__ == "__main__":
    main()
