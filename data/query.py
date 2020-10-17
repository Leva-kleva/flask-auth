create_user = """
        INSERT INTO 
            users (username, password, email) SELECT %(name)s, %(password)s, %(email)s  
        WHERE not exists( select username from users where username=%(name)s);
        """

get_user = "SELECT * FROM users WHERE email=%(email)s and password=%(password)s"

get_user_by_id = "SELECT * FROM users WHERE id=%(user_id)s"

delete_user = "DELETE FROM users WHERE email=%(email)s"

change_user_password = "UPDATE users SET password=%(password)s WHERE email=%(email)s"
