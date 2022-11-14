import os
import sys
import asyncio

async def restart_process():
    python = sys.executable
    try:
        os.execl(python, python, * sys.argv)
    except Exception as e:
        return e