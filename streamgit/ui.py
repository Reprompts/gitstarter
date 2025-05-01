import os
import streamlit as st
from .config import get_github_token, set_github_token
from .detector import git_installed, is_git_repo
import streamgit.git_utils as gu
import streamgit.github_utils as gh

WORKFLOWS = [
    "Init / Reset Git Repo",
    "Create New Project",
    "Existing Local Project",
    "Commit & Push",
    "Pull & Sync",
    "Branch Management",
    "Pull Requests",
    "Stash & Restore",
    "Logs & Diff",
    "Settings"
]

def sidebar():
    st.sidebar.title("🔧 Workflows")
    st.sidebar.markdown("Select the task you want to perform. Each section will guide you through the steps.")
    choice = st.sidebar.radio("", WORKFLOWS)
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 GitHub Token (optional)")
    token = st.sidebar.text_input(
        "Paste PAT to enable GitHub API features",
        type="password",
        value=st.session_state.get("github_token",""),
        key="github_token_input"
    )
    if st.sidebar.button("Save Token"):
        if token.strip():
            set_github_token(token.strip())
            st.sidebar.success("Token saved for this session")
        else:
            st.sidebar.error("Please enter a non-empty token")
    return choice

def show(res):
    st.markdown("**Command run:**")
    st.code(res["cmd"])
    st.markdown("**Output:**")
    st.text_area("", res.get("output",""), height=100)
    if not res["success"]:
        st.error("⚠️ Command failed. Check the output above for errors.")

