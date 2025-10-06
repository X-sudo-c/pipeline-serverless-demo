import json
import socket

def check_host(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        host = body.get("host")
        port = body.get("port", 80)

        if not host:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing host"})}

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            status = "active"
        else:
            status = "inactive"

        return {
            "statusCode": 200,
            "body": json.dumps({"host": host, "port": port, "status": status})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
