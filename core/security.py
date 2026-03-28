import bcrypt


def generate_password_hash(password: str) -> str:
    
    # 1. Transformamos a string em bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Geramos um salt e criamos o hash
    salt = bcrypt.gensalt()
    # 3. Criamos o hash usando o bcrypt
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # Retornamos como string para salvar no banco de dados
    return hashed.decode('utf-8')


def verify_ppassword(password: str, hashed_password: str) -> bool:
    # Para verificar, comparamos a senha vinda do usuário
    # com o hash que está no banc
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))