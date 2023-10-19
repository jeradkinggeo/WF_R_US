import os
import subprocess

#Start dot py is to automate the process of executing the DataNormTool.
#Additionally start dot py will pull the latest version of the DataNormTool from the repository.

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
        subprocess.run(['python', 'DataToolEntryPoint.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running 'run.py': {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()