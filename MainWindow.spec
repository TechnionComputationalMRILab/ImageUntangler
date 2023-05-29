# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
                ('MRICenterline//app//config//config.ini', '.'),
                ('models//*', 'models')
             ]


a = Analysis(['main.py'],
             pathex=['Z:\\ang.a\\Code\\ImageUntangler\\ImageUntangler'],
             binaries=[],
             datas=added_files,
             hiddenimports=['configparser', 'vtkmodules','vtkmodules.all','vtkmodules.qt.QVTKRenderWindowInteractor','vtkmodules.util','vtkmodules.util.numpy_support', 'pydicom.encoders.gdcm', 'pydicom.encoders.pylibjpeg'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='ImageUntangler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='static\\favicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ImageUntangler')
