# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['WorkflowTest::test_api 1'] = {
    'data': {
        'approvalWorkflowList': {
            'edges': [
                {
                    'node': {
                        'approvalGraph': '{"nodes": [{"id": 1, "stateId": 1, "name": "New", "type": "junction", "stateName": "New", "active": true, "initial": true, "variables": []}, {"id": 2, "stateId": 2, "name": "Step 0 Approved", "type": "junction", "stateName": "Step 0 Approved", "active": true, "initial": false, "variables": []}, {"id": 3, "stateId": 3, "name": "Submitted for Step 0 Approval", "type": "junction", "stateName": "Submitted for Step 0 Approval", "active": true, "initial": false, "variables": [{"id": 1, "name": "Approval Step 0 0"}]}, {"id": 4, "stateId": 4, "name": "Approved", "type": "junction", "stateName": "Approved", "active": true, "initial": false, "variables": [{"id": 3, "name": "approved"}]}, {"id": 14, "stateId": 5, "name": "Approval Step 1 0", "type": "approval", "stateName": "Submitted for Step 1 Approval", "active": true, "initial": false, "variables": [{"id": 2, "name": "Approval Step 1 0"}]}, {"id": 6, "stateId": 6, "name": "Archived", "type": "end", "stateName": "Archived", "active": false, "initial": false, "variables": [{"id": 4, "name": "archived"}]}, {"id": 7, "stateId": 7, "name": "Pre Approved", "type": "junction", "stateName": "Pre Approved", "active": true, "initial": false, "variables": []}, {"id": 15, "stateId": 8, "name": "Approval Pre 0", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}, {"id": 16, "stateId": 8, "name": "Approval Pre 1", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}, {"id": 17, "stateId": 8, "name": "Approval Pre 2", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}, {"id": 18, "stateId": 8, "name": "Approval Pre 3", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}], "links": [{"id": 30, "transitionId": 5, "name": "Set In Approval Step 1", "label": null, "initialState": 2, "finalState": 5, "source": 2, "target": 14, "conditions": [], "callbacks": []}, {"id": 31, "transition_id": 8, "approval_transition_id": 6, "name": "Approve-1-5bdad55472eaf40b78e868f84b323a1d9", "label": "Approve", "initialState": 5, "finalState": 4, "source": 14, "target": 4, "approvalConditions": [{"id": 8, "type": "and", "functions": [], "sub_conditions": [{"id": 9, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 5, "name": "user_ids", "value": "[1, 2]", "function": 6, "workflow": 1}, {"id": 6, "name": "roles", "value": "[]", "function": 6, "workflow": 1}]}], "sub_conditions": []}, {"id": 10, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 2, "name": "variable_name", "value": "Approval Step 1 0"}]}], "conditions": [{"id": 14, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 32, "transitionId": 9, "name": "Archive", "label": null, "initialState": 4, "finalState": 6, "source": 4, "target": 6, "conditions": [], "callbacks": []}, {"id": 32, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 15, "conditions": [], "callbacks": []}, {"id": 33, "transition_id": 19, "approval_transition_id": 11, "name": "Approve-1-84f5e99a4101c4eec979c5c509d27472a", "label": "Approve", "initialState": 8, "finalState": 7, "source": 15, "target": 7, "approvalConditions": [{"id": 15, "type": "and", "functions": [], "sub_conditions": [{"id": 16, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 9, "name": "user_ids", "value": "[1, 2, 3]", "function": 11, "workflow": 1}, {"id": 10, "name": "roles", "value": "[]", "function": 11, "workflow": 1}]}], "sub_conditions": []}, {"id": 17, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 3, "name": "variable_name", "value": "Approval Pre 0"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 34, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 16, "conditions": [], "callbacks": []}, {"id": 35, "transition_id": 19, "approval_transition_id": 13, "name": "Approve-1-827cd28399d8b489d9ba349640e9a9bdf", "label": "Approve", "initialState": 8, "finalState": 7, "source": 16, "target": 7, "approvalConditions": [{"id": 21, "type": "and", "functions": [], "sub_conditions": [{"id": 22, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 13, "name": "user_ids", "value": "[1]", "function": 15, "workflow": 1}, {"id": 14, "name": "roles", "value": "[]", "function": 15, "workflow": 1}]}], "sub_conditions": []}, {"id": 23, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 4, "name": "variable_name", "value": "Approval Pre 1"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 36, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 17, "conditions": [], "callbacks": []}, {"id": 37, "transition_id": 19, "approval_transition_id": 15, "name": "Approve-1-827ae6d3d0c804da286ada2bd898cafb6", "label": "Approve", "initialState": 8, "finalState": 7, "source": 17, "target": 7, "approvalConditions": [{"id": 27, "type": "and", "functions": [], "sub_conditions": [{"id": 28, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 17, "name": "user_ids", "value": "[2, 3]", "function": 19, "workflow": 1}, {"id": 18, "name": "roles", "value": "[]", "function": 19, "workflow": 1}]}], "sub_conditions": []}, {"id": 29, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 5, "name": "variable_name", "value": "Approval Pre 2"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 38, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 18, "conditions": [], "callbacks": []}, {"id": 39, "transition_id": 19, "approval_transition_id": 17, "name": "Approve-1-883d2861adaf74648a5ca9c9e6544a3b1", "label": "Approve", "initialState": 8, "finalState": 7, "source": 18, "target": 7, "approvalConditions": [{"id": 33, "type": "and", "functions": [], "sub_conditions": [{"id": 34, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 21, "name": "user_ids", "value": "[2, 3]", "function": 23, "workflow": 1}, {"id": 22, "name": "roles", "value": "[]", "function": 23, "workflow": 1}]}], "sub_conditions": []}, {"id": 35, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 6, "name": "variable_name", "value": "Approval Pre 3"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}]}',
                        'id': 'QXBwcm92YWxXb3JrZmxvd05vZGU6MQ==',
                        'name': 'Test_Workflow'
                    }
                }
            ]
        }
    }
}

