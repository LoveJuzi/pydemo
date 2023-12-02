# pydemo

## 运行 'runevn.sh'

'runenv.sh' 用于配置 pydemo 的运行环境，需要使用如下代码运行：

`source runenv.sh`

## glVertexAttribPointer error

这个错误需要设置两个环境变量，这两个变量我们可以写入到".bashrc"文件中

```bash
export LIBGL_ALWAYS_SOFTWARE=1
export PYOPENGL_PLATFORM=x11
```

## PyGLM

通常建议使用 numpy 库，但是，为了学习的方便我们可以使用 PyGLM 库

``` sh
pip install PyGLM
```

## 阿里云镜像

设置镜像方便下载库

``` sh
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

使用如下指令用来恢复默认的镜像源

``` sh
pip config unset global.index-url
```