def main_ui():
    st.title("🧩 GitStarter Tutorial UI")
    st.markdown(
        "Welcome to GitStarter!  \n"
        "_Tip: Run this UI in one terminal session. To use your normal shell alongside, open a second terminal._  \n"
        "To stop this UI, press **Ctrl+C** in the terminal where you launched it (works on Windows, macOS, Linux)."
    )

    if not git_installed():
        st.error("Git CLI not found. Please install Git (https://git-scm.com/) and restart.")
        return

    # Repo URL only once at top
    if "repo_url" not in st.session_state:
        st.session_state.repo_url = ""
    st.markdown("### 🌐 Repository URL (optional)")
    st.markdown(
        "Paste your GitHub repo URL here once if you plan to push or create PRs. "
        "All workflows will use this value automatically."
    )
    repo = st.text_input("", value=st.session_state.repo_url, key="repo_url")
    if repo:
        st.success(f"Using repo URL: `{repo}` for all workflows")
    st.markdown("---")

    choice = sidebar()

    # 1. Init / Reset
    if choice == WORKFLOWS[0]:
        st.header("🛠️ Init / Reset Git Repo")
        st.markdown("Initialize a fresh Git repo or remove an existing one to start over.")
        path = st.text_input("Folder path", value=".", key="init_path")
        st.info("Step 1: Initialize or reset the Git repository in the specified folder.")
        if st.button("Initialize Git Repo"):
            st.caption("Raw command: `git init {path}`")
            show(gu.init_repo(path))
        if st.button("Remove .git directory"):
            st.caption("Raw command: `rm -rf {path}/.git` (or equivalent)")
            show(gu.remove_git(path))
        st.markdown("**What’s next?** → Choose **Create New Project** or **Existing Local Project** in the sidebar.")

    # 2. Create New Project
    elif choice == WORKFLOWS[1]:
        st.header("🚀 Create New GitHub Project")
        st.markdown("1. On GitHub, create a new repository → https://github.com/new  \n"
                    "2. Paste that repo’s clone URL above.  \n"
                    "3. Initialize, add remote, and clone locally.")
        if repo:
            if not is_git_repo():
                st.info("Step: Initialize this folder as Git repo.")
                if st.button("git init"):
                    st.caption("Raw command: `git init`")
                    show(gu.init_repo())
            else:
                st.success("Folder is already a Git repo.")
            st.info("Step: Link your local repo to GitHub.")
            if st.button("git remote add origin"):
                st.caption(f"Raw command: `git remote add origin {repo}`")
                show(gu.add_remote("origin", repo))
            st.info("Step: Clone the repository into this folder.")
            if st.button("git clone"):
                st.caption(f"Raw command: `git clone {repo}`")
                show(gu.clone_repo(repo))
            st.markdown("**Next:** Go to **Commit & Push** to version your code.")
        else:
            st.warning("Paste your new repo URL above to proceed.")

    # 3. Existing Local Project
    elif choice == WORKFLOWS[2]:
        st.header("🗂️ Existing Local Project")
        st.markdown("Turn an existing folder into a Git repo and optionally link to GitHub.")
        path = st.text_input("Project path", value=".", key="exist_path")
        try:
            os.chdir(path)
            st.write(f"Current folder: `{os.getcwd()}`")
        except Exception as e:
            st.error(f"Cannot access `{path}`: {e}")
            return
        if is_git_repo():
            st.success("This folder is already a Git repository.")
            st.info("You can remove and re-init if needed.")
            if st.button("Remove .git"):
                st.caption("Raw command: `rm -rf .git`")
                show(gu.remove_git(path))
        else:
            st.info("Folder is not a Git repo yet.")
            if st.button("git init"):
                st.caption("Raw command: `git init`")
                show(gu.init_repo(path))
        if repo:
            st.info("Link this repo to GitHub:")
            if st.button("git remote add origin"):
                st.caption(f"Raw command: `git remote add origin {repo}`")
                show(gu.add_remote("origin", repo))
        st.markdown("**Next:** Go to **Commit & Push** to start versioning.")

    # 4. Commit & Push
    elif choice == WORKFLOWS[3]:
        st.header("🔁 Commit & Push")
        st.markdown("Stage changes, commit with a message, then push to GitHub.")
        res = gu.status_porcelain()
        files = res["files"]
        st.markdown("**Unstaged changes:**")
        if files:
            sel = st.multiselect("Select files to stage", files, key="stage_sel")
            if st.button("git add"):
                st.caption("Raw command: `git add <files>`")
                show(gu.stage_files(sel))
        else:
            st.info("No untracked or modified files.")
        msg = st.text_input("Commit message", key="commit_msg")
        if st.button("git commit"):
            st.caption('Raw command: `git commit -m "your message"`')
            show(gu.commit(msg))
        st.info("After commit, you can push to the remote repository.")
        if st.button("git push"):
            st.caption("Raw command: `git push origin <branch>`")
            show(gu.push())
        st.markdown("⚠️ If you see merge conflicts, use **Pull & Sync** or **Stash & Restore** first.")

    # 5. Pull & Sync
    elif choice == WORKFLOWS[4]:
        st.header("📥 Pull & Sync")
        st.markdown("Fetch and merge changes from the remote before you start working.")
        if st.button("git pull"):
            st.caption("Raw command: `git pull origin <branch>`")
            show(gu.pull())
        st.markdown("⚠️ Conflicts can occur if remote changes overlap yours. Resolve via **Branch Management** or **Stash & Restore**.")

    # 6. Branch Management
    elif choice == WORKFLOWS[5]:
        st.header("🌿 Branch Management")
        st.markdown("Create, switch, and merge branches to keep features isolated.")
        show(gu.list_branches())
        new = st.text_input("New branch name", key="new_br")
        if st.button("create & checkout"):
            st.caption("Raw command: `git checkout -b <new-branch>`")
            show(gu.create_branch(new))
        sw = st.text_input("Switch to branch", key="sw_br")
        if st.button("checkout"):
            st.caption("Raw command: `git checkout <branch>`")
            show(gu.checkout(sw))
        mg = st.text_input("Merge branch into current", key="mg_br")
        if st.button("merge"):
            st.caption("Raw command: `git merge <branch>`")
            show(gu.merge(mg))
        st.markdown("**Tip:** Keep branches small to minimize conflicts.")

    # 7. Pull Requests
    elif choice == WORKFLOWS[6]:
        st.header("📌 Pull Requests")
        st.markdown("List or create PRs on GitHub. Requires a repo URL & token.")
        if not repo:
            st.warning("Enter the repo URL above to enable PR features.")
        else:
            if st.button("List Open PRs"):
                for pr in gh.list_pull_requests(*repo.split("/")[-2:]):
                    st.write(f"- [{pr.title}]({pr.html_url}) by {pr.user.login}")
            if st.checkbox("Create PR"):
                t = st.text_input("PR Title", key="pr_t")
                b = st.text_area("PR Description", key="pr_b")
                h = st.text_input("Head branch", key="pr_h")
                ba = st.text_input("Base branch", "main", key="pr_base")
                if st.button("Submit PR", key="submit_pr"):
                    st.caption("Raw API call: create_pull_request(owner, repo, title, body, head, base)")
                    res = gh.create_pull_request(*repo.split("/")[-2:], t, b, h, ba)
                    if res["success"]:
                        st.success(f"PR created: {res['url']}")
                    else:
                        st.error(res["error"])
        st.markdown("**Next:** Review or merge your PR on the GitHub website.")

    # 8. Stash & Restore
    elif choice == WORKFLOWS[7]:
        st.header("🧳 Stash & Restore")
        st.markdown("Temporarily save changes without committing, then reapply later.")
        if st.button("git stash"):
            st.caption("Raw command: `git stash`")
            show(gu.stash())
        if st.button("git stash apply"):
            st.caption("Raw command: `git stash apply`")
            show(gu.stash_apply())
        st.markdown("**Tip:** Stash before switching branches with uncommitted work.")

    # 9. Logs & Diff
    elif choice == WORKFLOWS[8]:
        st.header("🔍 Logs & Diff")
        st.markdown("View the commit history graph to understand project changes.")
        if st.button("Show log"):
            st.caption("Raw command: `git log --oneline --graph --decorate -n 20`")
            show(gu.log())
        st.markdown("**Tip:** Use logs before branching or merging to pick the right commit.")

    # 10. Settings
    else:
        st.header("⚙️ Settings & Git Config")
        st.markdown("Set your global Git identity and manage advanced options.")
        name = st.text_input(
            "user.name", value=os.getenv("GIT_AUTHOR_NAME",""), key="cfg_name"
        )
        email = st.text_input(
            "user.email", value=os.getenv("GIT_AUTHOR_EMAIL",""), key="cfg_email"
        )
        if st.button("Set config"):
            st.caption('Raw command: `git config --global user.name "<name>"` and `git config --global user.email "<email>"`')
            show(gu.run_cmd(f'git config --global user.name "{name}"'))
            show(gu.run_cmd(f'git config --global user.email "{email}"'))
        st.markdown("This applies to all your Git commits on this machine.")
