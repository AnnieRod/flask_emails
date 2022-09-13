from flask_app.config.mysqlconnection import connectToMySQL

import re

from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Mail: 
    def __init__(self, data):
        self.id = data['id']
        self.address = data['address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

##Recupera info por cada instancia creada
    @classmethod
    def get_emails(cls):
        query= "SELECT * FROM emails;"
        results = connectToMySQL('email_validation').query_db(query)
        emails = []
        for email in results:
            emails.append(cls(email))
        return emails

## Crea instancia de correo e integra registro en base de datos
    @classmethod
    def save_email(cls, data):
        query = "INSERT INTO emails(address, created_at, updated_at) VALUES (%(address)s, NOW(), NOW());"
        new_mail = connectToMySQL('email_validation').query_db(query, data)
        return new_mail
    
##BONUS NINJA: Método de borrado de direccion de correo
    @classmethod
    def delete_mail(cls,data):
        query = "DELETE FROM emails WHERE id = %(id)s"
        return connectToMySQL('email_validation').query_db(query, data)

##MÉTODO DE VALIDACION
    @staticmethod
    def validate_email(email):
        is_valid = True
        ##BONUS NINJA: Valida si el email ya existe
        query = "SELECT * FROM emails WHERE address = %(address)s;"
        coincidence = connectToMySQL('email_validation').query_db(query, email)
        if len(coincidence) >= 1:
            flash ("Invalid email, address already registered...")
            is_valid = False
            return is_valid
            
        if not EMAIL_REGEX.match(email['address']):
            flash("Email is not valid!")
            is_valid = False
        else:
            flash(f"The email address you entered ({email['address']}) is VALID, Thank you!")
            is_valid = True
        return is_valid