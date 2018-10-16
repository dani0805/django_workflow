from django.db import models

# Create your models here.
from django.db.models import CASCADE

from django_workflow.models import Transition


class ApprovalGroup(models.Model):
    transitions = models.ManyToManyField(Transition, related_name="group")

    @staticmethod
    def clone_from_old(transition_map: dict):
        """
        Clone groups from old to new ones
        :param transition_map: {old_transition_id: new_transition_id}
        :return: void
        """
        # old : new
        group_map = {}
        transitions = Transition.objects.filter(id__in=transition_map.keys())
        for transition in transitions:
            old_group = transition.group.first()
            if old_group is None:
                continue
            # if the old_group is not in the map, it is not be processed, so create the new group and link the new transations
            if old_group.id not in group_map:
                old_group_id = old_group.id
                group_map[old_group_id] = None
                new_group = old_group
                # clone db object
                new_group.id, new_group.pk = None, None
                new_group.save()
                group_map[old_group_id] = new_group.id
                # retrieve the old transition ids linked to the group
                old_transition_ids = list(Transition.objects.filter(group__id=old_group_id).values_list('id', flat=True))
                # retrieve the mapping
                new_transition_ids = [v for k, v in transition_map.items() if k in old_transition_ids]
                new_group.transitions.set(Transition.objects.filter(id__in=new_transition_ids))

