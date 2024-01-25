# Plugget Qt [![PyPI](https://img.shields.io/pypi/v/plugget-qt)](https://pypi.org/project/plugget-qt/)

Plugget Qt is a UI for [plugget](https://github.com/plugget/plugget).  
Easily search, list & (un)install [plugget packages](https://github.com/plugget/plugget-pkgs).  

Plugget qt is used by:  
<img src="https://raw.githubusercontent.com/tandpfun/skill-icons/59059d9d1a2c092696dc66e00931cc1181a4ce1f/icons/Blender-Dark.svg" width="32" style="max-width: 100%;"> [Plugget Qt Blender addon](https://github.com/plugget/plugget-qt-addon)  
<img src="https://raw.githubusercontent.com/tandpfun/skill-icons/59059d9d1a2c092696dc66e00931cc1181a4ce1f/icons/UnrealEngine.svg" width="32" style="max-width: 100%;"> [Plugget Qt Unreal plugin](https://github.com/hannesdelbeke/plugget-unreal)  
- [plugget-qt-maya-plugin](https://github.com/plugget/plugget-qt-maya-plugin) A Maya plugin that launches the Plugget Qt UI window
- [plugget qt substance painter](https://github.com/plugget/plugget-substance-painter-plugin)


## Instructions
To show the qt window:
```python
import plugget_qt
w = plugget_qt.show()  # store reference in w, to prevent garbage collection
``` 

![image](https://github.com/plugget/plugget-qt/assets/3758308/86cc7019-fb8b-4b6f-b2a9-e57ff82bdd62)  
_Dark ui is not included, just add a qt stylesheet, e.g. [blender-qt-stylesheet](https://github.com/hannesdelbeke/blender-qt-stylesheet)_

### Installation
(depending on the app, you might want to replace python for the app's python interpreter, and maybe also use `--target "install/path/to/folder" --no-user` to install your python package to a custom folder)
```
python -m pip install plugget-qt
```

### Dependencies
- [plugget](https://github.com/plugget/plugget) (Apache 2.0) Python module.
- [qtpy](https://pypi.org/project/QtPy/) (MIT) Qt wrapper for PySide & PyQt




If this tool is helpfull, you can ⭐ star it on the github page,
just click the ⭐ star button in the top-right of this page.
