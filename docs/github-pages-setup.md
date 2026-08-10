# GitHub Pages 开通步骤

这份文档只讲一件事：把这个项目放到 GitHub 上，并让它自动刷新后发布到 Pages。

## 先认清 3 个名字

- `.github/workflows/refresh-and-deploy.yml`：真正的工作流文件路径。
- `Refresh data and deploy Pages`：GitHub `Actions` 页面里看到的工作流名字。
- `https://<用户名>.github.io/<仓库名>/`：最终网页地址。

你在 GitHub 页面里看不到“文件”，通常不是坏了，而是还没把 `.github/workflows/refresh-and-deploy.yml` 这个文件上传到仓库。

## 推荐做法

推荐用 `git push`。它最稳，不容易漏掉隐藏目录 `.github/`。

### 1. 检查本地文件

先确认本地能看到这个文件：

```bash
ls .github/workflows/refresh-and-deploy.yml
```

如果能看到，就说明工作流文件在本地已经准备好了。

### 2. 在 GitHub 新建仓库

1. 登录 GitHub。
2. 点右上角 `+`。
3. 选 `New repository`。
4. 仓库名随意，比如 `hospital`。
5. 不要先勾选初始化 README、.gitignore 或 license。

### 3. 用命令行把整个项目推上去

打开终端，进入你的项目目录：

```bash
cd /path/to/hospital
```

如果这里还不是 git 仓库，先初始化：

```bash
git init
```

如果 `git status` 已经能正常输出，那就说明仓库已经初始化过，可以跳过这一步。

然后提交并推送：

```bash
git add .
git commit -m "Initial publish"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

这一步会把整个项目一起上传，包括 `.github/workflows/refresh-and-deploy.yml`。

如果 `git remote add origin` 提示 origin 已存在，就改用：

```bash
git remote set-url origin https://github.com/<你的用户名>/<仓库名>.git
```

### 4. 如果你非要用网页上传

必须上传整个项目根目录，至少要包含这些内容：

- `.github/workflows/refresh-and-deploy.yml`
- `frontend-prototype/`
- `data-access-research/`
- `scripts/`
- `docs/`
- `requirements.txt`

不要只上传 `frontend-prototype/`。如果只上传前端文件，GitHub Pages 也许能显示页面，但自动刷新不会存在。

### 5. 在 GitHub 上开启 Pages

1. 打开你的仓库主页。
2. 点右上方 `Settings`。
3. 左侧点 `Pages`。
4. 在 `Build and deployment` 区域，把 `Source` 改成 `GitHub Actions`。
5. 如果页面提示保存，点击保存。

### 6. 在 GitHub 上开启 Actions

1. 回到仓库主页。
2. 点上方的 `Actions`。
3. 如果 GitHub 提示你启用 Actions，点允许。
4. 左侧栏找到 `Workflows`。
5. 点 `Refresh data and deploy Pages`。

### 7. 手动跑第一次

1. 在工作流页面右上角点 `Run workflow`。
2. `Branch` 选择你的主分支，通常是 `main`。
3. `with_wechat_fetch` 默认不勾选。
4. 点绿色的 `Run workflow` 确认。
5. 等待任务跑完，看到绿色成功标记。

如果你想让它顺便抓微信候选入口，就勾选 `with_wechat_fetch`。第一次建议不勾选，先确认基础链路正常。

### 8. 查看在线地址

1. 回到 `Settings -> Pages`。
2. 等几分钟。
3. 页面会显示在线地址。
4. 以后用这个地址访问，而不是去 GitHub 仓库里点源码文件。

## 如果找不到工作流

先按这个顺序排查：

1. 仓库里是否真的有 `.github/workflows/refresh-and-deploy.yml`。
2. 这个文件是否已经提交并推送到了 GitHub。
3. 默认分支是不是 `main` 或 `master`，如果不是，要改 workflow 里的 `push.branches`。
4. `Settings -> Actions -> General` 是否禁用了 Actions。
5. 你是不是只上传了 `frontend-prototype/`，漏掉了项目根目录。

## 如果报 `requirements.txt` 找不到

这说明 GitHub Actions 已经进到你的仓库里了，但仓库根目录缺了这个文件。通常是下面两种情况之一：

1. 你只上传了部分文件，没有把整个项目根目录一起推上去。
2. 你把项目又套了一层文件夹，比如仓库里变成了 `hospital/requirements.txt`，而不是根目录直接有 `requirements.txt`。

你在 GitHub 仓库首页点开后，应该直接能看到这些顶层目录和文件：

- `.github`
- `frontend-prototype`
- `data-access-research`
- `docs`
- `scripts`
- `requirements.txt`

如果你看到的是一个大文件夹，点进去才是这些内容，那就说明你上传错层级了。把里面那层内容整体重新推到仓库根目录。

最稳的修法是重新在本地项目目录里运行一次：

```bash
cd /Users/shiliu/Documents/hospital-app
git add .
git commit -m "Add GitHub Pages workflow"
git push
```

这样会把 `requirements.txt` 和隐藏目录 `.github/` 一起带上去。

## 如果 Pages 还是 404

1. 先等 1 到 3 分钟。
2. 再刷新一次页面。
3. 去 `Actions` 看最新一次 workflow 是否成功。
4. 如果 workflow 成功但还是 404，回 `Settings -> Pages` 再确认 `Source` 是 `GitHub Actions`。

## 本地预览

如果你只是想先看页面，不用配置 GitHub：

1. 打开本地项目目录。
2. 双击 `frontend-prototype/index.html`。

这个页面本身就是静态文件，不需要服务器。
