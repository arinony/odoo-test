from odoo import models, fields, api

class Projet(models.Model):
    _name = 'mon.module.projet'
    _description = 'Projet pour regrouper les tâches'

    name = fields.Char(string='Nom du projet', required=True)
    description = fields.Text(string='Description')
    date_debut = fields.Date(string='Date de début', default=fields.Date.today)
    date_fin = fields.Date(string='Date de fin prévue')
    chef_projet = fields.Many2one('res.users', string='chef de projet', default=lambda self: self.env.user)
    active = fields.Boolean(string='Actif', default=True)

   
    tache_ids = fields.One2many(
           'mon.module.tache',
            'projet_id',
            string='Tâches du projet'
        )
