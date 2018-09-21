# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['WorkflowTest::test_api 2'] = {
    'data': {
        'stateList': {
            'edges': [
                {
                    'node': {
                        'active': True,
                        'id': 'U3RhdGVOb2RlOjE=',
                        'initial': True,
                        'name': 'state 1',
                        'workflow': {
                            'id': 'V29ya2Zsb3dOb2RlOjE=',
                            'name': 'Test_Workflow'
                        }
                    }
                },
                {
                    'node': {
                        'active': True,
                        'id': 'U3RhdGVOb2RlOjI=',
                        'initial': False,
                        'name': 'state 2',
                        'workflow': {
                            'id': 'V29ya2Zsb3dOb2RlOjE=',
                            'name': 'Test_Workflow'
                        }
                    }
                },
                {
                    'node': {
                        'active': False,
                        'id': 'U3RhdGVOb2RlOjM=',
                        'initial': False,
                        'name': 'state 3',
                        'workflow': {
                            'id': 'V29ya2Zsb3dOb2RlOjE=',
                            'name': 'Test_Workflow'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['WorkflowTest::test_api 3'] = {
    'data': {
        'stateList': {
            'edges': [
                {
                    'node': {
                        'active': True,
                        'id': 'U3RhdGVOb2RlOjE=',
                        'initial': True,
                        'name': 'state 1',
                        'workflow': {
                            'id': 'V29ya2Zsb3dOb2RlOjE=',
                            'name': 'Test_Workflow'
                        }
                    }
                },
                {
                    'node': {
                        'active': True,
                        'id': 'U3RhdGVOb2RlOjI=',
                        'initial': False,
                        'name': 'state 2',
                        'workflow': {
                            'id': 'V29ya2Zsb3dOb2RlOjE=',
                            'name': 'Test_Workflow'
                        }
                    }
                },
                {
                    'node': {
                        'active': False,
                        'id': 'U3RhdGVOb2RlOjM=',
                        'initial': False,
                        'name': 'state 3',
                        'workflow': {
                            'id': 'V29ya2Zsb3dOb2RlOjE=',
                            'name': 'Test_Workflow'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['WorkflowTest::test_api 1'] = {
    'data': {
        'workflowList': {
            'edges': [
                {
                    'node': {
                        'id': 'V29ya2Zsb3dOb2RlOjE=',
                        'initialPrefetch': '''
                             {
                                "username":"admin",
                                "date_joined__gte":"today - 24*3600"
                             }
                             ''',
                        'initialState': {
                            'id': 'U3RhdGVOb2RlOjE=',
                            'name': 'state 1'
                        },
                        'initialTransition': {
                            'id': 'VHJhbnNpdGlvbk5vZGU6MQ==',
                            'name': 'auto_initial'
                        },
                        'name': 'Test_Workflow',
                        'objectType': 'django.contrib.auth.models.User'
                    }
                }
            ]
        }
    }
}

snapshots['WorkflowTest::test_api 4'] = {
    'data': {
        'transitionList': {
            'edges': [
                {
                    'node': {
                        'conditionSet': {
                            'edges': [
                                {
                                    'node': {
                                        'conditionType': 'FUNCTION',
                                        'functionSet': {
                                            'edges': [
                                                {
                                                    'node': {
                                                        'functionModule': 'django_workflow.conditions',
                                                        'functionName': 'object_attribute_value',
                                                        'id': 'RnVuY3Rpb25Ob2RlOjI=',
                                                        'parameters': {
                                                            'edges': [
                                                                {
                                                                    'node': {
                                                                        'id': 'RnVuY3Rpb25QYXJhbWV0ZXJOb2RlOjM=',
                                                                        'name': 'attribute_name',
                                                                        'value': 'username'
                                                                    }
                                                                },
                                                                {
                                                                    'node': {
                                                                        'id': 'RnVuY3Rpb25QYXJhbWV0ZXJOb2RlOjQ=',
                                                                        'name': 'attribute_value',
                                                                        'value': '{{ object.username }}'
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    }
                                                }
                                            ]
                                        },
                                        'id': 'Q29uZGl0aW9uTm9kZToy'
                                    }
                                }
                            ]
                        },
                        'finalState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjE=',
                            'initial': True,
                            'name': 'state 1',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'id': 'VHJhbnNpdGlvbk5vZGU6MQ==',
                        'initialState': None,
                        'name': 'auto_initial'
                    }
                },
                {
                    'node': {
                        'conditionSet': {
                            'edges': [
                            ]
                        },
                        'finalState': {
                            'active': False,
                            'id': 'U3RhdGVOb2RlOjM=',
                            'initial': False,
                            'name': 'state 3',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'id': 'VHJhbnNpdGlvbk5vZGU6NA==',
                        'initialState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjE=',
                            'initial': True,
                            'name': 'state 1',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'name': 'manual_1'
                    }
                },
                {
                    'node': {
                        'conditionSet': {
                            'edges': [
                                {
                                    'node': {
                                        'conditionType': 'FUNCTION',
                                        'functionSet': {
                                            'edges': [
                                                {
                                                    'node': {
                                                        'functionModule': 'django_workflow.conditions',
                                                        'functionName': 'object_attribute_value',
                                                        'id': 'RnVuY3Rpb25Ob2RlOjE=',
                                                        'parameters': {
                                                            'edges': [
                                                                {
                                                                    'node': {
                                                                        'id': 'RnVuY3Rpb25QYXJhbWV0ZXJOb2RlOjE=',
                                                                        'name': 'attribute_name',
                                                                        'value': 'is_superuser'
                                                                    }
                                                                },
                                                                {
                                                                    'node': {
                                                                        'id': 'RnVuY3Rpb25QYXJhbWV0ZXJOb2RlOjI=',
                                                                        'name': 'attribute_value',
                                                                        'value': 'True'
                                                                    }
                                                                }
                                                            ]
                                                        }
                                                    }
                                                }
                                            ]
                                        },
                                        'id': 'Q29uZGl0aW9uTm9kZTox'
                                    }
                                }
                            ]
                        },
                        'finalState': {
                            'active': False,
                            'id': 'U3RhdGVOb2RlOjM=',
                            'initial': False,
                            'name': 'state 3',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'id': 'VHJhbnNpdGlvbk5vZGU6Ng==',
                        'initialState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjI=',
                            'initial': False,
                            'name': 'state 2',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'name': 'manual_2'
                    }
                },
                {
                    'node': {
                        'conditionSet': {
                            'edges': [
                            ]
                        },
                        'finalState': {
                            'active': False,
                            'id': 'U3RhdGVOb2RlOjM=',
                            'initial': False,
                            'name': 'state 3',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'id': 'VHJhbnNpdGlvbk5vZGU6Mw==',
                        'initialState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjE=',
                            'initial': True,
                            'name': 'state 1',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'name': 'auto_slow'
                    }
                },
                {
                    'node': {
                        'conditionSet': {
                            'edges': [
                            ]
                        },
                        'finalState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjI=',
                            'initial': False,
                            'name': 'state 2',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'id': 'VHJhbnNpdGlvbk5vZGU6NQ==',
                        'initialState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjI=',
                            'initial': False,
                            'name': 'state 2',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'name': 'auto_self'
                    }
                },
                {
                    'node': {
                        'conditionSet': {
                            'edges': [
                            ]
                        },
                        'finalState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjI=',
                            'initial': False,
                            'name': 'state 2',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'id': 'VHJhbnNpdGlvbk5vZGU6Mg==',
                        'initialState': {
                            'active': True,
                            'id': 'U3RhdGVOb2RlOjE=',
                            'initial': True,
                            'name': 'state 1',
                            'variableDefinitions': {
                                'edges': [
                                ]
                            }
                        },
                        'name': 'auto_fast'
                    }
                }
            ]
        }
    }
}

snapshots['WorkflowTest::test_api 5'] = {
    'data': {
        'createWorkflow': {
            'workflow': {
                'id': 'V29ya2Zsb3dOb2RlOjI=',
                'initialPrefetch': '',
                'name': 'Test 2 WF',
                'objectType': 'django.contrib.auth.User'
            }
        }
    }
}
