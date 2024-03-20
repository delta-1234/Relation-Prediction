import csv
from neo4j import GraphDatabase

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_or_get_node(self, label, properties):
        with self._driver.session() as session:
            return session.execute_write(self._create_or_get_node, label, properties)

    @staticmethod
    def _create_or_get_node(tx, label, properties):
        query = f"MATCH (n:{label}) WHERE n.name = $name RETURN n"
        result = tx.run(query, name=properties["name"])
        existing_node = result.single()

        if existing_node:
            return existing_node["n"]
        else:
            create_query = f"CREATE (n:{label} $properties) RETURN n"
            created_node = tx.run(create_query, properties=properties).single()
            return created_node["n"]

    def create_relationship(self, node1, relationship, node2):
        with self._driver.session() as session:
            session.execute_write(self._create_relationship, node1, relationship, node2)

    @staticmethod
    def _create_relationship(tx, node1, relationship, node2):
        query = f"MATCH (a), (b) WHERE id(a) = $node1 AND id(b) = $node2 CREATE (a)-[:`{relationship}`]->(b)"
        tx.run(query, node1=node1.id, node2=node2.id)

# 配置Neo4j连接信息
uri = "bolt://localhost:7687"
user = "neo4j"
password = "88888888"

# 创建KnowledgeGraph实例
graph = KnowledgeGraph(uri, user, password)

# 读取CSV文件并创建节点和关系
with open('.\data\\2021\data2021.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # 创建或获取头节点
        head_properties = {"name": row['head']}
        head_node = graph.create_or_get_node("Person", head_properties)

        # 创建或获取尾节点
        tail_properties = {"name": row['tail']}
        tail_type = 'tailType' + str(row['tail_offset'])
        tail_node = graph.create_or_get_node(tail_type, tail_properties)

        # 创建关系
        graph.create_relationship(head_node, row['relation'], tail_node)

# 关闭Neo4j连接
graph.close()
