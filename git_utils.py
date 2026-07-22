import subprocess

# ==========================================================
# Run Git Command
# ==========================================================

def run_git(command):

    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    return result.returncode


# ==========================================================
# Git Add
# ==========================================================

def git_add():

    print()
    print("=" * 60)
    print("GIT ADD")
    print("=" * 60)

    status = run_git("git add .")

    if status != 0:
        raise Exception("Git Add Failed.")

    return status


# ==========================================================
# Git Commit
# ==========================================================

def git_commit(message):

    print()
    print("=" * 60)
    print("GIT COMMIT")
    print("=" * 60)

    status = run_git(f'git commit -m "{message}"')

    if status != 0:
        raise Exception("Git Commit Failed.")

    return status


# ==========================================================
# Git Push
# ==========================================================

def git_push():

    print()
    print("=" * 60)
    print("GIT PUSH")
    print("=" * 60)

    status = run_git("git push origin main")

    if status != 0:
        raise Exception("Git Push Failed.")

    return status


# ==========================================================
# Complete Git Update
# ==========================================================

def git_update(report_date):

    git_add()

    git_commit(f"Daily IMD Update - {report_date}")

    git_push()