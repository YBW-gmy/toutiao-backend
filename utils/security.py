import hashlib
import base64
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prehash(password: str) -> str:
    """SHA-256 预哈希，绕过 bcrypt 72 字节限制"""
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")


def get_hash_password(password: str):
    """新密码统一走 SHA-256 预哈希"""
    return pwd_context.hash(_prehash(password))


def verify_password(plain_password: str, hashed_password: str) -> tuple[bool, bool]:
    """
    验证密码，自动兼容旧格式。
    返回 (成功, 是否需要更新密码哈希)
    """
    # 先尝试新方式 (SHA-256 预哈希)
    if pwd_context.verify(_prehash(plain_password), hashed_password):
        return True, False
    # 兼容旧方式 (原始 bcrypt，无预哈希)
    if pwd_context.verify(plain_password, hashed_password):
        return True, True  # 需要升级为新格式
    return False, False
