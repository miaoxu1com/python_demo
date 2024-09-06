放入目录自动解压存在的压缩文件
C:\Users\username\AppData\Local\pyoxidizer\python_distributions
cpython-3.10.9%2B20221220-x86_64-pc-windows-msvc-shared-pgo-full.tar.zst
C:\Users\username\AppData\Local\pyoxidizer\rust
cargo-1.66.0-x86_64-pc-windows-msvc.tar.xz
rustc-1.66.0-x86_64-pc-windows-msvc.tar.xz

镜像:https://rsproxy.cn/dist/2022-12-15/cargo-1.66.0-x86_64-pc-windows-msvc.tar.xz
官网:https://static.rust-lang.org/dist/2022-12-15/cargo-1.66.0-x86_64-pc-windows-msvc.tar.xz

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
