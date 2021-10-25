#nothing to impoer now

def is_valid_node(request):
    host = request.build_absolute_uri("/")
    if host not in ["http://127.0.0.1:8000/", "http://127.0.0.1:9000/", "http://localhost:8000/", "https://c404project.herokuapp.com/"]:
        return False
    return True
