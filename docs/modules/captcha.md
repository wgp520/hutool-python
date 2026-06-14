# 验证码工具 - CaptchaUtil

## 由来

图形验证码是 Web 应用中常见的安全措施。`CaptchaUtil` 基于 Pillow 提供了验证码生成功能。

## 使用

```python
from hutool import CaptchaUtil

# 创建文字验证码
captcha = CaptchaUtil.create_line_captcha(width=200, height=80, code_count=5)
code = captcha.create_code()        # 生成验证码文本
captcha.verify(code)                # True
captcha.verify("wrong")             # False

# 保存为文件
captcha.write("/path/to/captcha.png")

# 获取字节
image_bytes = captcha.get_image_bytes(format="png")
```

## 验证码类型

### 线条干扰验证码

```python
captcha = CaptchaUtil.create_line_captcha(
    width=200, height=80,
    code_count=5,     # 字符数
    line_count=50     # 干扰线条数
)
```

### 圆形干扰验证码

```python
captcha = CaptchaUtil.create_circle_captcha(
    width=200, height=80,
    code_count=5,
    circle_count=20   # 干扰圆圈数
)
```

### 扭曲验证码

```python
captcha = CaptchaUtil.create_shear_captcha(
    width=200, height=80,
    code_count=5
)
```

### 算术验证码

```python
captcha = CaptchaUtil.create_arithmetic_captcha(width=200, height=80)
code = captcha.create_code()    # 生成算式，如 "3+5=?"
result = captcha.get_result()   # 获取结果，如 "8"
```
