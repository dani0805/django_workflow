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
                        'approvalGraph': '{"nodes": [{"id": 1, "state_id": 1, "name": "New", "type": "junction", "state_name": "New", "active": true, "variables": []}, {"id": 2, "state_id": 2, "name": "Submitted", "type": "junction", "state_name": "Submitted", "active": true, "variables": []}, {"id": 3, "state_id": 3, "name": "Step 0 Approved", "type": "junction", "state_name": "Step 0 Approved", "active": true, "variables": []}, {"id": 9, "state_id": 4, "name": "Approval Step 0 0", "type": "approval", "state_name": "Submitted for Step 0 Approval", "active": true, "variables": [{"id": 1, "name": "Approval Step 0 0"}]}, {"id": 5, "state_id": 5, "name": "Step 1 Approved", "type": "end", "state_name": "Step 1 Approved", "active": false, "variables": []}, {"id": 10, "state_id": 6, "name": "Approval Step 1 0", "type": "approval", "state_name": "Submitted for Step 1 Approval", "active": true, "variables": [{"id": 2, "name": "Approval Step 1 0"}]}, {"id": 7, "state_id": 7, "name": "Pre Approved", "type": "junction", "state_name": "Pre Approved", "active": true, "variables": []}, {"id": 11, "state_id": 8, "name": "Approval Pre 0", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 12, "state_id": 8, "name": "Approval Pre 1", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 13, "state_id": 8, "name": "Approval Pre 2", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 14, "state_id": 8, "name": "Approval Pre 3", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}], "links": [{"id": 20, "transition_id": 2, "name": "Set In Approval Step 0", "initial_state": 7, "final_state": 4, "start_node": 7, "end_node": 9, "conditions": [], "callbacks": []}, {"id": 21, "transition_id": 5, "approval_transition_id": 3, "name": "Approve Step 0 0", "initial_state": 4, "final_state": 3, "start_node": 9, "end_node": 3, "approval_conditions": [{"id": 1, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 1, "name": "user_ids", "value": "[]"}, {"id": 2, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 1, "name": "variable_name", "value": "Approval Step 0 0"}]}], "conditions": [{"id": 3, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 9, "name": "All Step 1 Approvals Collected", "initial_state": 6, "final_state": 5, "start_node": 6, "end_node": 5, "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 6, "name": "Set In Approval Step 1", "initial_state": 3, "final_state": 6, "start_node": 3, "end_node": 10, "conditions": [], "callbacks": []}, {"id": 23, "transition_id": 9, "approval_transition_id": 7, "name": "Approve Step 1 0", "initial_state": 6, "final_state": 5, "start_node": 10, "end_node": 5, "approval_conditions": [{"id": 4, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 5, "name": "user_ids", "value": "[]"}, {"id": 6, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 2, "name": "variable_name", "value": "Approval Step 1 0"}]}], "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 24, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 11, "conditions": [], "callbacks": []}, {"id": 25, "transition_id": 19, "approval_transition_id": 11, "name": "Approve Pre 0", "initial_state": 8, "final_state": 7, "start_node": 11, "end_node": 7, "approval_conditions": [{"id": 7, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 9, "name": "user_ids", "value": "[1, 2, 3]"}, {"id": 10, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 3, "name": "variable_name", "value": "Approval Pre 0"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 26, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 12, "conditions": [], "callbacks": []}, {"id": 27, "transition_id": 19, "approval_transition_id": 13, "name": "Approve Pre 1", "initial_state": 8, "final_state": 7, "start_node": 12, "end_node": 7, "approval_conditions": [{"id": 9, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 13, "name": "user_ids", "value": "[1]"}, {"id": 14, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 4, "name": "variable_name", "value": "Approval Pre 1"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 28, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 13, "conditions": [], "callbacks": []}, {"id": 29, "transition_id": 19, "approval_transition_id": 15, "name": "Approve Pre 2", "initial_state": 8, "final_state": 7, "start_node": 13, "end_node": 7, "approval_conditions": [{"id": 11, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 17, "name": "user_ids", "value": "[2, 3]"}, {"id": 18, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 5, "name": "variable_name", "value": "Approval Pre 2"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 30, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 14, "conditions": [], "callbacks": []}, {"id": 31, "transition_id": 19, "approval_transition_id": 17, "name": "Approve Pre 3", "initial_state": 8, "final_state": 7, "start_node": 14, "end_node": 7, "approval_conditions": [{"id": 13, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 21, "name": "user_ids", "value": "[2, 3]"}, {"id": 22, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 6, "name": "variable_name", "value": "Approval Pre 3"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}]}',
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
                        'approvalGraph': '{"nodes": [{"id": 1, "state_id": 1, "name": "New", "type": "junction", "state_name": "New", "active": true, "variables": []}, {"id": 2, "state_id": 2, "name": "Submitted", "type": "junction", "state_name": "Submitted", "active": true, "variables": []}, {"id": 3, "state_id": 3, "name": "Step 0 Approved", "type": "junction", "state_name": "Step 0 Approved", "active": true, "variables": []}, {"id": 9, "state_id": 4, "name": "Approval Step 0 0", "type": "approval", "state_name": "Submitted for Step 0 Approval", "active": true, "variables": [{"id": 1, "name": "Approval Step 0 0"}]}, {"id": 5, "state_id": 5, "name": "Step 1 Approved", "type": "end", "state_name": "Step 1 Approved", "active": false, "variables": []}, {"id": 10, "state_id": 6, "name": "Approval Step 1 0", "type": "approval", "state_name": "Submitted for Step 1 Approval", "active": true, "variables": [{"id": 2, "name": "Approval Step 1 0"}]}, {"id": 7, "state_id": 7, "name": "Pre Approved", "type": "junction", "state_name": "Pre Approved", "active": true, "variables": []}, {"id": 11, "state_id": 8, "name": "Approval Pre 0", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 12, "state_id": 8, "name": "Approval Pre 1", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 13, "state_id": 8, "name": "Approval Pre 2", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 14, "state_id": 8, "name": "Approval Pre 3", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 3, "name": "Approval Pre 0"}, {"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}], "links": [{"id": 20, "transition_id": 2, "name": "Set In Approval Step 0", "initial_state": 7, "final_state": 4, "start_node": 7, "end_node": 9, "conditions": [], "callbacks": []}, {"id": 21, "transition_id": 5, "approval_transition_id": 3, "name": "Approve Step 0 0", "initial_state": 4, "final_state": 3, "start_node": 9, "end_node": 3, "approval_conditions": [{"id": 1, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 1, "name": "user_ids", "value": "[]"}, {"id": 2, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 1, "name": "variable_name", "value": "Approval Step 0 0"}]}], "conditions": [{"id": 3, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 9, "name": "All Step 1 Approvals Collected", "initial_state": 6, "final_state": 5, "start_node": 6, "end_node": 5, "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 6, "name": "Set In Approval Step 1", "initial_state": 3, "final_state": 6, "start_node": 3, "end_node": 10, "conditions": [], "callbacks": []}, {"id": 23, "transition_id": 9, "approval_transition_id": 7, "name": "Approve Step 1 0", "initial_state": 6, "final_state": 5, "start_node": 10, "end_node": 5, "approval_conditions": [{"id": 4, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 5, "name": "user_ids", "value": "[]"}, {"id": 6, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 2, "name": "variable_name", "value": "Approval Step 1 0"}]}], "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 24, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 11, "conditions": [], "callbacks": []}, {"id": 25, "transition_id": 19, "approval_transition_id": 11, "name": "Approve Pre 0", "initial_state": 8, "final_state": 7, "start_node": 11, "end_node": 7, "approval_conditions": [{"id": 7, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 9, "name": "user_ids", "value": "[1, 2, 3]"}, {"id": 10, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 3, "name": "variable_name", "value": "Approval Pre 0"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 26, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 12, "conditions": [], "callbacks": []}, {"id": 27, "transition_id": 19, "approval_transition_id": 13, "name": "Approve Pre 1", "initial_state": 8, "final_state": 7, "start_node": 12, "end_node": 7, "approval_conditions": [{"id": 9, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 13, "name": "user_ids", "value": "[1]"}, {"id": 14, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 4, "name": "variable_name", "value": "Approval Pre 1"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 28, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 13, "conditions": [], "callbacks": []}, {"id": 29, "transition_id": 19, "approval_transition_id": 15, "name": "Approve Pre 2", "initial_state": 8, "final_state": 7, "start_node": 13, "end_node": 7, "approval_conditions": [{"id": 11, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 17, "name": "user_ids", "value": "[2, 3]"}, {"id": 18, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 5, "name": "variable_name", "value": "Approval Pre 2"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 30, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 14, "conditions": [], "callbacks": []}, {"id": 31, "transition_id": 19, "approval_transition_id": 17, "name": "Approve Pre 3", "initial_state": 8, "final_state": 7, "start_node": 14, "end_node": 7, "approval_conditions": [{"id": 13, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 21, "name": "user_ids", "value": "[2, 3]"}, {"id": 22, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 6, "name": "variable_name", "value": "Approval Pre 3"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}]}',
                        'id': 'QXBwcm92YWxXb3JrZmxvd05vZGU6MQ==',
                        'name': 'Test_Workflow'
                    }
                }
            ]
        }
    }
}

