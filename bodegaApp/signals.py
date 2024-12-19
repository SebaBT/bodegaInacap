import json
import logging
from django.db.models.signals import pre_save, pre_delete
from django.db.models.signals import post_migrate
from django.apps import AppConfig, apps
from django.dispatch import receiver
from django.forms import model_to_dict
from bodegaApp.models.helpers.adjuntoDefaults import create_default_adjunto  # Import functions
from bodegaApp.models.helpers.adminDefaults import create_default_admin, create_default_person
from bodegaApp.models.helpers.categoriaDefaults import create_default_categoria
from bodegaApp.models.identidades import Usuario
from bodegaApp.models.registros import Registro

@receiver(post_migrate)
def create_default_instances(sender, **kwargs):
    if isinstance(sender, AppConfig) and sender.name == 'bodegaApp': # Check against AppConfig type and name
        create_default_adjunto()
        create_default_categoria()
        create_default_person()
        create_default_admin()
        
def log_change(sender, instance, action):  # Consolidated logic
    try:
        if sender._meta.app_label == 'bodegaApp' and not sender._meta.model_name == 'registro':
            user_id = 'System'
            if hasattr(instance, 'usuario') and instance.usuario:
                user_id = instance.usuario.id

            nombre_tabla = sender._meta.db_table

            if action == 'deleted':  # Special handling for deletions
                previous_data = model_to_dict(instance)
                new_data = {}  # Empty for deletions
            else: # created or updated
                try:
                    previous_instance = sender.objects.get(pk=instance.pk)
                    previous_data = model_to_dict(previous_instance)

                except sender.DoesNotExist:
                    previous_data = {}

                new_data = model_to_dict(instance)

            Registro.objects.create(
                user_id=Usuario.objects.get(id=user_id),
                nombreTabla=nombre_tabla,
                modeloPrevio=json.dumps(previous_data),
                modeloNuevo=json.dumps(new_data),
                action=action,
            )

    except Exception as e:
        logging.error(f"Error in model_log signal: {e}")
        
@receiver(pre_save)
def model_log_save(sender, instance, **kwargs):  # Renamed for clarity
    log_change(sender, instance, 'ACTUALIZADO' if instance.pk else 'CREADO')

@receiver(pre_delete)
def model_log_delete(sender, instance, **kwargs):
    log_change(sender, instance, 'BORRADO')

