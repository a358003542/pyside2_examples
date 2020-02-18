# timer

## UPDATE LOG
### 1.2.2
优化
### 1.2.1
代码整理

### 1.2.0
- 新增查看运行时日志功能 【任何成熟的软件都应该有一个完备的运行时日志查看功能】
- 新增运行记录自动保存功能 【防止程序意外终止】


## 制作
### 更新翻译
```text
pyside2-lupdate timer.pro 
```

### 更新资源
```text
pyside2-rcc timer.qrc -o timer_rc.py
```

```text
pyinstaller timer.spec
```