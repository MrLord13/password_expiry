{
    'name': 'Password Expiry ERPishro',
    'version': '19.0.1.0.0',
    'author': 'AliReza Nemati',
    'description': 'Password Expiry ERPishro Company',
    'summary': 'Password Expiry ERPishro Company',
    'category': 'Security',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/cron.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'sequence': -100
}
