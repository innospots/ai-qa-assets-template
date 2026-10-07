// 业务域：客户管理租户上下文（Skill 示例；正式资产见 data/customer/tenants.js）。
output.customer = output.customer || {};
output.customer.tenants = {
  current: {
    description: '当前测试租户',
    code: 'TENANT001'
  },
  other: {
    description: '其他租户，用于隔离验证',
    code: 'TENANT002'
  }
};
