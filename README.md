# 1、搭建项目结构

```
config.py : 项目配置文件,生成诸如DEBUG = True、SQLALCHEMY_DATABASE_URI、SQLALCHEMY_TRACK_MODIFICATION = True等配置信息

exts.py :此文件用于实例化db即db = SQLALCHEMY(),防止循环导入

models.py :用于生成项目的模型文件

manage.py :项目的入口文件
```

# 2、使用Bootstrap制作导航条
## （1）Bootstrap的使用
进入到 ` https://www.bootcss.com `中引用:
```
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
```
又因为js文件要依赖jquery文件,所以进入到`http://www.bootcdn.cn/jquery/`复制`<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>`到上面的`bootstrap.min.js`前面
终上:
```
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>

<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

```
## (2)导航条的使用
在组件中找到导航条,复制相关代码,并根据实际需要进行修改

**遇到的问题**:在`static/css/index.css`文件中更改图片的样式,在浏览器中重新启动后并没有引用修改后后的样式而是继续使用修改前的样式,这是由于浏览器缓存的缘故,可以通过*CRTL+F5*刷新浏览器,也可以再浏览器中进行设置当打开开发者模式时不进行缓存.

# 3、使用基模板和模板继承
基模板的使用:将网站中各网页中相同的部分如导航栏、侧边栏等抽离出来放在`base.html`文件中,这样可以减少代码量,可以提高代码的复用.

模板的继承:使用`{% extends 'base.html' %}`继承基模板的代码,同时可以在`{% block xxx %} {% endblock %}`中自定义代码.
















