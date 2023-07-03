## MineSweeper Python

##### 使用 Python 3.8.10 與 tkinter 實作的踩地雷遊戲
##### A MineSweeper game using Python 3.8.10 and tkinter

### 內含檔案

---

**minesweeper_ui.py**

> 程式本體

```python
{
    class GameDialog(tk.Toplevel):  #遊戲的功能介面，包含重新開始遊戲、重新設置遊戲及退出遊戲
        ...
    class GameWinDialog(GameDialog):    #遊戲勝利
        ...
    class GameOverDialog(GameDialog):   #踩到地雷，遊戲結束
        ...
    class GameConfigDialog(simpledialog.Dialog):    #設定踩地雷的寬度、高度及地雷數量
        ...
    class Minesweeper(tk.Tk):   #踩地雷主程式
        ...
}
```
