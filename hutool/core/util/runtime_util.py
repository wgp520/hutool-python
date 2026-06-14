"""运行时工具类"""

from __future__ import annotations

import os
import subprocess
import sys
from typing import List, Optional


class RuntimeUtil:
    """运行时工具类"""

    @staticmethod
    def exec(command: str, timeout: Optional[int] = None) -> str:
        """执行系统命令，返回输出"""
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout

    @staticmethod
    def exec_lines(command: str, timeout: Optional[int] = None) -> List[str]:
        """执行系统命令，返回输出行列表"""
        output = RuntimeUtil.exec(command, timeout=timeout)
        lines = output.splitlines()
        # 去除末尾空行
        while lines and not lines[-1].strip():
            lines.pop()
        return lines

    @staticmethod
    def get_pid() -> int:
        """获取当前进程PID"""
        return os.getpid()

    @staticmethod
    def get_memory_info() -> dict:
        """获取内存信息（单位字节）
        返回 {'total': ..., 'available': ..., 'used': ...}
        使用 /proc/meminfo (Linux) 或 psutil 回退
        """
        # 尝试使用 psutil（跨平台）
        try:
            import psutil  # type: ignore

            mem = psutil.virtual_memory()
            return {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
            }
        except ImportError:
            pass

        # Linux 回退：读取 /proc/meminfo
        if sys.platform.startswith("linux"):
            meminfo = {}
            try:
                with open("/proc/meminfo") as f:
                    for line in f:
                        parts = line.split(":")
                        if len(parts) == 2:
                            key = parts[0].strip()
                            val = parts[1].strip().split()[0]
                            meminfo[key] = int(val) * 1024  # kB -> bytes
                total = meminfo.get("MemTotal", 0)
                available = meminfo.get("MemAvailable", meminfo.get("MemFree", 0))
                return {
                    "total": total,
                    "available": available,
                    "used": total - available,
                }
            except OSError:
                pass

        return {"total": 0, "available": 0, "used": 0}

    @staticmethod
    def get_available_processors() -> int:
        """获取可用CPU核心数"""
        try:
            return os.cpu_count() or 1
        except Exception:
            return 1
