import requests
import os

# 从 GitHub Secrets 获取密钥
SESSION = os.getenv('LEETCODE_SESSION')
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN')

def get_submissions():
    url = "https://leetcode.cn/graphql/"
    headers = {
        "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN}",
        "X-CSRFToken": CSRF_TOKEN,
        "Referer": "https://leetcode.cn/progress/",
    }
    # 这里的查询语句是力扣获取最近提交记录的标准接口
    payload = {
        "query": """
        query submissions($offset: Int, $limit: Int) {
            submissionList(offset: $offset, limit: $limit) {
                submissions {
                    id
                    title
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
    else:
        print(f"登录失败，状态码: {resp.status_code}")
        return []

# 后续可以继续写：获取题目详情、保存为文件等逻辑
if __name__ == "__main__":
    subs = get_submissions()
    for s in subs:
        if s['statusDisplay'] == 'Accepted':
            print(f"找到已通过题目: {s['title']}, 语言: {s['lang']}")
