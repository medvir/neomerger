# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['/Users/ozagordi/Dropbox/Software/neomerger'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='NeoMerger',
          icon='img/dlicon.icns',
          debug=False,
          strip=False,
          upx=True,
          console=False )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')

app = BUNDLE(exe,
             name='NeoMerger.app',
             icon='img/dlicon.icns',
             bundle_identifier=None)
