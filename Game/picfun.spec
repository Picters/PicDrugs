# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['PicFun.py'],
    pathex=['.'],  # Assuming the spec file is in the root directory of the project
    binaries=[],
    datas=[
        ('characters/Kira.png', 'characters'),
        ('sfx/fun.mp3', 'sfx'),
        ('sfx/grab.mp3', 'sfx'),
        ('sfx/scream.mp3', 'sfx'),
        ('sfx/voice1.mp3', 'sfx'),
        ('sfx/voice2.mp3', 'sfx'),
        ('sfx/voice3.mp3', 'sfx'),
        ('sfx/voice4.mp3', 'sfx'),
        ('sfx/voice5.mp3', 'sfx'),
        ('sfx/voiserubka.mp3', 'sfx'),
        ('images/trash.png', 'images'),
        ('images/arrow.png', 'images'),
        ('images/rubka.png', 'images'),
    ],
    hiddenimports=[],
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
    name='picfun',
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
)