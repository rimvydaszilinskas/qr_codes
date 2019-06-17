import re
import qrcode

class VCardGenerator:
    def __init__(self, *args, **kwargs):
        self.__firstname = kwargs.get('firstname', None)
        self.__lastname = kwargs.get('lastname', None)
        self.__email = kwargs.get('email', None)
        self.__organization = kwargs.get('organization', None)
        self.__phones = []
        self.__title = None

    def set_email(self, email):
        self.__email = email

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def set_lastname(self, lastname):
        self.__lastname = lastname

    def set_organization(self, organization):
        self.__organization = organization

    def set_title(self, title):
        self.__title = title

    def add_phone(self, phone, phone_type='HOME'):
        self.__phones.append({'number': phone, 'type': phone_type})

    def get_phones(self):
        return self.__phones

    def generate_string(self):
        string = 'BEGIN:VCARD\nVERSION:4.0\n'
        string += f'N:{self.__lastname if self.__lastname else ""};{self.__firstname if self.__firstname else ""};;;\n'
        if self.__organization:
            string += f'ORG:{self.__organization}\n'
        if self.__title:
            string += f'TITLE:{self.__title}'

        for phone in self.__phones:
            string += f'TEL;TYPE={phone["type"]};VALUE=uri:tel:{phone["number"]}\n'

        if self.__email:
            string += f'EMAIL:{self.__email}\n'
        string += 'END:VCARD'

        return string

    def loads(self, vcard):
        lines = vcard.splitlines()
        
        for line in lines:
            if line.startswith('N'):
                names = line.split(':')[1].split(';')
                if names[0] != '':
                    self.set_lastname(names[0])
                if names[1] != '':
                    self.set_firstname(names[1])
            elif line.startswith('ORG:'):
                organization = line.split(':')[1]

                self.set_organization(organization)
            elif line.startswith('TITLE:'):
                title = line.split(':')[1]

                self.set_title(title)
            elif line.startswith('TEL;'):
                match = re.search(r'TYPE=(.+?);VALUE=uri:tel:(.+)', line)
                
                self.add_phone(phone=match.group(2), phone_type=match.group(1))
            elif line.startswith('EMAIL:'):
                email = line.split(':')[1]
                self.set_email(email)

    def get_as_dictionary(self):
        return {
            'firstname': self.__firstname,
            'lastname': self.__lastname,
            'phones': self.__phones,
            'email': self.__email,
            'organization': self.__organization,
            'title': self.__title
        }

    def get_qr(self):
        return qrcode.make(self.generate_string())