# -*- mode: python ; coding: utf-8 -*-

import os
from glob import glob
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# include folders
folders = ["src", "src/app/tool"]
inc = [os.path.join(os.getcwd(), folder) for folder in folders]

# hidden imports
modules = [
    "app.tool." + os.path.basename(module)[:-3]
    for module in glob(os.path.join(os.getcwd(), "src/app/tool/*.py"))
]

a = Analysis(
    ["src/main.py"],
    pathex=folders,
    binaries=[],
    datas=[],
    hiddenimports=modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AdDrive",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="adDrive",
)
