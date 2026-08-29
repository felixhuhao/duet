# ByteMe Mobile · 新 MacBook Air 三端环境安装指南

> 更新日期：2026-08-20（Asia/Shanghai）
>
> 文档归属：个人开发机 bootstrap；项目内的实时工具链、验证与发布契约仍以 `byteme_mobile` 仓为准。
>
> 适用范围：Apple Silicon MacBook Air，从空机器开始搭建 `byteme_mobile` 的 iOS、Android、
> HarmonyOS emulator/simulator 与本地测试环境。
>
> 历史版本选择依据保留在
> `byteme_mobile/docs/devlogs/2026-08-20-三端本地环境与版本基线调研.md`。已经完成安装后的日常命令只认
> `byteme_mobile/docs/dev/本地开发测试说明.md`；HarmonyOS 详细签名与排障只认
> `byteme_mobile/docs/dev/HarmonyOS本地测试手册.md`。

本文只负责**首次安装与环境资格确认**，不定义每个 Goal、Integration window 或 Release 的必跑平台。
三端产品范围、工具链与验证分层只认
`byteme_mobile/docs/dev/本地开发测试说明.md` §1。

本指南只安装 Mobile v2 需要的环境。**不安装 Java 老后端、MySQL、Redis、`/compat` 代理或
Desktop 工具链。**文中的 JDK 是 Android/DevEco 构建运行时，不代表重新依赖 Java 后端。

---

## 0. 开始前确认

### 0.1 机器与磁盘

- Apple Silicon：M 系列芯片；
- macOS：仓库已验证 Xcode 26.6，参考系统为 macOS Tahoe 26.6；
- 内存：16 GB 可以使用；Android reference 可在连续 Integration window 内复用，iOS 只在平台专项时启动，
  OHOS emulator 必须显式按需启动并在 finalize 后关闭；不要让三端模拟器同时常驻；
- 磁盘：建议开始前至少空出 180 GB。Xcode + 两个 iOS runtime、Android SDK/三个 image、
  DevEco + Pura 90 都会占用大量空间；
- 网络：需要访问 Apple、Google Maven/SDK、GitCode、pub.dev、华为开发者站和公司 Gitea。

查看机器信息：

```sh
uname -m
sw_vers
df -h /
```

成功标准：

- `uname -m` 输出 `arm64`；
- 系统盘剩余空间满足上述要求；
- 系统更新已经完成，重启后再继续。

### 0.2 准备账号

在安装前确认能够登录：

1. 公司 Gitea：读取 `develop/byteme_mobile`；
2. Apple ID：下载 Xcode 与 Simulator Runtime；
3. 华为开发者账号：能够为 `com.dagong.byteme` 生成调试签名；
4. 如需 iOS 真机，再准备 Apple Developer team；仅 Simulator 不需要；
5. Agent 测试地址：默认使用
   `https://test-dagong-agent.byteme.chat/agent/api`，不要准备 Java `/api/v2` 地址或省略
   `/agent` 部署前缀。

---

## 1. 安装系统基础工具

### 1.1 安装 Rosetta 2

当前 OHOS Flutter fork 的 host `impellerc` 仍是 x86_64。即使三端模拟器都是 ARM64，
Apple Silicon 上执行 `./tool/flutterw run` 仍需要 Rosetta。

```sh
sudo softwareupdate --install-rosetta --agree-to-license
```

系统会要求输入当前 Mac 管理员密码。完成后验证：

```sh
/usr/sbin/pkgutil --pkg-info com.apple.pkg.RosettaUpdateAuto
```

成功标准：输出 Rosetta package 信息，而不是 `No receipt`。

### 1.2 安装 Xcode Command Line Tools

```sh
xcode-select --install
```

如果系统提示已经安装，可直接继续。验证：

```sh
git --version
xcrun --version
```

### 1.3 安装 Homebrew

