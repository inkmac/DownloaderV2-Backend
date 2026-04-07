from pathlib import Path

def check_cookie_file_valid(cookiefile: Path) -> tuple[bool, str]:
    """
    检查 Cookie 文件：
    1. 是否存在
    2. 是否为空
    3. 是否是合法的 Netscape 格式
    返回：(是否合法, 提示信息)
    """
    # 1. 检查文件是否存在
    if not cookiefile.exists():
        return False, f"[Warning] Cookie 文件不存在：{cookiefile}"

    # 2. 检查是否是文件（不是文件夹）
    if not cookiefile.is_file():
        return False, f"[Warning] 不是有效文件：{cookiefile}"

    # 3. 检查文件大小是否为空
    if cookiefile.stat().st_size == 0:
        return False, f"[Warning] Cookie 文件为空：{cookiefile}"

    # 4. 检查是否是标准 Netscape Cookie 格式（关键）
    try:
        with open(cookiefile, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()

            # 合法的 Netscape Cookie 文件第一行必须是这个
            if not first_line.startswith("# Netscape HTTP Cookie File"):
                return False, "[Warning] Cookie 格式错误，不是标准 Netscape 格式"

        return True, ""

    except Exception as e:
        return False, f"[Warning] 读取 Cookie 文件失败：{str(e)}"