LIST_WORKFLOW_APPROVAL_GRAPH_GQL = '''
query approvalWorkflowList($param: String) {
  approvalWorkflowList(name:$param) {
    edges{
      node {
        id
        name
        approvalGraph
      }
    }
  }
}
'''