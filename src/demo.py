import requests


def run(event, context):
    resp = requests.get("https://www.astrolabe-expeditions.org/")
    return {
        "body": f"Response status: {resp.status_code}",
        "headers": {
            "Content-Type": ["text/plain"],
        },
    }

if __name__ == "__main__":
    from scaleway_functions_python import local
    local.serve_handler(run)
