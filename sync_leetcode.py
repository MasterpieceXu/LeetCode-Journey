import requests
import os
import sys

# 强制实时输出日志
def log(msg):
    print(msg, flush=True)

# 从 Secrets 获取（确保里面只有纯乱码！）
SESSION = os.getenv('LEETCODE_SESSION', '').strip()
CSRF_TOKEN = os.getenv('LEETCODE_CSRF_TOKEN', '').strip()

log("--- 🛠️ 诊断开始 ---")

if not SESSION or not CSRF_TOKEN:
    log("❌ 错误：环境变量为空，请检查 GitHub Secrets 名称是否拼写正确。")
    sys.exit(1)

# 构造标准 Headers
# 重点：X-CSRFToken 必须和 Cookie 里的 csrftoken 一致
headers = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};",
    "X-CSRFToken": CSRF_TOKEN,
    "Origin": "https://leetcode.cn",
    "Referer": "https://leetcode.cn/progress/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# 这是一个最基础的查询，用来测试连通性
query = {
    "query": "{ submissionList(offset: 0, limit: 1) { submissions { id } } }"
}

log(f"🚀 正在尝试连接 https://leetcode.cn/graphql/ ...")

try:
    response = requests.post("https://leetcode.cn/graphql/", json=query, headers=headers)
    
    if response.status_code == 200:
        log("🎉 成功！接口握手成功。")
        # 如果成功了，可以在这里打印一下题目数量看看
        data = response.json()
        log("数据抓取正常。")
    else:
        log(f"❌ 失败，状态码: {response.status_code}")
        log("--- 力扣服务器返回的报错信息如下 ---")
        log(response.text) # 这一行是破案的关键！
        log("----------------------------------")
        
except Exception as e:
    log(f"❌ 网络请求发生异常: {e}")

log("--- 诊断结束 ---")
