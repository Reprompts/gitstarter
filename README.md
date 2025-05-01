# gitstarter

**Hybrid Streamlit UI** that automates Git-CLI workflows for beginners and GitHub-API tasks for power users—all from your local directory.

---

## 📄 License

This project is released under the MIT License (see [LICENSE](LICENSE)).  
© 2025 RePromptsQuest. All rights reserved.

---

## 🔗 Links

- **GitHub**: https://github.com/reprompts/gitstarter  

- **LinkedIn Group**: https://www.linkedin.com/groups/14631875/  

- **Twitter / X**: [@RepromptsQuest](https://twitter.com/RepromptsQuest)  

- **Dev.to**: https://dev.to/repromptsquest  

---

## ✨ Features

- 🚀 **Workflow-driven UI**: Choose scenarios (Init, Clone, Commit, PRs, etc.) from a sidebar  
- 🧩 **Pure Git-CLI automation**: No token needed for local Git commands (`init`, `add`, `commit`, `push`, `pull`, `branch`, `stash`, `merge`, `log`)  
- 🔐 **Optional GitHub API**: Create repos & pull-requests when you paste your PAT  
- 🌐 **Persistent Repo URL**: Enter once, use across all workflows  
- 🧠 **Educational**: Previews actual Git commands, shows output and errors  
- ⚙️ **Settings**: Edit `user.name` / `user.email`, manage PAT, reset `.git`  

---

## 🚀 Quickstart

1. **Install**  
   ```bash
   pip install gitstarter

Run:
gitstarter


Follow the UI

Paste your repo URL at the top (optional for local-only work).

Select a workflow in the sidebar (e.g. “Init / Reset Git Repo”, “Commit & Push”).

Click buttons to run Git commands—no terminal typing needed.

🛡️ Security
No telemetry: gitstarter does not phone home or collect usage data.

Token safety: Your GitHub PAT is stored only in Streamlit session state and the environment; it is never logged.

Error handling: All errors from Git CLI or GitHub API are caught and displayed in the UI.

🤝 Contributing
We welcome all contributions! See CONTRIBUTING.md for guidelines.

