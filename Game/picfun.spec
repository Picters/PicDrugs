# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['PicFun.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Kira.png', '.'),  # ��������� ���� Kira.png � ������
        ('henrybaby.png', '.'),  # ��������� ���� henrybaby.png � ������
        ('fun.mp3', '.'),
        ('grab.mp3', '.'),
        ('scream.mp3', '.'),
        ('voice1.mp3', '.'),
        ('voice2.mp3', '.'),
        ('voice3.mp3', '.'),
        ('voice4.mp3', '.'),
        ('voice5.mp3', '.'),
        ('trash.png', '.'),  # ��������� ���� trash.png � ������
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