snapshots['WorkflowTest::test_modify_workflow 2'] = {
    'data': {
        'approvalWorkflowList': {
            'edges': [
                {
                    'node': {
                        'approvalGraph': '{"nodes": [{"id": 1, "state_id": 1, "name": "New", "type": "junction", "state_name": "New", "active": true, "variables": []}, {"id": 2, "state_id": 2, "name": "Submitted", "type": "junction", "state_name": "Submitted", "active": true, "variables": []}, {"id": 3, "state_id": 3, "name": "Step 0 Approved", "type": "junction", "state_name": "Step 0 Approved", "active": true, "variables": []}, {"id": 9, "state_id": 4, "name": "Approval Step 0 0", "type": "approval", "state_name": "Submitted for Step 0 Approval", "active": true, "variables": [{"id": 1, "name": "Approval Step 0 0"}]}, {"id": 5, "state_id": 5, "name": "Step 1 Approved", "type": "end", "state_name": "Step 1 Approved", "active": false, "variables": []}, {"id": 10, "state_id": 6, "name": "Approval Step 1 0", "type": "approval", "state_name": "Submitted for Step 1 Approval", "active": true, "variables": [{"id": 2, "name": "Approval Step 1 0"}]}, {"id": 7, "state_id": 7, "name": "Pre Approved", "type": "junction", "state_name": "Pre Approved", "active": true, "variables": []}, {"id": 11, "state_id": 8, "name": "Approval Pre 1", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 12, "state_id": 8, "name": "Approval Pre 2", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}, {"id": 13, "state_id": 8, "name": "Approval Pre 3", "type": "approval", "state_name": "Submitted for Pre Approval", "active": true, "variables": [{"id": 4, "name": "Approval Pre 1"}, {"id": 5, "name": "Approval Pre 2"}, {"id": 6, "name": "Approval Pre 3"}]}], "links": [{"id": 20, "transition_id": 2, "name": "Set In Approval Step 0", "initial_state": 7, "final_state": 4, "start_node": 7, "end_node": 9, "conditions": [], "callbacks": []}, {"id": 21, "transition_id": 5, "approval_transition_id": 3, "name": "Approve Step 0 0", "initial_state": 4, "final_state": 3, "start_node": 9, "end_node": 3, "approval_conditions": [{"id": 1, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 1, "name": "user_ids", "value": "[]"}, {"id": 2, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 1, "name": "variable_name", "value": "Approval Step 0 0"}]}], "conditions": [{"id": 3, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 9, "name": "All Step 1 Approvals Collected", "initial_state": 6, "final_state": 5, "start_node": 6, "end_node": 5, "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 6, "name": "Set In Approval Step 1", "initial_state": 3, "final_state": 6, "start_node": 3, "end_node": 10, "conditions": [], "callbacks": []}, {"id": 23, "transition_id": 9, "approval_transition_id": 7, "name": "Approve Step 1 0", "initial_state": 6, "final_state": 5, "start_node": 10, "end_node": 5, "approval_conditions": [{"id": 4, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 5, "name": "user_ids", "value": "[]"}, {"id": 6, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 2, "name": "variable_name", "value": "Approval Step 1 0"}]}], "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 24, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 11, "conditions": [], "callbacks": []}, {"id": 25, "transition_id": 19, "approval_transition_id": 13, "name": "Approve Pre 1", "initial_state": 8, "final_state": 7, "start_node": 11, "end_node": 7, "approval_conditions": [{"id": 9, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 13, "name": "user_ids", "value": "[1]"}, {"id": 14, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 4, "name": "variable_name", "value": "Approval Pre 1"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 26, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 12, "conditions": [], "callbacks": []}, {"id": 27, "transition_id": 19, "approval_transition_id": 15, "name": "Approve Pre 2", "initial_state": 8, "final_state": 7, "start_node": 12, "end_node": 7, "approval_conditions": [{"id": 11, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 17, "name": "user_ids", "value": "[2, 3]"}, {"id": 18, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 5, "name": "variable_name", "value": "Approval Pre 2"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 28, "transition_id": 10, "name": "Set In Approval Pre", "initial_state": 2, "final_state": 8, "start_node": 2, "end_node": 13, "conditions": [], "callbacks": []}, {"id": 29, "transition_id": 19, "approval_transition_id": 17, "name": "Approve Pre 3", "initial_state": 8, "final_state": 7, "start_node": 13, "end_node": 7, "approval_conditions": [{"id": 13, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 21, "name": "user_ids", "value": "[2, 3]"}, {"id": 22, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 6, "name": "variable_name", "value": "Approval Pre 3"}]}], "conditions": [{"id": 15, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}]}',
                        'id': 'QXBwcm92YWxXb3JrZmxvd05vZGU6MQ==',
                        'name': 'Test_Workflow'
                    }
                }
            ]
        }
    }
}

