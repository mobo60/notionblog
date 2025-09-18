import os
from git import Repo, exc # 從 git 函式庫匯入 Repo 和 exc (用於錯誤處理)

# 您的專案路徑
repo_path = "/home/mobofami/notionblog"

try:
    # 試圖載入現有的儲存庫
    print(f"正在檢查 '{repo_path}' 是否為 Git 儲存庫...")
    repo = Repo(repo_path)
    print("✅ 已成功載入現有的 Git 儲存庫。")

except exc.InvalidGitRepositoryError:
    # 如果載入失敗 (代表不是 Git 儲存庫)，就執行初始化
    print(f"'{repo_path}' 不是一個 Git 儲存庫，現在開始執行初始化 (git init)...")
    repo = Repo.init(repo_path)
    print("✅ 新的 Git 儲存庫初始化完成。")

except Exception as e:
    print(f"❌ 發生非預期的錯誤: {e}")
    exit() # 如果發生其他錯誤，就結束程式

# --- 現在，您可以安全地執行後續的 add, commit, push 操作 ---

try:
    if repo.is_dirty(untracked_files=True):
        print("\n偵測到檔案變動，開始執行 Git 操作...")
        
        # 執行 git add .
        repo.git.add(A=True)
        
        # 執行 git commit
        commit_message = "自動更新：同步 Notion 內容"
        repo.index.commit(commit_message)
        print(f"建立 Commit：'{commit_message}'")

        # 執行 git push
        # 在推送前，先檢查是否已設定遠端儲存庫
        if not repo.remotes:
            print("\n⚠️ 警告：找不到遠端儲Git存庫 (remote origin)。")
            print("這可能是您第一次初始化，請先手動在終端機設定一次遠端：")
            print(f"cd {repo_path}")
            print("git remote add origin https://github.com/YourUsername/notionblog.git")
        else:
            origin = repo.remote(name='origin')
            origin.push()
            print("✅ 成功將變動推送到 GitHub！")
    else:
        print("\n✅ 儲存庫沒有變動，無需執行任何操作。")

except Exception as e:
    print(f"\n❌ Git 操作失敗: {e}")