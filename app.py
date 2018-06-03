# coding=utf-8
from flask import Flask, jsonify, render_template
from py2neo import Graph, authenticate

app = Flask(__name__)
# set up authentication parameters
authenticate("localhost:7474", "neo4j", "XXXX")

# connect to authenticated graph database
graph = Graph("http://localhost:7474/db/data/")

def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "label": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.n.properties)

    return {"data": data}

def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node._id),
            "target": str(relationRecord.r.end_node._id),
            "relationship": relationRecord.r.rel.type}

    return {"data": data}

@app.route('/kg/graph')
def index():
    return render_template('index.html')

@app.route('/kg/graph/json')
def get_graph():
    nodes = list(map(buildNodes, graph.cypher.execute('MATCH (n) RETURN n')))
    edges = list(map(buildEdges, graph.cypher.execute('MATCH ()-[r]->() RETURN r')))
    # 保证中文不乱码
    app.config['JSON_AS_ASCII'] = False
    return jsonify(elements = {"nodes": nodes, "edges": edges})

if __name__ == '__main__':
    app.run(debug = True)

