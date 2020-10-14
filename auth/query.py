create_user = "INSERT INTO users (username, password, email) VALUES ('{name}', '{password}', '{email}')"

get_user = "SELECT * FROM users WHERE email='{email}' and password='{password}'"

get_user_by_id = "SELECT * FROM users WHERE id='{user_id}'"

delete_user = "DELETE FROM users WHERE email='{email}'"

change_user_password = "UPDATE users SET password='{password}' WHERE email='{email}'"
