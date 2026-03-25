from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

class Tache(models.Model):
    _name = 'mon.module.tache'
    _description = 'Tâche personnalisée'

    name = fields.Char(string='Nom de la tâche', required=True)
    description = fields.Text(string='Description')
    date_creation = fields.Datetime(string='Date de création', default=fields.Datetime.now) 
    date_echeance = fields.Date(string='Date d\'échéance')

    #champ pour le calendrier
    date_debut = fields.Date(string='Date de début', default=fields.Date.today)
    #fin du champ

    est_termine = fields.Boolean(string='Terminé', default=False)
    priorite = fields.Selection([
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
    ], string='Priorité', default='moyenne')

    # Nouveau champ etat pour kaban
    state = fields.Selection([
            ('a_faire', 'A faire'),
            ('en_cours', 'En cours'),
            ('termine', 'Terminé'),
    ], string='Etat', default='a_faire', required=True)
    #fin du nouveau champ

    est_en_retard = fields.Boolean(
        string='En retard',
        compute='_compute_est_en_retard',
        store=True
    )


    utilisateur_id = fields.Many2one('res.users', string='Assigné à', default=lambda self: self.env.user)

    jours_restants = fields.Integer(
        string='Jours restants',
        compute='_compute_jours_restants'
    )

    projet_id = fields.Many2one(
        'mon.module.projet',
        string='Projet',
        ondelete='set null'
    )

    etiquette_ids = fields.Many2many(
        'mon.module.etiquette',
        string='Etiquettes'
    )

    #methode d'automatisation
    @api.model
    def action_automatique_taches_en_retard(self):
        ajourdhui = fields.Date.today()
        taches_en_retard = self.search([
            ('date_echeance', '<', ajourdhui ),
            ('state', '!=', 'termine'),
            ('est_termine', '=', False)
        ])
        for tache in taches_en_retard:
            tache.write({
                'state': 'en_cours',
                'priorite': 'haute',
                'est_en_retard': True
            })
        return len(taches_en_retard)
    
    def action_marquer_comme_termine(self):
        for record in self:
            record.write({
                'state': 'termine',
                'est_termine':True,
                'est_en_retard':False,
                'date_echeance':fields.Date.today()
            })

    def action_reactiver_tache(self):
        for record in self:
            record.write({
                'state':'a_faire',
                'est_termine': False
            })

    @api.model
    def cron_verifier_echeances(self):
        count = self.action_automatique_taches_en_retard()
        _logger.info(f"{count} tâches mises à jour automatiquement")

    
    @api.depends('date_echeance', 'state', 'est_termine')
    def _compute_est_en_retard(self):
        for record in self:
            if(record.date_echeance and 
               record.date_echeance < fields.Date.today() and 
               record.state != 'termine' and
               not record.est_termine):
                
                record.est_en_retard = True
                if record.priorite != 'haute':
                    record.priorite = 'haute'
                if record.state != 'en_cours':
                    record.state = 'en_cours'
            else:
                record.est_en_retard = False

    #fin de methodes d automatisation

    @api.depends('date_echeance')
    def _compute_jours_restants(self):
        for record in self:
            if record.date_echeance:
                today = fields.Date.today()
                record.jours_restants = (record.date_echeance - today).days
            else:
                record.jours_restants=0