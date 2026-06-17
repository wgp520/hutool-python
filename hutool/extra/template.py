"""模板工具类，基于jinja2"""

import os
from typing import Optional

from jinja2 import BaseLoader, Environment, FileSystemLoader, StrictUndefined


class TemplateUtil:
    """模板工具类，基于jinja2"""

    @staticmethod
    def render(template_str: str, context: Optional[dict] = None) -> str:
        """渲染模板字符串

        :param template_str: 模板字符串
        :param context: 上下文变量字典
        :return: 渲染后的字符串
        """
        if context is None:
            context = {}
        env = Environment(loader=BaseLoader(), undefined=StrictUndefined)
        template = env.from_string(template_str)
        return template.render(**context)

    @staticmethod
    def render_file(template_path: str, context: Optional[dict] = None) -> str:
        """渲染模板文件

        :param template_path: 模板文件路径
        :param context: 上下文变量字典
        :return: 渲染后的字符串
        """
        if context is None:
            context = {}
        template_path = os.path.abspath(template_path)
        template_dir = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        env = Environment(loader=FileSystemLoader(template_dir), undefined=StrictUndefined)
        template = env.get_template(template_name)
        return template.render(**context)

    @staticmethod
    def render_template(template_path: str, context: Optional[dict] = None) -> str:
        """渲染模板文件（``render_file`` 别名，与 hutoolpy 兼容）。

        :param template_path: 模板文件路径
        :param context: 上下文变量字典
        :return: 渲染后的字符串
        """
        return TemplateUtil.render_file(template_path, context)
