from odoo import models, fields, api

class Etiquette(models.Model):
    _name = 'mon.module.etiquette'
    _description = 'Etiquette pour catégoriser les tâches'

    name = fields.Char(string='Nom de l\'étiquette', required=True)
    couleur = fields.Selection([
        ('red', 'Rouge'),
        ('blue', 'Bleu'),
        ('green', 'Vert'),
        ('yellow', 'Jaune'),
        ('orange', 'Orange'),
        ('purple', 'Violet'),
    ], string='Couleur', default='blue')
    description = fields.Text(string='Description')