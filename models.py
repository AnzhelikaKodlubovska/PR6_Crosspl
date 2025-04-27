class Client:
    def __init__(self, name, gender, birthdate, phone, email, extra_info):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.phone = phone
        self.email = email
        self.extra_info = extra_info

    def __repr__(self):
        return f"Client(first_name='{self.name}', gender='{self.gender}', birthdate='{self.birthdate}', phone='{self.phone}', email='{self.email}', extra_info='{self.extra_info}')"