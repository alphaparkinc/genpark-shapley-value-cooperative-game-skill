import json
import sys
from client import ShapleyValueEngine

def handle_rpc(line):
    try:
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        rid = req.get("id")
        
        if method == "tools/list":
            tools = [
                {"name": "compute_shapley", "description": "Compute Shapley values for coalition values"}
            ]
            return json.dumps({"jsonrpc": "2.0", "id": rid, "result": {"tools": tools}})
        elif method == "tools/call":
            tname = params.get("name")
            args = params.get("arguments", {})
            if tname == "compute_shapley":
                c_map = args["coalition_map"] # stringified frozen-set -> value
                engine = ShapleyValueEngine(args["players"])
                def v(c):
                    key = ",".join(sorted(c))
                    return c_map.get(key, 0.0)
                res = engine.compute(v)
                return json.dumps({"jsonrpc": "2.0", "id": rid, "result": {"shapley_values": res}})
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}})

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(handle_rpc(line.strip()), flush=True)
