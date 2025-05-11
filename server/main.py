from mcp_sdk import Tool, Server
import os, shutil, hashlib, zipfile

@Tool
def list_dir(path: str) -> list[str]:
    return os.listdir(os.path.expanduser(path))

@Tool
def move_file(src: str, dst: str) -> str:
    shutil.move(os.path.expanduser(src), os.path.expanduser(dst))
    return "moved"

@Tool
def delete_dup(path: str) -> int:
    seen, removed = set(), 0
    for root, _, files in os.walk(os.path.expanduser(path)):
        for f in files:
            p = os.path.join(root, f)
            h = hashlib.md5(open(p,'rb').read()).hexdigest()
            if h in seen:
                os.remove(p); removed += 1
            else:
                seen.add(h)
    return removed

@Tool
def compress(path: str, out_zip: str) -> str:
    with zipfile.ZipFile(out_zip,'w') as z:
        for root, _, files in os.walk(os.path.expanduser(path)):
            for f in files:
                full = os.path.join(root,f)
                z.write(full, full.replace(path, ""))
    return out_zip

Server(tools=[list_dir, move_file, delete_dup, compress]).run()
