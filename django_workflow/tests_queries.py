LIST_WORKFLOWS_GQL = '''
query workflowList {
  workflowList {
    edges{
      node {
        id
        name
        objectType
        initialPrefetch
        initialState {
          id
          name
        }
        initialTransition {
          id
          name
        }
      }
    }
  }
}
'''
LIST_STATES_GQL = '''
query stateList {
  stateList {
    edges{
      node {
        id
        name
        active
        initial
        workflow {
          id
          name
        }
      }
    }
  }
}
'''
CREATE_WORKFLOW_GQL = '''
mutation createWorkflow($input: CreateWorkflowInput!) {
  createWorkflow(input:$input) {
    workflow {
      id
      name
      initialPrefetch
      objectType
    }
  }
}
'''
LIST_TRANSITIONS_GQL = '''
query transitionList($param: ID) {
  transitionList(workflow_Id:$param) {
    edges{
      node {
        id
        name
        initialState {
          id
          name
          active
          initial
          variableDefinitions {
            edges {
              node {
                id
                name
              }
            }
          }
        }
        finalState {
          id
          name
          active
          initial
          variableDefinitions {
            edges {
              node {
                id
                name
              }
            }
          }
        }
        conditionSet {
          edges {
            node {
              id
              conditionType
              functionSet {
                edges {
                  node {
                    id
                    functionModule
                    functionName
                    parameters{
                      edges {
                        node {
                          id
                          name
                          value
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
'''
LIST_WORKFLOW_STATES_GQL = '''
query stateList($param: ID) {
  stateList(workflow_Id:$param) {
    edges{
      node {
        id
        name
        active
        initial
        workflow {
          id
          name
        }
        
      }
    }
  }
}
'''