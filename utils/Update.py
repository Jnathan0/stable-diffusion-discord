import subprocess

async def update_local():
    try:
        result = subprocess.run(['/usr/bin/git', 'pull'], encoding='utf-8', capture_output=True, check=True)
        return result.stdout    
    except subprocess.CalledProcessError as e:
        return e