snapshots['WorkflowTest::test_modify_workflow 3'] = {
    'data': {
        'approvalWorkflowList': {
            'edges': [
                {
                    'node': {
                        'approvalGraph': '{"nodes": [{"id": 1, "state_id": 1, "name": "New", "type": "junction", "state_name": "New", "active": true, "variables": []}, {"id": 2, "state_id": 2, "name": "Submitted", "type": "junction", "state_name": "Submitted", "active": true, "variables": []}, {"id": 3, "state_id": 3, "name": "Step 0 Approved", "type": "junction", "state_name": "Step 0 Approved", "active": true, "variables": []}, {"id": 8, "state_id": 4, "name": "Approval Step 0 0", "type": "approval", "state_name": "Submitted for Step 0 Approval", "active": true, "variables": [{"id": 1, "name": "Approval Step 0 0"}]}, {"id": 5, "state_id": 5, "name": "Step 1 Approved", "type": "end", "state_name": "Step 1 Approved", "active": false, "variables": []}, {"id": 9, "state_id": 6, "name": "Approval Step 1 0", "type": "approval", "state_name": "Submitted for Step 1 Approval", "active": true, "variables": [{"id": 2, "name": "Approval Step 1 0"}]}, {"id": 7, "state_id": 7, "name": "Pre Approved", "type": "junction", "state_name": "Pre Approved", "active": true, "variables": []}], "links": [{"id": 20, "transition_id": 2, "name": "Set In Approval Step 0", "initial_state": 7, "final_state": 4, "start_node": 7, "end_node": 8, "conditions": [], "callbacks": []}, {"id": 21, "transition_id": 5, "approval_transition_id": 3, "name": "Approve Step 0 0", "initial_state": 4, "final_state": 3, "start_node": 8, "end_node": 3, "approval_conditions": [{"id": 1, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 1, "name": "user_ids", "value": "[]"}, {"id": 2, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 1, "name": "variable_name", "value": "Approval Step 0 0"}]}], "conditions": [{"id": 3, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 9, "name": "All Step 1 Approvals Collected", "initial_state": 6, "final_state": 5, "start_node": 6, "end_node": 5, "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}, {"id": 22, "transition_id": 6, "name": "Set In Approval Step 1", "initial_state": 3, "final_state": 6, "start_node": 3, "end_node": 9, "conditions": [], "callbacks": []}, {"id": 23, "transition_id": 9, "approval_transition_id": 7, "name": "Approve Step 1 0", "initial_state": 6, "final_state": 5, "start_node": 9, "end_node": 5, "approval_conditions": [{"id": 4, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "is_approver", "parameters": [{"id": 5, "name": "user_ids", "value": "[]"}, {"id": 6, "name": "roles", "value": "[]"}]}], "sub_conditions": []}], "approval_callbacks": [{"module": "simple_approval.callbacks", "name": "on_approval", "parameters": [{"id": 2, "name": "variable_name", "value": "Approval Step 1 0"}]}], "conditions": [{"id": 6, "type": "function", "functions": [{"module": "simple_approval.conditions", "name": "all_approvals_collected", "parameters": []}], "sub_conditions": []}], "callbacks": []}]}',
                        'id': 'QXBwcm92YWxXb3JrZmxvd05vZGU6MQ==',
                        'name': 'Test_Workflow'
                    }
                }
            ]
        }
    }
}
