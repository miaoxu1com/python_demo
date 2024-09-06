放入目录自动解压存在的压缩文件
https://ezirmusitua.site/blog/package-python-application-with-pyoxidizer

C:\Users\username\AppData\Local\pyoxidizer\python_distributions
cpython-3.10.9%2B20221220-x86_64-pc-windows-msvc-shared-pgo-full.tar.zst
C:\Users\username\AppData\Local\pyoxidizer\rust
cargo-1.66.0-x86_64-pc-windows-msvc.tar.xz
rustc-1.66.0-x86_64-pc-windows-msvc.tar.xz

镜像:https://rsproxy.cn/dist/2022-12-15/cargo-1.66.0-x86_64-pc-windows-msvc.tar.xz
官网:https://static.rust-lang.org/dist/2022-12-15/cargo-1.66.0-x86_64-pc-windows-msvc.tar.xz

执行 pyoxidizer run 开始构建每次pyoxidizer 随机生成一个临时目录C:\Users\username\AppData\Local\Temp\pyoxidizer1spl1y\app
进入目录Cargo.toml目录下的.cargo目录下的config改为

[source.crates-io]
#registry = "https://github.com/rust-lang/crates.io-index"
# 指定镜像
replace-with = 'tuna' # 如：tuna、sjtu、ustc，或者 rustcc

# 中国科学技术大学
[source.ustc]
registry = "https://mirrors.ustc.edu.cn/crates.io-index"

# 上海交通大学
[source.sjtu]
registry = "https://mirrors.sjtug.sjtu.edu.cn/git/crates.io-index/"

# 清华大学
[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"

# rustcc社区
[source.rustcc]
registry = "https://code.aliyun.com/rustcc/crates.io-index.git"


def make_exe():
    dist = default_python_distribution()
    policy = dist.make_python_packaging_policy()
	#policy.resources_location = "in-memory"
    policy.resources_location_fallback = "filesystem-relative:prefix"
    python_config = dist.make_python_interpreter_config()
    python_config.run_module = "app"
    exe = dist.to_python_executable(
        name="app",
        packaging_policy=policy,
        config=python_config,
    )
    # 或者使用 requirements.txt 文件添加
    exe.add_python_resources(exe.pip_install(["-r", "requirements.txt"]))
    # 将当前目录下的 app 包作为嵌入的资源文件
    exe.add_python_resources(exe.read_package_root(
        path=".",
        packages=["common", "ui","utils"],
    ))
    return exe

def make_embedded_resources(exe):
    return exe.to_embedded_resources()

def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)
    return files

def make_msi(exe):
    return exe.to_wix_msi_builder(
        "app",
        "My Application",
        "1.0",
        "Alice Jones"
    )

def register_code_signers():
    return

register_code_signers()
register_target("exe", make_exe)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)
register_target("msi_installer", make_msi, depends=["exe"])
resolve_targets()
