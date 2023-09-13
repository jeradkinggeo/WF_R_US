import os
import subprocess


def git_pull_origin():
    try:
        subprocess.run(['git', 'pull', 'origin'], check=True)
        print("Git pull completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running 'git pull origin': {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

def main():

    git_pull_origin()

    # After updating the repository, you can call run.py
    try:
        subprocess.run(['python', 'run.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running 'run.py': {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)