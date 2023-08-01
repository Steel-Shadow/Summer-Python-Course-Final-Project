import json
import os
import sys

from flask import Flask, jsonify, render_template, send_from_directory, request

import manage_Neo4j
from utils.sorter import sort_by_search_key

name = sys.argv[1]
# print(name)
# app_path = os.path.abspath(os.path.dirname(__file__))
app_path = os.getcwd()
name_nodes_path = os.path.join(app_path, 'templates', name + '_nodes.json')
name_links_path = os.path.join(app_path, 'templates', name + '_links.json')
default_nodes_path = os.path.join(app_path, 'templates/origin_nodes.json')
default_links_path = os.path.join(app_path, 'templates/origin_links.json')

# 读取 HTML 文件内容
with open('templates/originKG.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
# 读取用于替换的文件内容
try:
    with open(name_nodes_path, 'r', encoding='utf-8') as file:
        # print('name file found')
        nodes_content = file.read()
except:
    with open(default_nodes_path, 'r', encoding='utf-8') as file:
        # print('use default')
        nodes_content = file.read()
try:
    with open(name_links_path, 'r', encoding='utf-8') as file:
        links_content = file.read()
except:
    with open(default_links_path, 'r', encoding='utf-8') as file:
        links_content = file.read()

# 替换 HTML 内容中的第一个 data=[...] 为 data=[]
modified_content = html_content.replace('"data": []', '"data": ' + nodes_content, 1)
modified_content = modified_content.replace('"links": []', '"links": ' + links_content, 1)

# 写入修改后的内容回到 HTML 文件
with open('templates/for_show.html', 'w', encoding='utf-8') as file:
    file.write(modified_content)


app = Flask(__name__)


@app.route('/')
def chart():
    return render_template('for_show.html')


@app.route('/interact/<path:filename>')
def serve_interact_files(filename):
    return send_from_directory('templates/interact', filename)


@app.route('/api/addNode', methods=['POST'])
def add_node():
    data = request.json  # 获取前端发送的JSON数据
    manage_Neo4j.add_in_neo4j(data)
    # 返回响应
    return jsonify({'message': '新增一个节点成功'})


@app.route('/api/updateNode', methods=['POST'])
def update_node():
    data = request.json  # 获取前端发送的JSON数据
    manage_Neo4j.update_in_neo4j(data)
    # 返回响应
    return jsonify({'message': '更新成功'})


@app.route('/api/getNodeInfo', methods=['POST'])
def list_classes():
    data = request.json  # 获取前端发送的JSON数据
    classes = manage_Neo4j.fetch_data(data['name'])
    # print(data['name'])
    classes = sort_by_search_key(classes, data['name'])
    # classes = [('2022升级-《慕慕到家》家政小程序组件化进阶实战', 'https://coding.imooc.com/class/498.html', 'imooc', ''), ('7天快速学习计算机基础必考八股文', 'https://coding.imooc.com/class/540.html', 'imooc', '')]
    print(classes)
    # 返回响应
    return jsonify({'message': 'success'})


@app.route('/api/saveNodes', methods=['POST'])
def save_nodes():
    data = request.json
    with open('templates/nodes_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True)
    return jsonify({'message': 'success'})


@app.route('/api/saveLinks', methods=['POST'])
def save_links():
    data = request.json
    with open('templates/links_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True)
    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run()
