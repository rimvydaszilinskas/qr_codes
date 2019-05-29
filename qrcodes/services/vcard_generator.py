import qrcode
import re

PHONE_TYPES = ["WORK", "HOME", "MAIN", "MOBILE"]

def get_phone_type(line):
    # return type of phone based on the line of text
    matches = re.search("TYPE=(.+?):", line)
    
    if matches is None:
        return None

    PHONE_TYPES = ["WORK", "HOME", "MAIN", "MOBILE"]

    for phone_type in PHONE_TYPES:
        if phone_type in matches.group().upper():
            return phone_type
    
    return None

def generate_vcard_string(firstname, lastname, title=None, organisation=None,
                            job_title=None, phone=None, email=None, revision_date=None, birthday=None):
    # convert all the data to strings correctly for future use
    title = convert(title)
    organisation = convert(organisation)
    job_title = convert(job_title)
    phone = convert(phone)
    email = convert(email)
    revision_date = convert(revision_date)
    birthday = convert(birthday)

    # start writing the file
    string = 'BEGIN:VCARD\nVERSION:4.0\n'
    string += f'N:{lastname};{firstname};;{title};\n'
    if organisation != '':
        string += f'ORG:{organisation}\n'
    if job_title != '':
        string += f'TITLE:{job_title}\n'
    
    # check if phone exist
    if phone != '':
        # check if phone is defined in appropriate type. 
        if isinstance(phone, list) or isinstance(phone, tuple):
            # if iterabale - iterata
            for number in phone:
                if isinstance(number, str):
                    string += f"TEL;TYPE=HOME:{number}\n"
                else:
                    string += f"TEL;TYPE={number.get('type', 'HOME')}:{number.get('number', '')}\n"
        elif isinstance(phone, str):
            #  if string, that means only one phone created
            string += f"TEL;TYPE=HOME:{phone}\n"
        elif isinstance(phone, dict):
            string += f"TEL;TYPE={phone.get('type', 'HOME')}:{phone.get('number')}\n"

    # the same as phones goes for email
    if isinstance(email, list) or isinstance(email, tuple):
        for email_address in email:
            string += f'EMAIL:{email_address}\n'
    elif email != '':
        string += f'EMAIL:{email}\n'
    if revision_date != '':
        string += f'REV:{revision_date}\n'
    string += 'END:VCARD'

    return string

def generate_vcard_qrcode(firstname, lastname, title=None, organisation=None, 
                            job_title=None, phone=None, email=None, revision_date=None, birthday=None):
    vcard_info = generate_vcard_string(firstname, lastname, title, organisation, job_title, phone, email, revision_date, birthday)

    return qrcode.make(vcard_info)

def generate_vcard_qrcode_from_vcard(info):
    return qrcode.make(info)

def convert(value):
    # returns empty string if the value is null otherwise the original value is returned
    return '' if value is None else value

def load_data_from_vcard(vcard):
    lines = vcard.splitlines()
    # initialize empty dictionary for data
    data = {}
    # setup empty array for phones
    data["phone"] = []

    for line in lines:
        if line.startswith("N:"):
            # get the names
            linesplit = line.split(":")
            names = linesplit[1].split(";")
            # convert names to list
            names = list(names)
            # split name into firstname and lastname
            if len(names) == 1:
                data["firstname"] = names[0]
            elif len(names) >= 2:
                data["lastname"] = names[0]
                data["firstname"] = names[1]
        # set the organization
        if line.startswith("ORG:"):
            organization = line.split(":")[1]
            data["organization"] = organization
        # set phones
        if line.startswith("TEL:") or line.startswith("TEL;"):
            phone = {}
            phone_type = get_phone_type(line)

            if phone_type is not None:
                phone["type"] = phone_type

            # extract the number
            number = line.split(":")[1]
            phone["number"] = number

            data["phone"].append(phone)
        if line.startswith("TITLE:"):
            data["job_title"] = line.split(":")[1]
        if line.startswith("EMAIL:"):
            data["email"] = line.split(":")[1]
    return data