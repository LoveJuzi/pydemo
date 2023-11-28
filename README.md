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

