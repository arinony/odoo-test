from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class TacheRESTAPI(http.Controller):
    def check_api_key(self):
        api_key = request.httprequest.headers.get('X-API-KEY')
        if not api_key:
                return False
        
        return api_key == 'ton_api_secrete_key'
    
    def json_response(self, data, status=200):
         return Response(
              json.dumps(data, ensure_ascii=False),
              status=status,
              content_type='application/json; charset=utf-8'
         )
    
    @http.route('/api/v1/taches', type='http', auth='user', methods=['GET'], csrf=False)
    def get_taches(self, **kwargs):
         try:
            domain = []
            if kwargs.get('state'):
                domain.append(('state', '=', kwargs['state']))
            if kwargs.get('priorite'):
                domain.append(('priorite', '=', kwargs['priorite']))
            if kwargs.get('projet_id'):
                domain.append(('projet_id','=', int(kwargs['projet_id']))) 
            if kwargs.get('utilisateur_id'):
                domain.append(('utilisateur_id','=', int(kwargs['utilisateur_id'])))  

            taches = request.env['mon.module.tache'].search(domain)

            result = []
            for tache in taches:
                 result.append({
                    'id': tache.id,
                    'name': tache.name,
                    'description': tache.description,
                    'state': tache.state,
                    'priorite': tache.priorite,
                    'date_echeance': str(tache.date_echeance) if tache.date_echeance else None,
                    'jours_restants': tache.jours_restants,
                    'est_en_retard': tache.est_en_retard,
                    'projet': tache.projet_id.name if tache.projet_id else None,
                    'projet_id': tache.projet_id.id  if tache.projet_id else None,
                    'utilisateur': tache.utilisateur_id.name if tache.utilisateur_id else None,
                    'etiquettes': [{'id': tag.id, 'name': tag.name, 'couleur':tag.couleur}
                    for tag in tache.etiquette_ids]})
                 
            return self.json_response({
                 'success': True,
                 'data': result,
                 'total': len(result)
            })
        
         except Exception as e:
              _logger.error("API Error: %s", str(e))
              return self.json_response({
                   'success': False,
                   'error': str(e)
              }, status=500)
         
    @http.route('/api/v1/taches/<int:tache_id>', type='http', auth='user', methods=['GET'], csrf=False)
    def get_tache(self, tache_id, **kwargs):
        try:
              tache = request.env['mon.module.tache'].browse(tache_id)
              if not tache.exists():
                   return self.json_response({
                        'success':False,
                        'error': 'Tâches non trouvée'
                   }, status=404)
              data = {
                   'id' : tache.id,
                   'name' : tache.name,
                   'description' : tache.description,
                   'state' : tache.state,
                   'priorite' : tache.priorite,
                   'date_creation' : str(tache.date_creation),
                   'date_echeance' : str(tache.date_echeance) if tache.date_echeance else None,
                   'jours_restants' : tache.jours_restants,
                   'est_en_retard' : tache.est_en_retard,
                    'projet' : {
                         'id' : tache.projet_id.id,
                         'name': tache.projet_id.name,
                    }      
                    if tache.projet_id else None,
                    'utilisateur': {
                         'id': tache.utilisateur_id.id,
                         'name': tache.utiisateur_id.name,
                    }
                    if tache.utilisateur_id else None
                    ,
                    'etiquettes': [{
                         'id': tag.id,
                         'name' : tag.name,
                         'couleur' : tag.couleur,                 
                             }
                        for tag in tache.etiquette_ids]
                        }
              return self.json_response({
                         'success' : True,
                         'data' : data
                    })            
        except Exception as e:
             _logger.error("API Error: %s", str(e))
             return self.json_response({
                  'success':False,
                  'error' : str(e)
             }, status=500)
        
    @http.route('/api/v1/taches', type='json', auth='user', methods=['POST'], csrf=False)
    def create_tache(self, **data):
         try:
              nouvelle_tache = request.env['mon.module.tache'].create({
                   'name': data.get('name'),
                   'description': data.get('description'),
                   'state' : data.get('state', 'a_faire'),
                   'priorite': data.get('priorite', 'moyenne'),
                   'date_echeance': data.get('date_echeance'),
                   'projet_id': data.get('projet_id'),
                   'utilisateur_id':data.get('utilisateur_id', request.env.user.id),
              })

              if data.get('etiquette_ids'):
                   nouvelle_tache.etiquette_ids = [(6, 0, data['etiquette_ids'])]

              return {
                   'success' : True,
                   'message' : 'Tâche créer avec succés',
                   'id': nouvelle_tache.id
              }
         except Exception as e:
              _logger.error("API Create Error: %s", str(e))
              return {
                   'success':False,
                   'error': str(e)
              }
         
    @http.route('/api/v1/taches/<int:tache_id>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_tache(self, tache_id, **data):
         try:
              tache = request.env['mon.module.tache'].browse(tache_id)
              if not tache.exists():
                   return {
                        'success':False,
                        'error': 'Tâche non trouvée'
                   }
              update_data = {}
              for field in ['name', 'description', 'state', 'priorite', 'date_echeance', 'projet_id', 'utilisateur_id']:
                   if field in data:
                        update_data[field] = data[field]
              if update_data:
                   tache.write(update_data)

              if 'etiquette_ids' in data:
                   tache.etiquette_ids = [(6, 0, data['etiquette_ids'])]

              return {
                   'success': True,
                   'message': 'Tâche mise à jour avec succès'
              }
         

         except Exception as e:
              _logger.error("API Update Error: %s", str(e))
              return {
                   'success':False,
                   'error':str(e)
              }
         
    @http.route('/api/v1/taches/<int:tache_id>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def delete_tache(self, tache_id):
         try:
              tache = request.env['mon.module.tache'].browse(tache_id)
              if not tache.exists():
                   return {
                        'success' : False,
                        'errorr': 'Tâche non trouvée' 
                   }
              tache.unlink()

              return {
                   'success': True,
                   'messsage': 'Tâcje supprimée avec succès'
              }
         except Exception as e:
              _logger.error("API Delete Error: %s", str(e))
              return {
                   'success': False,
                   'error': str(e)
              }
         
    @http.route('/api/v1/taches/<int:tache_id>/terminer', type='json', auth='user', methods=['POST'],  csrf=False)
    def terminer_tache(self, tache_id):
         try:
              tache = request.env['mon.module.tache'].browse(tache_id)
              if not tache.exists():
                   return {
                        'success': False,
                        'error': 'Tâche non trouvée'
                   }
              tache.action_marquer_comme_termine()

              return {
                   'success': True, 
                   'message':'Tâche marquée comme terminée'
              }
         except Exception as e:
              _logger.error("API action Error: %s", str(e))
              return {
                   'success': False,
                   'error':str(e)
              }
         
    @http.route('/api/v1/statistiques', type='http', auth='user', methods=['GET'], csrf=False)
    def get_statistiques(self):
         try:
              env = request.env
              Tache = env['mon.module.tache']

              total_taches = Tache.search_count([])
              taches_terminees = Tache.search_count([('state', '=', 'termine')])
              taches_en_retard = Tache.search_count([('est_en_retard', '=', True)])

              stats_priorite = {}
              for priorite in ['basse', 'moyenne', 'haute']:
                   stats_priorite[priorite] = Tache.search_count([('priorite', '=', priorite)])
              stats_etat = {}
              for etat in ['a_faire', 'en_cours', 'termine']:
                   stats_etat[etat] = Tache.search_count([('state', '=', etat)])
              return self.json_response({
                   'success': True,
                   'data': {
                        'total_taches' : total_taches,
                        'taches_terminees': taches_terminees,
                        'taches_en_retard': taches_en_retard,
                        'taux_accomplissement': (taches_terminees / total_taches *100) if total_taches > 0 else 0,
                        'par_priorite': stats_priorite,
                        'par_etat': stats_etat
                   }
              })
         except Exception as e:
              _logger.error("API Stats Error: %s", str(e))
              return self.json_response({
                   'success': False,
                   'error': str(e)
              }, status=500)