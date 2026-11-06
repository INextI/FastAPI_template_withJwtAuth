from Auth.utils import hashed_password, validate_password
import bcrypt

def test_password_is_hashed():
    password = "pass"
    result = hashed_password(password)

    assert result != password.encode()
    assert isinstance(result, bytes)
    assert bcrypt.checkpw(password.encode(), result)

def test_validate_password():
    password = "pass"
    hashed = hashed_password(password)

    assert validate_password(password, hashed) is True

def test_wrong_password_is_rejected():
    password = "pass"
    hashed = hashed_password(password)
    wrong_pass = "wrong_pass"
    assert validate_password(password=wrong_pass, hashed_password=hashed) is not True