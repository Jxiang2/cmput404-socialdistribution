from sdapis.models import Node
from sdapis.serializers import NodeSerializer
import requests

# return a list of valid nodes(hosts)
def get_valid_nodes():
    nodes = Node.objects.all()
    node_serializer = NodeSerializer(nodes, many=True)
    valid_nodes = []
    node = requests.check_compatibility()
    print(node)
    for n in node_serializer.data:
        valid_nodes.append(n["host"])
    return valid_nodes

def is_valid_node(request):
    host = request.build_absolute_uri("/")
    if host not in ["http://127.0.0.1:8000/", "http://localhost:8000/", "https://c404project.herokuapp.com/"]:
        valid_nodes = get_valid_nodes()
        if host not in valid_nodes:
            return False
    return True
