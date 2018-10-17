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
                            "stateId": state.id,
                            "name": name,
                            "type": type,
                            "stateName": state.name,
                            "active": state.active,
                            "initial": state.initial,
                            "variables": [{"id": v.id, "name": v.name} for v in state.variable_definitions.all()]
                        }
                    )
                    links.append(
                        {
                            "id": self.link_id_seq,
                            "transitionId": incoming_transition.id,
                            "name": incoming_transition.name,
                            "label": incoming_transition.label,
                            "initialState": incoming_transition.initial_state.id if incoming_transition.initial_state else None,
                            "finalState": incoming_transition.final_state.id,
                            "source": incoming_transition.initial_state.id if incoming_transition.initial_state else None,
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
                            "label": approval_transition.label,
                            "initialState": outgoing_transition.initial_state.id,
                            "finalState": outgoing_transition.final_state.id,
                            "source": self.node_id_seq,
                            "target": outgoing_transition.final_state.id,
                            "approvalConditions": [Graph.render_condition(c) for c in approval_transition.condition_set.all()],
                            "approvalCallbacks": [Graph.render_callback(k) for k in approval_transition.callback_set.all()],
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
                        "stateId": state.id,
                        "name": state.name,
                        "type": type,
                        "stateName": state.name,
                        "active": state.active,
                        "initial": state.initial,
                        "variables": [{"id": v.id, "name": v.name} for v in state.variable_definitions.all()]
                    }
                )
                if type != NodeType.JUNCTION:
                    for t in list(state.incoming_transitions.all()) + list(state.outgoing_transitions.all()):
                        links.append(
                            {
                                "id": self.link_id_seq,
                                "transitionId": t.id,
                                "name": t.name,
                                "label": t.label,
                                "initialState": t.initial_state.id if t.initial_state else None,
                                "finalState": t.final_state.id,
                                "source": t.initial_state.id if t.initial_state else None,
                                "target": t.final_state.id,
                                "conditions": [Graph.render_condition(c) for c in
                                    t.condition_set.all()],
                                "callbacks": [Graph.render_callback(k) for k in t.callback_set.all()]

                            }
                        )
        return nodes, links

    def is_connected(self, node_encountered=None, start_node=None, graph=None) -> bool:
        """
        Determines if a graph is connected, recursive function that checks if, starting from a node, a path
        exists from the starting node to the others
        :param node_encountered: set([node])
        :param start_node:
        :param graph: result of nodes_and_links, passed as parameters for performance
        :return:
        """
        if graph is None:
            graph = self.nodes_and_links
        # first time initialize the set
        if node_encountered is None:
            node_encountered = set()
        if not start_node:
            start_node = list(filter(lambda x: x["stateId"] == self.workflow.initial_state.id, graph["nodes"]))[0]
        node_encountered.add(start_node["id"])
        #print(start_node["name"])
        if len(node_encountered) != len(graph["nodes"]):
            outgoing_links = list(filter(lambda link: link["source"] == start_node["id"], graph["links"]))
            #print(len(list(map(lambda link: link["target"], outgoing_links))))
            for node_id in list(map(lambda link: link["target"], outgoing_links)):
                if node_id not in node_encountered:
                    node = list(filter(lambda node: node["id"] == node_id, graph["nodes"]))[0]
                    if self.is_connected(node_encountered, node, graph):
                        return True
        else:
            return True
        #print(len(node_encountered), len(graph["nodes"]))
        return False