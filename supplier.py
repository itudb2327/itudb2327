class Supplier:
    def __init__(self, id=None, company=None, last_name=None, first_name=None, email_address=None, job_title=None,
                 business_phone=None, home_phone=None, mobile_phone=None, fax_number=None, address=None,
                 city=None, state_province=None, zip_postal_code=None, country_region=None, web_page=None,
                 notes=None, attachments=None):
        self.id = id
        self.company = company
        self.last_name = last_name
        self.first_name = first_name
        self.email_address = email_address
        self.job_title = job_title
        self.business_phone = business_phone
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.fax_number = fax_number
        self.address = address
        self.city = city
        self.state_province = state_province
        self.zip_postal_code = zip_postal_code
        self.country_region = country_region
        self.web_page = web_page
        self.notes = notes
        self.attachments = attachments