{
    'name' : 'Gestion des tâches',
    'version':'6.6',
    'summary':'Gestion de tâches personnalisée',
    'description':"""
        Mon premier module odoo pour gérer des tâches personnalisées
        Créé prendant mon apprentissage Odoo
""",
    'category': 'Productivity',
    'author':'Victorio',
    'website':'',
    'depends':['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/vues.xml',
        'views/graphiques.xml',
        'views/automation.xml',
        'views/recherches.xml'
    ],
    'controllers': ['controllers/rest_api.py'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images':['static/description/icon.png']
}