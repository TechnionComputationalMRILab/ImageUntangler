# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src\\MainWindowComponents\\MainWindow.py'],
             pathex=['C:\\Users\\ang.a\\OneDrive - Technion\\Documents\\GitHub\\ImageUntangler'],
             binaries=[],
             datas=[('src\\config', 'config'), ('src\\CSS', 'CSS')],
             hiddenimports=['vtkmodules','vtkmodules.all','vtkmodules.qt.QVTKRenderWindowInteractor','vtkmodules.util','vtkmodules.util.numpy_support'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='imageuntangler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
