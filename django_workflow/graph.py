from django_workflow.models import Workflow, Condition, Function, Callback


class Graph:

    def __init__(self, workflow: Workflow):
        self.workflow = workflow

    @property
    def nodes_and_links(self) -> dict:
        nodes = [
            {
                "id": s.id,
                "name": s.name,
                "active": s.active,
                "variables": [{"id": v.id, "name": v.name} for v in s.variable_definitions.all()]
            }
            for s in self.workflow.state_set.all()
        ]
        links = [
            {
                "id": t.id,
                "name": t.name,
                "label": t.label,
                "initial_state": t.initial_state.id if t.initial_state else None,
                "final_state": t.final_state.id,
                "conditions": [Graph.render_condition(c) for c in t.condition_set.all()],
                "callbacks": [Graph.render_callback(k) for k in t.callback_set.all()]

            }
            for t in self.workflow.transition_set.all()
        ]
        return {"nodes": nodes, "links":links}

    def is_connected(self, node_encoutered = None, start_node=None, graph=None) -> bool:
        """
        Determines if a graph is connected, recursive function that checks if, starting from a node, a path
        exists from the starting node to the others
        :param node_encoutered: set([node])
        :param start_node:
        :param graph: result of nodes_and_links, passed as parameters for performance
        :return:
        """
        if graph is None:
            graph = self.nodes_and_links
        # first time initialize the set
        if node_encoutered is None:
            node_encoutered = set()
        if not start_node:
            start_node = graph["nodes"][0]
        node_encoutered.add(start_node["id"])
        if len(node_encoutered) != len(graph["nodes"]):
            outgoing_links = filter(lambda link: link["source"] == start_node["id"], graph["links"])
            for node_id in list(map(lambda link: link["target"], outgoing_links)):
                if node_id not in node_encoutered:
                    node = list(filter(lambda node: node["id"] == node_id, graph["nodes"]))[0]
                    if self.is_connected(node_encoutered, node, graph):
                        return True
        else:
            return True
        return False


    @staticmethod
    def render_condition(condition: Condition) -> dict:
        condition_dict = {
            "id": condition.id,
            "type": condition.condition_type,
            "functions": [ Graph.render_function(f) for f in condition.function_set.all()],
            "sub_conditions": [ Graph.render_condition(c) for c in condition.child_conditions.all()]
        }
        return condition_dict

    @staticmethod
    def render_function(function: Function) -> dict:
        function_dict = {
            "module": function.function_module,
            "name": function.function_name,
            "parameters": [
                {
                    "id": p.id,
                    "name": p.name,
                    "value": p.value,
                    "function": p.function_id,
                    "workflow": p.workflow_id
                }
                for p in function.parameters.all()
            ]
        }
        return function_dict

    @staticmethod
    def render_callback(callback:Callback) -> dict:
        callback_dict = {
            "module": callback.function_module,
            "name": callback.function_name,
            "parameters": [
                {
                    "id": p.id,
                    "name": p.name,
                    "value": p.value
                }
                for p in callback.parameters.all()
            ]
        }
        return callback_dict
