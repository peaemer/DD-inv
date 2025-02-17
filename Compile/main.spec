# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\alex\\PycharmProjects\\DD-inv\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\alex\\PycharmProjects\\DD-inv\\includes', 'includes/'), ('C:\\Users\\alex\\PycharmProjects\\DD-inv\\cache.py', '.')],
    hiddenimports=['sqlite3', 'tkinter', 'customtkinter', 'pillow', 'CTkListbox'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\alex\\PycharmProjects\\DD-inv\\includes\\assets\\srhIcon.ico'],
)
