# Plugget Qt [![PyPI](https://img.shields.io/pypi/v/plugget-qt)](https://pypi.org/project/plugget-qt/)

Plugget Qt is a UI for [plugget](https://github.com/plugget/plugget).  
Easily search, list & (un)install [plugget packages](https://github.com/plugget/plugget-pkgs).  

Plugget qt is used by:  
<img src="https://raw.githubusercontent.com/tandpfun/skill-icons/59059d9d1a2c092696dc66e00931cc1181a4ce1f/icons/Blender-Dark.svg" width="32" style="max-width: 100%;"> [Plugget Qt Blender addon](https://github.com/plugget/plugget-qt-addon)  
<img src="https://raw.githubusercontent.com/tandpfun/skill-icons/59059d9d1a2c092696dc66e00931cc1181a4ce1f/icons/UnrealEngine.svg" width="32" style="max-width: 100%;"> [Plugget Qt Unreal plugin](https://github.com/hannesdelbeke/plugget-unreal)  

## Instructions
To show the qt window:
```python
import plugget_qt
w = plugget_qt.show()  # store reference in w, to prevent garbage collection
``` 

![image](https://github.com/plugget/plugget-qt-addon/assets/3758308/0752c140-5b26-452e-81ac-fc4e36ccdb23)<br>
_Dark ui is not included, just add a qt stylesheet, e.g. [blender-qt-stylesheet](https://github.com/hannesdelbeke/blender-qt-stylesheet)_

### Installation
(depending on the app, you might want to replace python for the app's python interpreter, and maybe also use `--target "install/path/to/folder" --no-user` to install your python package to a custom folder)
```
python -m pip install plugget-qt
```

### Dependencies
- `plugget` Python module.
- `PySide2`




If this tool is helpfull, you can ⭐ star it on the github page,
just click the ⭐ star button in the top-right of this page.
