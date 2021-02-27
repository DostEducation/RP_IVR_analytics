from api import models

def get_partner_id_by_system_phone(system_phone):
	system_phone_details = models.SystemPhone.query.get_by_phone(system_phone)
	if system_phone_details:
		partner_system_phone = models.PartnerSystemPhone.query.get_by_system_phone_id(system_phone_details.id)
		if partner_system_phone:
			return partner_system_phone.partner_id