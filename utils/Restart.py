import os
import sys
import asyncio

async def restart_process():
    pid = os.getpid()
    try:
        os.execv(sys.argv[0], sys.argv)
    except Exception as e:
        return e