从 [brew.sh](https://brew.sh/) 使用其当前给出的 Apple Silicon 安装命令。安装器结束后，按它打印的
提示把 `/opt/homebrew/bin` 加入 `~/.zprofile`，然后重新打开终端。

验证：

```sh
brew --version
brew doctor
```

`brew doctor` 的第三方软件提示不一定阻塞；`brew` 命令不存在则不要继续。

### 1.4 安装本仓需要的命令行依赖

```sh
brew install openjdk@17 cocoapods
```

验证：

```sh
export BYTEME_JDK17_HOME="$(brew --prefix openjdk@17)/libexec/openjdk.jdk/Contents/Home"
"$BYTEME_JDK17_HOME/bin/java" -version
pod --version
```

期望：

- Java 主版本为 17；
- CocoaPods 为 1.17.x；当前 `Podfile.lock` 由 1.17.0 生成。

不要把 `JAVA_HOME` 永久全局指向 Android Studio 或 DevEco 的 JBR。后文会分别为 Android 和
HarmonyOS 选择运行时，避免两个 IDE 升级后互相污染。

---

## 2. 取得正确的 Mobile 源码

### 2.1 先向 integration owner 要冻结 SHA

历史复核基线 `origin/v2@88d66246` 已包含当日 Java cutoff 与 Desktop 拆分；2026-08-25 起正式开发主线
已提升为 `main`。不要只问“是不是 main”；必须向 integration owner
取得一个完整的、干净的 **40 位 commit SHA**。下面将它写成 `<OWNER_PROVIDED_SHA>`。

### 2.2 建立工作区并 clone

```sh
mkdir -p "$HOME/Workspace"
cd "$HOME/Workspace"

git clone https://gitea-dg.byteme.chat/develop/byteme_mobile.git byteme_mobile
cd byteme_mobile
git fetch origin --tags
git checkout main
git checkout --detach <OWNER_PROVIDED_SHA>
```

比较 SHA：

```sh
git rev-parse HEAD
git status --short
```

成功标准：

- `git rev-parse HEAD` 与 owner 给出的 40 位 SHA 完全一致；
- `git status --short` 无输出。

如果 SHA 不一致，**在这里停止**。先重新 `git fetch origin`；如果仍找不到该 commit，
让 owner 确认已 push 的远端位置，或给你一个 `git bundle`。不要基于其他时间线的源码
继续安装并记录“三端通过”。

---

## 3. 安装唯一允许使用的 Flutter SDK

### 3.1 clone OHOS fork 的稳定 tag

```sh
mkdir -p "$HOME/Workspace/tools"
cd "$HOME/Workspace/tools"

git clone \
  --depth 1 \
  --branch 3.41.10-ohos-1.0.0 \
  https://gitcode.com/CPF-Flutter/flutter_flutter.git \
  flutter-ohos-3.41.10
```

该目录只是安装示例，不是 wrapper 的机器级规范。无论 SDK 安装在哪，都应在运行仓库工具前显式设置：

```sh
export BYTEME_FLUTTER_ROOT=/absolute/path/to/flutter-ohos-3.41.10
```

验证 tag 与 OHOS 枚举：

```sh
cd "$HOME/Workspace/tools/flutter-ohos-3.41.10"
git tag --points-at HEAD
test "$(git rev-parse HEAD)" = "244a0e8abb3085e8675589b13e219af8c41cb7aa"
grep -q '^[[:space:]]*ohos,' packages/flutter/lib/src/foundation/platform.dart
```

成功标准：

- 第一条输出 `3.41.10-ohos-1.0.0`；
- 后两条静默返回成功。

如果 Flutter 后面显示版本 `0.0.0`，通常是浅克隆没有拿到 tag。修复：

```sh
git fetch origin tag 3.41.10-ohos-1.0.0 --no-tags
git checkout 3.41.10-ohos-1.0.0
```

### 3.2 创建日常分析用 OHOS stub

这个 stub 只让 OHOS fork 在 pub/analyze/unit test 时通过路径检查，不包含真实 SDK，也绝不能用于
HAP 或 OHOS run。

```sh
mkdir -p "$HOME/Workspace/tools/hos-sdk-stub/openharmony"
mkdir -p "$HOME/Workspace/tools/hos-sdk-stub/hmscore"
```

### 3.3 从仓库 wrapper 验证 Flutter

```sh
cd "$HOME/Workspace/byteme_mobile"
./tool/flutterw --version
```

期望看到：

```text
Flutter 3.41.10-ohos-1.0.0
Dart 3.11.5
```

不要用 PATH 中的 `flutter` 或 `dart` 代替 wrapper。`TargetPlatform.ohos` 只有这个 fork 存在，
官方 Flutter 会让三端共同代码直接编译失败。

### 3.4 先固定 Android JDK

```sh
export BYTEME_JDK17_HOME="$(brew --prefix openjdk@17)/libexec/openjdk.jdk/Contents/Home"

./tool/flutterw config --jdk-dir "$BYTEME_JDK17_HOME"
```

Android SDK 尚未安装，SDK 路径到 §6 再固定；这里不执行一个注定找不到目录的命令。

### 3.5 拉取 Flutter/Dart 依赖

如果 `~/.zprofile` 里设置过国内 pub 镜像，先删除或在当前终端取消：

```sh
unset PUB_HOSTED_URL
cd "$HOME/Workspace/byteme_mobile"
./tool/flutterw pub get
```

成功标准：

- 命令 rc=0；
- `.dart_tool/package_config.json` 存在；
- 没有 `advisories` 元数据错误。

若出现 `pub.flutter-io.cn` advisories 错误，说明镜像变量仍从 shell 配置中重新注入，修正
`~/.zprofile` 后开新终端重试。

---

## 4. 先跑不依赖 emulator 的基础门禁

这一步先证明源码、fork、pub 与 JDK 没问题，避免装完三个 IDE 才发现仓库 SHA 或 SDK 错了。

```sh
cd "$HOME/Workspace/byteme_mobile"

./tool/flutterw analyze lib test --no-pub
./tool/testw test/core/constants/mobile_agent_config_test.dart
```

成功标准：

- analyze 没有 error，也没有相对仓库基线新增 warning；
- 定向测试通过；
- 没有泄漏的 `flutter_tester` 或 120 秒墙钟超时。

`./tool/testw --full` 只能在 primary worktree 的 clean `main` 上运行。新 clone 若正好是 owner
给出的 frozen SHA，可以在全部环境装完后运行一次；不要在有文档或代码改动的工作树强跑。

---

## 5. 安装并打通 iOS Simulator（优先级 1）

### 5.1 安装 Xcode 26.6

从 Mac App Store 或 Apple Developer Downloads 安装稳定版 Xcode 26.6，放在：

```text
/Applications/Xcode.app
```

安装后执行：

```sh
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -license accept
sudo xcodebuild -runFirstLaunch
xcodebuild -version
xcode-select -p
```

期望：

```text
Xcode 26.6
/Applications/Xcode.app/Contents/Developer
```

### 5.2 下载两个 iOS runtime

打开 Xcode：

1. `Xcode → Settings → Components`；
2. 安装 iOS 26 runtime；
3. 安装 iOS 18 runtime，用来覆盖建议的最低系统版本；
4. 等两个下载都完成，再打开设备管理器。

如果 Components 不显示 iOS 18，使用 Apple 官方 Additional Simulator Runtimes 下载与
Xcode 26 兼容的版本；不要从非 Apple 来源下载 runtime。

### 5.3 创建两台 Simulator

打开 `Xcode → Window → Devices and Simulators → Simulators`：

1. 点击左下角 `+`；
2. 创建 `ByteMe-iOS18`，选择一个普通 iPhone 机型和 iOS 18；
3. 再创建 `ByteMe-iOS26`，选择当前主流 iPhone 和 iOS 26；
4. 先只启动 `ByteMe-iOS18`。

验证：

```sh
xcrun simctl list devices available
cd "$HOME/Workspace/byteme_mobile"
./tool/flutterw devices
```

两条命令都应列出已启动的 Simulator。

### 5.4 安装 Pods

```sh
cd "$HOME/Workspace/byteme_mobile/ios"
./install_pods.sh
cd ..
```

成功标准：

- `pod install` 成功；
- 没有全局排除 Apple Silicon `arm64`；
- `ios/Runner.xcworkspace` 存在。

如果 Specs 过旧导致找不到 Pod：

```sh
pod repo update
cd "$HOME/Workspace/byteme_mobile/ios"
./install_pods.sh
```

### 5.5 第一次运行 iOS

先从 `./tool/flutterw devices` 复制 Simulator device id，然后执行：

```sh
cd "$HOME/Workspace/byteme_mobile"

./tool/flutterw run -d <IOS_SIMULATOR_ID> \
  --dart-define=API_BASE_URL=https://test-dagong-agent.byteme.chat/agent/api \
  --dart-define=AGENT_WEB_BASE_URL=https://test-dagong-agent.byteme.chat/agent \
  --dart-define=APP_BUILD_TARGET=ios \
  --dart-define=APP_GIT_COMMIT=$(git rev-parse --short HEAD)
```

成功标准：

- App 编译、安装并打开；
- 终端进入 Flutter 调试会话；
- 启动没有尝试访问 Java `/api/v2` 或 `/compat`；
- 登录前页面、基本导航和网络错误态可见。

按 `q` 退出。随后关闭 iOS 18 Simulator，再启动 iOS 26，重复一次。不要同时开两台。

---

## 6. 安装并打通 Android Emulator（优先级 2）

### 6.1 安装 Android Studio 2026.1 stable

从 [Android Studio 官方下载页](https://developer.android.com/studio) 下载 macOS ARM64 稳定版，
将应用拖入 `/Applications`。首次启动选择 Standard setup 即可，但后面仍要手工补齐版本。

不要用 Android Studio 自带 JBR 25 运行本仓 Gradle；本仓继续固定 §1 安装的 JDK 17。

### 6.2 安装 Android SDK 组件

打开 Android Studio：

1. `More Actions → SDK Manager`；
2. `SDK Platforms` 勾选 `Android 16 / API 36`；
3. 勾选 `Show Package Details`；
4. 需要最低线时同时准备 API 29，API 34 作为中间回归；
5. 在 `SDK Tools` 勾选：
   - Android SDK Build-Tools 36；
   - Android SDK Platform-Tools；
   - Android SDK Command-line Tools (latest)；
   - Android Emulator；
   - NDK (Side by side) `28.2.13676358`；
6. 点击 Apply，接受 license，等下载完成。

长期 16 KB 修复会另升 NDK r28+；首次复现当前仓库仍先装 r27，不在环境搭建时擅自改项目配置。

### 6.3 固定 SDK/JDK 并接受 license

```sh
cd "$HOME/Workspace/byteme_mobile"
export BYTEME_JDK17_HOME="$(brew --prefix openjdk@17)/libexec/openjdk.jdk/Contents/Home"
export BYTEME_ANDROID_SDK="$HOME/Library/Android/sdk"

./tool/flutterw config --jdk-dir "$BYTEME_JDK17_HOME"
./tool/flutterw config --android-sdk "$BYTEME_ANDROID_SDK"

JAVA_HOME="$BYTEME_JDK17_HOME" \
  "$BYTEME_ANDROID_SDK/cmdline-tools/latest/bin/sdkmanager" --licenses
```

逐项输入 `y` 接受 Android license。然后验证：

```sh
./tool/flutterw doctor -v
test -f "$BYTEME_ANDROID_SDK/platforms/android-36/android.jar"
test -x "$BYTEME_ANDROID_SDK/platform-tools/adb"
test -d "$BYTEME_ANDROID_SDK/ndk/28.2.13676358"
```

Android toolchain 不应再报缺 SDK/JDK；HarmonyOS stub 相关提示此时可忽略。

### 6.4 创建 ARM64 AVD

打开 `Android Studio → Tools → Device Manager`：

1. 点击 `Create device`；
2. 选择一台普通 Pixel 手机；
3. 在 system image 中选择 **ARM64 / arm64-v8a**；
4. 依次创建：
   - `ByteMe-API29-arm64`；
   - `ByteMe-API34-arm64`；
   - `ByteMe-API36-arm64`；
5. 每台建议保留默认内存，不为了速度给三台同时分配大量 RAM；
6. 先只启动 API 29。

如果旧 API 29 image 默认不显示，勾选 `Show Package Details` 或在 Device Manager 的 image
列表中切到其他 images；只使用 Google/Android 官方 ARM64 image。

### 6.5 验证设备并第一次运行

```sh
export BYTEME_ADB="$HOME/Library/Android/sdk/platform-tools/adb"
"$BYTEME_ADB" devices

cd "$HOME/Workspace/byteme_mobile"
./tool/flutterw devices
```

记下类似 `emulator-5554` 的 id，然后执行：

```sh
./tool/flutterw run -d <ANDROID_EMULATOR_ID> \
  --dart-define=API_BASE_URL=https://test-dagong-agent.byteme.chat/agent/api \
  --dart-define=AGENT_WEB_BASE_URL=https://test-dagong-agent.byteme.chat/agent \
  --dart-define=APP_BUILD_TARGET=android \
  --dart-define=APP_GIT_COMMIT=$(git rev-parse --short HEAD)
```

成功标准同 iOS：build、install、launch、调试会话都成功，且网络只走 Agent。

按 `q` 退出并关闭 API 29。至少再在 API 36 重复一次；API 34 用于发布前中间版本回归。

### 6.6 预留 16 KB emulator

首次搭建完成后，在 SDK Manager/Device Manager 另下载 Android 15 或 Android 16 的官方
**16 KB page size ARM64** image。它不是日常主 emulator，但必须在扫码/ML Kit 修复批次使用。

当前 APK 中 `libimage_processing_util_jni.so` 仍为 4 KB ELF 对齐，所以在修复前失败是已知事实，
不能通过换普通 4 KB emulator 隐藏。完整证据见版本基线调研报告 §7。

---

## 7. 安装并打通 HarmonyOS Emulator（优先级 3）

### 7.1 安装 DevEco Studio 6.1.1

从[华为 DevEco Studio 官方页面](https://developer.huawei.com/consumer/cn/deveco-studio/)进入资源/
历史版本，下载 macOS ARM 版 DevEco Studio 6.1.1。不要选择 `26.0.0 Beta`。

把 App 放到：

```text
/Applications/DevEco-Studio.app
```

首次启动按 Setup Wizard 安装默认工具。随后在 DevEco 的 SDK Manager 确认：

- HarmonyOS SDK 6.1.1 / API 24；
- OpenHarmony toolchains，包含 hdc；
- hvigor 与 ohpm；
- 本地 Emulator 工具。

### 7.2 验证 DevEco 目录

新开终端，复制整段：

```sh
export BYTEME_DEVECO_HOME=/Applications/DevEco-Studio.app/Contents
export HOS_SDK_HOME="$BYTEME_DEVECO_HOME/sdk"
export DEVECO_SDK_HOME="$HOS_SDK_HOME"
export JAVA_HOME="$BYTEME_DEVECO_HOME/jbr/Contents/Home"
export PATH="$JAVA_HOME/bin:$BYTEME_DEVECO_HOME/tools/hvigor/bin:$BYTEME_DEVECO_HOME/tools/ohpm/bin:$PATH"
export BYTEME_OHOS_HDC="$HOS_SDK_HOME/default/openharmony/toolchains/hdc"

test -d "$HOS_SDK_HOME/default/openharmony"
test -x "$BYTEME_OHOS_HDC"
test -x "$BYTEME_DEVECO_HOME/tools/hvigor/bin/hvigorw"
test -x "$BYTEME_DEVECO_HOME/tools/ohpm/bin/ohpm"
test -x "$JAVA_HOME/bin/java"
```

全部静默成功才继续。注意：

- `HOS_SDK_HOME` 指向 `Contents/sdk`；
- 不指向 `sdk/default` 或 `sdk/default/openharmony`；
- hdc 在 SDK 的 `toolchains/hdc`，不在 DevEco `tools/hdc/bin`；
- 这组 `JAVA_HOME` 只用于当前 OHOS 终端。

### 7.3 创建 Pura 90 ARM64 emulator

在 DevEco Studio 打开 Device Manager：

1. 新建 Local Emulator；
2. 选择手机设备 Pura 90；
3. 选择 HarmonyOS 6.1.1 / API 24；
4. 选择 ARM64 image；
5. RAM 选择 2 GB，storage 保持 6 GB；
6. 命名为 `ByteMe-Pura90-API24`；
7. 等 image 完整下载与部署；
8. 从 Device Manager 启动，等到系统桌面完全出现。

不要直接双击 DevEco 安装目录中的 Emulator 二进制；Device Manager 才会带上实例、镜像和连接参数。

### 7.4 让 hdc 和 Flutter 看到设备

保持 §7.2 的环境变量仍在当前终端：

```sh
"$BYTEME_OHOS_HDC" list targets -v
cd "$HOME/Workspace/byteme_mobile"
./tool/flutterw devices
```

成功标准：

- hdc 输出设备 transport id，而不是 `[Empty]`；
- Flutter 列表中同一个设备的平台是 OHOS。

把 transport id 保存到当前终端：

```sh
export BYTEME_OHOS_DEVICE_ID='<复制 hdc 输出的 transport id>'
```

### 7.5 生成并安全提取调试签名

`./tool/flutterw run` 到 OHOS 强制签名。按下面顺序操作：

1. 用 DevEco Studio 打开 `~/Workspace/byteme_mobile/ohos/`；
2. 登录华为开发者账号；
3. 打开 `File → Project Structure → Signing Configs`；
4. 选择 debug，勾选 `Automatically generate signature`；
5. 等 DevEco 写入完成；
6. **不要执行 git add，不要提交 `ohos/build-profile.json5`**；
7. 立刻回到仓库根执行：

```sh
cd "$HOME/Workspace/byteme_mobile"
./tool/ohos-signing-extract
git status --porcelain ohos/build-profile.json5
test -f ohos/signing.local.json
./tool/ohos-signing-status --device-id "$BYTEME_OHOS_DEVICE_ID"
```

成功标准：

- `build-profile.json5` 的 status 无输出；
- `ohos/signing.local.json` 存在且未被 Git 跟踪；
- 状态工具输出 `deviceReadiness: READY_FOR_RUN`；
- bundle 是 `com.dagong.byteme`，profile 未过期且包含当前设备。

调试 profile 通常只有 14 天有效期。过期或换设备后重新执行本节，不要手填 DevEco 加密密码。

### 7.6 第一次构建、签名和运行

先做 unsigned build，将工具链问题和签名问题分开：

```sh
cd "$HOME/Workspace/byteme_mobile"

HOS_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk \
  ./tool/flutterw build hap --debug --no-codesign \
  --dart-define=APP_BUILD_TARGET=ohos \
  --dart-define=APP_GIT_COMMIT=$(git rev-parse --short HEAD)
```

成功后再运行到 Pura 90：

```sh
HOS_SDK_HOME=/Applications/DevEco-Studio.app/Contents/sdk \
  ./tool/flutterw run -d "$BYTEME_OHOS_DEVICE_ID" \
  --dart-define=API_BASE_URL=https://test-dagong-agent.byteme.chat/agent/api \
  --dart-define=AGENT_WEB_BASE_URL=https://test-dagong-agent.byteme.chat/agent \
  --dart-define=APP_BUILD_TARGET=ohos \
  --dart-define=APP_GIT_COMMIT=$(git rev-parse --short HEAD)
```

成功标准：signed HAP 构建、安装、App 启动、终端进入调试会话。失败时严格按
`byteme_mobile/docs/dev/HarmonyOS本地测试手册.md` 从 hdc/签名逐层排查。

### 7.7 补最低线 API 20 证据

Pura 90 API 24 只验证当前上界。要把 `compatibleSdkVersion` 从 17 提到建议的 API 20，必须另找：

- HarmonyOS 6.0 / API 20 物理设备；或
- 华为官方云测中的 API 20 设备。

在 API 20 上至少验证安装、启动、登录、Agent 网络、扫码/权限相关入口和本次发布主流程，并记录
设备、系统版本、commit 和日期。没有这份证据时不要提前修改 `compatibleSdkVersion`。

---

## 8. 新机器的三端环境资格验收

这是新机器/新工具链的一次性资格确认，不是每个 Goal 或每次 Release 的固定矩阵。准备哪个目标就验证
哪个目标；日常 Integration 仍由 Registry 的显式 profile/environment 决定。多个目标都已安装时，
每次只启动一台，建议按下面顺序执行：

| 顺序 | 设备 | 必做 |
|---|---|---|
| 1 | iOS 18 Simulator | build/run、启动、登录入口、主导航、Agent 错误态 |
| 2 | iOS 26 Simulator | 当前系统 build/run 与关键页面 |
| 3 | Android API 29 ARM64 | 最低线 build/run 与关键页面 |
| 4 | Android API 36 ARM64 | 当前 target 行为与关键页面 |
| 5 | Pura 90 API 24 ARM64 | signed HAP、安装、启动、主流程 |
| 6 | HarmonyOS API 20 真机/云测 | compatible 最低线证据，配置调整前必做 |

运行前先确认 Agent health 与 auth POST 都直达正确部署路径。该探针发送空 JSON，不含手机号，
不会触发短信：

```sh
./tool/release-environment-preflight \
  --api-base https://test-dagong-agent.byteme.chat/agent/api
```

如果 health 失败，记录为环境不可用，不要切到 Java 继续测试。

每端人工检查：

- [ ] App 能启动，不白屏、不立即崩溃；
- [ ] `APP_BUILD_TARGET` 与 runtime 一致；
- [ ] 网络只访问 Agent `/api`；
- [ ] 登录入口和主导航可达；
- [ ] 经营/门户保持产品红线；
- [ ] 支付入口选择正确平台并能安全 fail closed；
- [ ] 弱网、401、后端不可用时不回退 Java；
- [ ] 记录 commit、设备、OS、日期与结果。

Emulator 通过不代表原生能力已验收。StoreKit、支付宝/微信、推送、相机扫码、录音、权限、文件选择
和 WebView 最终仍需物理真机与真实渠道。

---

## 9. 自动化验证

### 9.1 每台新 Mac 的基础验证

```sh
cd "$HOME/Workspace/byteme_mobile"

./tool/flutterw --version
./tool/flutterw analyze lib test --no-pub
./tool/testw test/core/constants/mobile_agent_config_test.dart
```

### 9.2 clean integration SHA 的全量门禁

确认是 primary worktree、分支为 `main`、`git status --short` 无输出后：

```sh
./tool/testw --full
```

不要直接执行 `flutter test`，也不要用官方 `dart` 跑 build_runner。

### 9.3 当前 smoke 口径

Java cutoff 已并入 `origin/main`，其中删除了依赖 Java payment/points model 的旧
`integration_test/app_smoke_test.dart`。新 Mac 不要尝试恢复它，也不要照抄旧手册中对该文件的
命令。Agent-only smoke 补齐前，以 unit/widget/HTTP mock、三端实际启动和真机 checklist
分别记录证据。

---

## 10. 明确不要安装的东西

- Java 老后端仓及其服务；
- 老后端 MySQL、Redis、本地容器编排；
- `/api/v2`、`/compat` 或 Java fallback proxy；
- Desktop/macOS/Windows/Linux Mobile 构建环境；
- 官方 Flutter SDK；
- `26.0.0 Beta` DevEco/HarmonyOS 工具线；
- 任何非 `3.41.10-ohos-1.0.0` @ `244a0e8abb3085e8675589b13e219af8c41cb7aa` 的
  Flutter fork、branch 或 canary；
- 为了兼容旧真机额外安装 32 位 Android toolchain。

保留的 Java 运行时只有：

- OpenJDK 17：Android Gradle；
- DevEco bundled JBR：OHOS hvigor/ohpm/签名。

---

## 11. 常见失败按这个顺序查

| 现象 | 先查 | 处理 |
|---|---|---|
| wrapper 拒绝 Flutter identity | tag 与 `git rev-parse HEAD` 是否同时命中 | 重新 fetch/checkout `3.41.10-ohos-1.0.0`，核对 exact source `244a0e8a…` |
| `impellerc` 架构错误 | Rosetta receipt | 重装 Rosetta，不用换 Flutter beta |
| pub advisories 报错 | `PUB_HOSTED_URL` | 移除 `pub.flutter-io.cn`，使用官方源 |
| wrapper 找不到 SDK | `BYTEME_FLUTTER_ROOT` 是否指向正确 fork | 显式 export SDK 绝对路径，不要为迁就相邻目录假设移动仓库 |
| sdkmanager 要求 JDK | 实际 `java -version` | 用 `BYTEME_JDK17_HOME` 单次注入，不用系统 JDK |
| Android 缺 `android.jar` | platform 安装是否残缺 | SDK Manager 重装对应 Platform，不只建空目录 |
| Android emulator 很慢/崩 | 是否同时开多台 | 关闭 iOS/OHOS，只留一个 ARM64 AVD |
| iOS Pod 不支持 arm64 | 是否有旧全局 `EXCLUDED_ARCHS` | 使用仓库 `install_pods.sh`，不要恢复全局排除 |
| hdc `[Empty]` | Pura 是否从 Device Manager 启动到桌面 | 先修 emulator/hdc，不查 Flutter |
| hdc 有设备、Flutter 没有 | `HOS_SDK_HOME` | 指向 `DevEco-Studio.app/Contents/sdk` 后重试 |
| OHOS run 无签名 | `ohos-signing-status` | 恢复本地注入、检查过期与 UDID |
| App 拒绝 API URL | 是否是 Java/compat/非 HTTPS | 只传 Agent HTTPS `/api` 地址 |
| 16 KB emulator 扫码失败 | APK 中 ML Kit `.so` | 这是已知阻断，升级 scanner 后重新验 ELF |

排障原则：先证明上一层已经成功，再查下一层；不要同时修改 Flutter、JDK、SDK、签名和业务代码。

---

## 12. 安装完成清单

- [ ] owner 提供的 frozen SHA 与本机 `HEAD` 一致；
- [ ] `git status --short` 干净；
- [ ] Rosetta 已安装；
- [ ] Flutter `3.41.10-ohos-1.0.0` / Dart 3.11.5 / exact source `244a0e8abb3085e8675589b13e219af8c41cb7aa`；
- [ ] OHOS stub 存在，且没有被用于 HAP/run；
- [ ] OpenJDK 17 已固定给 Android；
- [ ] Xcode 26.6、iOS 18/26 Simulator 可运行；
- [ ] CocoaPods 1.17.x、`install_pods.sh` 成功；
- [ ] Android SDK/target 36、NDK `28.2.13676358`、API 29/34/36 ARM64 AVD 已准备；
- [ ] DevEco 6.1.1、SDK API 24、Pura 90 ARM64 已准备；
- [ ] OHOS 签名状态为 `READY_FOR_RUN`；
- [ ] analyze 与定向测试通过；
- [ ] iOS 18/26、Android 29/36、OHOS 24 均完成 build/run；
- [ ] API 20 真机/云测已预约或完成，未用 API 24 结果冒充；
- [ ] 三端均只访问 Agent，不存在 Java fallback；
- [ ] 真支付、推送、扫码、录音、权限与 WebView 的物理真机验收另有记录。
