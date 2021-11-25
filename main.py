import requests  # 导入requests 模块
import json
import pandas as pd

def fetch_github_issue(access_token=None, repo_user=None, repo_addr=None, first_page=1, csv_path='issue.csv'):
    """
    :param access_token: 用于突破github api 访问限制
    :param repo_user: github repo的创建用户名
    :param repo_addr: github repo仓库名
    :param first_page: 起始页，默认为1
    :param csv_path: 用于指定最后生成的csv名称和存储地址
    :return: 无
    """

    # 给请求指定一个请求头来模拟chrome浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        "Authorization": "token "+access_token
        }
    # 请求的github仓库地址
    web_url = 'https://api.github.com/repos/' + repo_user + '/' + repo_addr + '/issues?state=all'
    cnt = 0
    github_issue_dict = {}
    page = first_page  # 起始页
    web_url_diff_page = web_url + '&page=' + str(page)
    print(web_url_diff_page)
    github_issue_request = requests.get(web_url_diff_page, headers=headers)  # 像目标url地址发送get请求，返回一个response对象
    github_issue_set = json.loads(github_issue_request.text)
    while len(github_issue_set) > 0:
        print('page:', page)
        for single_github_issue in github_issue_set:
            try:
                for label in single_github_issue['labels']:
                    if label['name'] == 'Type:Bug' or label['name'] == 'bug' or label['name'] == 'Bug':
                        single_github_dict = {'number': single_github_issue['number'], 'title': single_github_issue['title'],
                                              'time': single_github_issue['created_at']}
                        github_issue_dict[cnt] = single_github_dict
                        cnt += 1
            except:
                pass
        page += 1
        web_url_diff_page = web_url + '&page=' + str(page)
        github_issue_request = requests.get(web_url_diff_page, headers=headers)  # 像目标url地址发送get请求，返回一个response对象
        github_issue_set = json.loads(github_issue_request.text)

    filename_df = pd.DataFrame.from_dict(github_issue_dict)
    word_vector = filename_df.T
    word_vector.to_csv(csv_path)


if __name__ == '__main__':
    your_access_token = input("请输入你的access_toekn：")
    repo_user = input("请输入仓库拥有者的用户名：")
    repo_addr = input("请输入仓库名：")
    csv_path = input("请输入csv的文件名，以.csv结尾")
    fetch_github_issue(access_token=your_access_token, repo_user=repo_user,
                       repo_addr=repo_addr, csv_path=csv_path)
