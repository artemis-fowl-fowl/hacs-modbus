"""Cover template pour volets iSMART."""

# Ce fichier servira à créer automatiquement les covers template
# L'utilisateur peut copier le contenu dans la section template: de configuration.yaml

COVER_TEMPLATE = """
template:
  - cover:
      - unique_id: tpl_vr_gabriel
        name: VR Gabriel
        default_entity_id: cover.vr_gabriel
        open_cover:
          - action: switch.turn_on
            target:
              entity_id: switch_gabriel_volet_up
        close_cover:
          - action: switch.turn_on
            target:
              entity_id: switch_gabriel_volet_down
        stop_cover:
          - action: switch.turn_off
            target:
              entity_id: switch_gabriel_volet_up
"""

# À ajouter manuellement dans configuration.yaml pour chaque salle avec volets
