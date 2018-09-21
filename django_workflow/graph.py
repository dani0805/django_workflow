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
                "conditions": [Graph.render_condition(c) for c in t.condition_set.all()],
                "callbacks": [Graph.render_callback(k) for k in t.callback_set.all()]

            }
            for t in self.workflow.transition_set.all()
        ]
        return {"nodes": nodes, "links":links}

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
                    "value": p.value
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
