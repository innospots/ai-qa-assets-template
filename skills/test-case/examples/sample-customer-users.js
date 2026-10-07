// 业务域：客户管理测试用户（Skill 示例；正式资产见 data/customer/users.js）。
output.customer = output.customer || {};
output.customer.users = {
  operator: {
    description: '有创建/修改权限的运营人员',
    username: 'operator01',
    role: 'operator',
    tenant: 'TENANT001'
  },
  viewer: {
    description: '仅查看，无创建权限',
    username: 'viewer01',
    role: 'viewer',
    tenant: 'TENANT001'
  },
  otherTenantOperator: {
    description: '其他租户运营人员，用于跨租户拒绝验证',
    username: 'operator02',
    role: 'operator',
    tenant: 'TENANT002'
  }
};
