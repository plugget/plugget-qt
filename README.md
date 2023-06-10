# plugget qt search
a UI widget to search [plugget packages](https://github.com/hannesdelbeke/plugget-pkgs) written in qt &amp; Python

- used by [plugget-unreal](https://github.com/hannesdelbeke/plugget-unreal) & the [plugget qt addon](https://github.com/plugget/plugget-qt-addon) for Blender
- see [plugget](https://github.com/hannesdelbeke/plugget)


![image](https://github.com/plugget/plugget-qt-addon/assets/3758308/0752c140-5b26-452e-81ac-fc4e36ccdb23)<br>
_Dark ui is not included, just add a qt stylesheet_

### Dependencies
- `plugget` Python module.
- `PySide2`

If this tool is helpfull, you can ⭐ star it on the github page,
just click the ⭐ star button in the top-right of this page.

```python
import plugget_qt
w = plugget_qt.show()  # store reference in w, to prevent garbage collection
```