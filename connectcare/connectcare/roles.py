from rolepermissions.roles import AbstractUserRole

class Doctor(AbstractUserRole):
    available_permissions = {
    	'view_forum': True,
    	'view_schedule': True,
    	'view_patients': True,
    	'upload_results': True,
    	'view_records': True,
    	'upload_pres': True,
    	'search': True,
        'add_question':True,
        'add_comment':True,
        'view_pres': True,
        'view_results': True,
        'schedule': True,
        'add_schedule': True,
        'delete_schedule': True,



        
    }

class Patient(AbstractUserRole):
    available_permissions = {
        'view_forum': True,
        'upload_records': True,
        'view_results': True,
        'view_schedule': True,
        'view_doctors': True,
        'view_records': True,
        'view_pres': True,
        'search': True,
        'authorize':True,
        'add_question':True,
        'add_comment':True,
        'schedule': True,
        'add_schedule': True,
        'delete_schedule': True,

        
    }

class Public(AbstractUserRole):
    available_permissions = {
        'view_forum': True,
        'add_question':True,
        'add_comment':True,

    }