snapshots['WorkflowTest::test_modify_workflow 1'] = {
    'data': {
        'approvalWorkflowList': {
            'edges': [
                {
                    'node': {
                        'approvalGraph': '{"nodes": [{"id": 1, "stateId": 1, "name": "New", "type": "junction", "stateName": "New", "active": true, "initial": true, "variables": []}, {"id": 2, "stateId": 2, "name": "Step 0 Approved", "type": "junction", "stateName": "Step 0 Approved", "active": true, "initial": false, "variables": []}, {"id": 3, "stateId": 3, "name": "Submitted for Step 0 Approval", "type": "junction", "stateName": "Submitted for Step 0 Approval", "active": true, "initial": false, "variables": [{"id": 1, "name": "Approval Step 0 0"}]}, {"id": 4, "stateId": 4, "name": "Approved", "type": "junction", "stateName": "Approved", "active": true, "initial": false, "variables": [{"id": 3, "name": "approved"}]}, {"id": 14, "stateId": 5, "name": "Approval Step 1 0", "type": "approval", "stateName": "Submitted for Step 1 Approval", "active": true, "initial": false, "variables": [{"id": 2, "name": "Approval Step 1 0"}]}, {"id": 6, "stateId": 6, "name": "Archived", "type": "end", "stateName": "Archived", "active": false, "initial": false, "variables": [{"id": 4, "name": "archived"}]}, {"id": 7, "stateId": 7, "name": "Pre Approved", "type": "junction", "stateName": "Pre Approved", "active": true, "initial": false, "variables": []}, {"id": 15, "stateId": 8, "name": "Approval Pre 0", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}, {"id": 16, "stateId": 8, "name": "Approval Pre 1", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}, {"id": 17, "stateId": 8, "name": "Approval Pre 2", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}, {"id": 18, "stateId": 8, "name": "Approval Pre 3", "type": "approval", "stateName": "Submitted for Pre Approval", "active": true, "initial": false, "variables": [{"id": 5, "name": "Approval Pre 0"}, {"id": 6, "name": "Approval Pre 1"}, {"id": 7, "name": "Approval Pre 2"}, {"id": 8, "name": "Approval Pre 3"}]}], "links": [{"id": 30, "transitionId": 5, "name": "Set In Approval Step 1", "label": null, "initialState": 2, "finalState": 5, "source": 2, "target": 14, "conditions": [], "callbacks": []}, {"id": 31, "transition_id": 8, "approval_transition_id": 6, "name": "Approve-1-5d969c8299a0642a490fcaf172cadd10f", "label": "Approve", "initialState": 5, "finalState": 4, "source": 14, "target": 4, "approvalConditions": [{"id": 8, "type": "and", "functions": [], "sub_conditions": [{"id": 9, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 5, "name": "user_ids", "value": "[1, 2]", "function": 6, "workflow": 1}, {"id": 6, "name": "roles", "value": "[]", "function": 6, "workflow": 1}]}], "sub_conditions": []}, {"id": 10, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 2, "name": "variable_name", "value": "Approval Step 1 0"}]}], "conditions": [{"id": 14, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 32, "transitionId": 9, "name": "Archive", "label": null, "initialState": 4, "finalState": 6, "source": 4, "target": 6, "conditions": [], "callbacks": []}, {"id": 32, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 15, "conditions": [], "callbacks": []}, {"id": 33, "transition_id": 19, "approval_transition_id": 11, "name": "Approve-1-80a064c5e1e1a4af3b94b4d5bc1ff6ef4", "label": "Approve", "initialState": 8, "finalState": 7, "source": 15, "target": 7, "approvalConditions": [{"id": 15, "type": "and", "functions": [], "sub_conditions": [{"id": 16, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 9, "name": "user_ids", "value": "[1, 2, 3]", "function": 11, "workflow": 1}, {"id": 10, "name": "roles", "value": "[]", "function": 11, "workflow": 1}]}], "sub_conditions": []}, {"id": 17, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 3, "name": "variable_name", "value": "Approval Pre 0"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 34, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 16, "conditions": [], "callbacks": []}, {"id": 35, "transition_id": 19, "approval_transition_id": 13, "name": "Approve-1-8edbf9f6bfcf84ee9bcbe1ae03b4b4a44", "label": "Approve", "initialState": 8, "finalState": 7, "source": 16, "target": 7, "approvalConditions": [{"id": 21, "type": "and", "functions": [], "sub_conditions": [{"id": 22, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 13, "name": "user_ids", "value": "[1]", "function": 15, "workflow": 1}, {"id": 14, "name": "roles", "value": "[]", "function": 15, "workflow": 1}]}], "sub_conditions": []}, {"id": 23, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 4, "name": "variable_name", "value": "Approval Pre 1"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 36, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 17, "conditions": [], "callbacks": []}, {"id": 37, "transition_id": 19, "approval_transition_id": 15, "name": "Approve-1-8a0953269aa1546ea933ddb54ed830e81", "label": "Approve", "initialState": 8, "finalState": 7, "source": 17, "target": 7, "approvalConditions": [{"id": 27, "type": "and", "functions": [], "sub_conditions": [{"id": 28, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 17, "name": "user_ids", "value": "[2, 3]", "function": 19, "workflow": 1}, {"id": 18, "name": "roles", "value": "[]", "function": 19, "workflow": 1}]}], "sub_conditions": []}, {"id": 29, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 5, "name": "variable_name", "value": "Approval Pre 2"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 38, "transitionId": 10, "name": "Set In Approval Pre", "label": null, "initialState": 3, "finalState": 8, "source": 3, "target": 18, "conditions": [], "callbacks": []}, {"id": 39, "transition_id": 19, "approval_transition_id": 17, "name": "Approve-1-80b8f8b73883641dc8025f41611c098c5", "label": "Approve", "initialState": 8, "finalState": 7, "source": 18, "target": 7, "approvalConditions": [{"id": 33, "type": "and", "functions": [], "sub_conditions": [{"id": 34, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 21, "name": "user_ids", "value": "[2, 3]", "function": 23, "workflow": 1}, {"id": 22, "name": "roles", "value": "[]", "function": 23, "workflow": 1}]}], "sub_conditions": []}, {"id": 35, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_not_approved", "parameters": []}], "sub_conditions": []}]}], "approvalCallbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 6, "name": "variable_name", "value": "Approval Pre 3"}]}], "conditions": [{"id": 39, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}]}',
                        'id': 'QXBwcm92YWxXb3JrZmxvd05vZGU6MQ==',
                        'name': 'Test_Workflow'
                    }
                }
            ]
        }
    }
}
