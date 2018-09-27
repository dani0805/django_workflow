from enum import Enum

from django.db.models import Max, Q

import django_workflow.graph
from django_workflow.graph import Graph
from django_workflow.models import State, Transition, Workflow


class NodeType(str, Enum):
    APPROVED = "approved"
    APPROVAL = "approval"
    JUNCTION = "junction"
    START = "start"
    END = "end"

class ApprovalGraph(django_workflow.graph.Graph):

    def __init__(self, workflow: Workflow):
        super(ApprovalGraph, self).__init__(workflow)
        self.node_id_seq = workflow.state_set.aggregate(Max('id'))['id__max'] + 1
        self.link_id_seq = workflow.transition_set.aggregate(Max('id'))['id__max'] + 1

    @property
    def nodes_and_links(self) -> dict:
        states = self.workflow.state_set.all()
        nodes, links = self.nodes_and_links_from_states(states)
        return {"nodes": nodes, "links": links}

    @staticmethod
    def get_node_type(state: State) -> (NodeType, [str]):

        # check if it has variables and if they correspond to a "variable_name" callback parameter of a
        # transition that starts and end on this node
        if state.variable_definitions.all().count() > 0:
            transitions = Transition.objects.filter(
                callback__parameters__name="variable_name",
                workflow=state.workflow,
                initial_state=state,
                final_state=state)
            if transitions.count() > 0:
                return NodeType.APPROVAL, [
                    p.value
                    for t in transitions.all()
                    for c in t.callback_set.all()
                    for p in c.parameters.all()
                ]
        # check if no incoming transitions then start
        if state.incoming_transitions.count() == 0:
            return NodeType.START, None
        if state.outgoing_transitions.count() == 0:
            return NodeType.END, None
        else:
            return NodeType.JUNCTION, None

    def nodes_and_links_from_states(self, states: [State]) -> ([dict], [dict]):
        nodes = []
        links =[]
        for state in states:
            type, names = ApprovalGraph.get_node_type(state)
            if type == NodeType.APPROVAL:
                incoming_transition = state.incoming_transitions.exclude(
                    initial_state=state
                ).get()
                outgoing_transition = state.outgoing_transitions.exclude(
                    Q(final_state=state) |
                    Q(final_state__initial=True)
                ).get()

                for name in names:
                    nodes.append(
                        {
                            "id": self.node_id_seq,
                            "state_id": state.id,
                            "name": name,
                            "type": type,
                            "state_name": state.name,
                            "active": state.active,
                            "variables": [{"id": v.id, "name": v.name} for v in state.variable_definitions.all()]
                        }
                    )
                    links.append(
                        {
                            "id":self.link_id_seq,
                            "transition_id": incoming_transition.id,
                            "name": incoming_transition.name,
                            "initial_state": incoming_transition.initial_state.id if incoming_transition.initial_state else None,
                            "final_state": incoming_transition.final_state.id,
                            "source":incoming_transition.initial_state.id if incoming_transition.initial_state else None,
                            "target": self.node_id_seq,
                            "conditions": [Graph.render_condition(c) for c in incoming_transition.condition_set.all()],
                            "callbacks": [Graph.render_callback(k) for k in incoming_transition.callback_set.all()]

                        }
                    )
                    self.link_id_seq += 1
                    approval_transition = state.outgoing_transitions.get(
                        callback__parameters__name="variable_name",
                        final_state=state,
                        callback__parameters__value=name
                    )
                    links.append(
                        {
                            "id": self.link_id_seq,
                            "transition_id": outgoing_transition.id,
                            "approval_transition_id": approval_transition.id,
                            "name": approval_transition.name,
                            "initial_state": outgoing_transition.initial_state.id,
                            "final_state": outgoing_transition.final_state.id,
                            "source": self.node_id_seq,
                            "target": outgoing_transition.final_state.id,
                            "approval_conditions": [Graph.render_condition(c) for c in approval_transition.condition_set.all()],
                            "approval_callbacks": [Graph.render_callback(k) for k in approval_transition.callback_set.all()],
                            "conditions": [Graph.render_condition(c) for c in outgoing_transition.condition_set.all()],
                            "callbacks": [Graph.render_callback(k) for k in outgoing_transition.callback_set.all()]

                        }
                    )
                    self.link_id_seq += 1
                    self.node_id_seq += 1

            else:
                nodes.append(
                    {
                        "id": state.id,
                        "state_id": state.id,
                        "name": state.name,
                        "type": type,
                        "state_name": state.name,
                        "active": state.active,
                        "variables": [{"id": v.id, "name": v.name} for v in state.variable_definitions.all()]
                    }
                )
                if type != NodeType.JUNCTION:
                    for t in list(state.incoming_transitions.all()) + list(state.outgoing_transitions.all()):
                        links.append(
                            {
                                "id": self.link_id_seq,
                                "transition_id": t.id,
                                "name": t.name,
                                "initial_state": t.initial_state.id if t.initial_state else None,
                                "final_state": t.final_state.id,
                                "start_node": t.initial_state.id if t.initial_state else None,
                                "end_node": t.final_state.id,
                                "conditions": [Graph.render_condition(c) for c in
                                    t.condition_set.all()],
                                "callbacks": [Graph.render_callback(k) for k in t.callback_set.all()]

                            }
                        )
        return nodes, links