# 1、搭建项目结构
```
config.py : 项目配置文件,生成诸如DEBUG = True、SQLALCHEMY_DATABASE_URI、SQLALCHEMY_TRACK_MODIFICATION = True等配置信息

exts.py :此文件用于实例化db即db = SQLALCHEMY(),防止循环导入

models.py :用于生成项目的模型文件

manage.py :项目的入口文件
```
