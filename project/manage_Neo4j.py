from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import utils.sorter
from Spiders import Spiders

KG = Graph("neo4j://47.93.46.112:7687", auth=("neo4j", "buaayyds"))


def add_single(data):
    label = data['category']
    name = data['name']
    father = data['classify']

    # 如果存在同名节点，则不添加重复节点
    matcher = NodeMatcher(KG)
    existing_node = matcher.match(name=name).first()
    if existing_node:
        return

    # 增加节点
    node = Node(label, name=name, fixedName=name, classify=father)
    KG.create(node)
    if 'None' != father:
        father_node = KG.nodes.match(name=father).first()
        rtype = '学科组成' if label == '学科' else '分类'
        relationship = Relationship(father_node, rtype, node)
        KG.create(relationship)

    if '学科' == label:
        res = Spiders.scraping([name, ])

        for w in Spiders.web_scraping:  # 网页
            courses = res.get((w, name))

            if not courses:
                continue

            for course in courses:  # 课程
                e1, e2, e3, e4 = course
                node1 = Node("课程", sour=e1, className=e2, url=e3, school=e4)
                KG.create(node1)
                relation = Relationship(node, "课", node1)
                KG.create(relation)


def add_in_neo4j(data):
    for item in data:
        add_single(item)


def update_node_name(old_name, new_name):
    query = f"""
    MATCH (node {{name: '{old_name}'}})
    SET node.name = '{new_name}'
    RETURN node
    """
    KG.run(query)


def update_in_neo4j(data):
    for item in data:
        update_node_name(item['oldName'], item['name'])


def fetch_data(name):
    relationship_matcher = RelationshipMatcher(KG)

    # 查找指定名称的父节点
    parent_node = KG.nodes.match(name=name).first()

    # 如果没有找到匹配的父节点，则返回空列表
    if not parent_node:
        return []

    # 初始化一个列表来存储子节点的属性
    result_list = []

    # 遍历父节点的所有子节点
    for child_rel in relationship_matcher.match(nodes={parent_node}, rel_type=None):
        child_node = child_rel.end_node
        # 从每个子节点中提取所需的属性
        child_name = child_node.get("className", "")
        child_url = child_node.get("url", "")
        child_sour = child_node.get("sour", "")
        child_school = child_node.get("school", "")

        # 将属性添加到结果列表中
        result_list.append((child_sour, child_name, child_url, child_school))

    return utils.sorter.sort_by_name(result_list[1:])
