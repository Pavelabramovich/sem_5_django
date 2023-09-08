import http.client as client


def internet_connection_exists() -> bool:
    conn = client.HTTPSConnection("8.8.8.8", timeout=5)

    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False
    finally:
        conn.close()
