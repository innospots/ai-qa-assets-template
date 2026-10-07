// 业务域：创建客户 — 数组批量数据（Skill 示例）。
// 用途：一条 Case 循环多行 records，每行可有不同预期（success / reject）。
// 正式资产可写入 data/customer/customers.js 或独立 data/customer/create-batch.js。
//
// 仓库内同类参照：
// - data/customer/customers.js → customers 对象表
// - data/operations/users-batch.js → insertUsers.records（批量接口）

output.customer = output.customer || {};

output.customer.nameLengthBatch = {
  description: '名称长度边界：同构步骤、不同输入与预期，一条正向/边界 Case 循环执行',
  records: [
    {
      id: 'len1',
      description: '1 个字符应创建成功',
      name: 'A',
      code: 'CUST-BAT-01',
      phone: '13800138000',
      expect: 'success'
    },
    {
      id: 'len100',
      description: '100 个字符应创建成功',
      name: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
      code: 'CUST-BAT-02',
      phone: '13800138000',
      expect: 'success'
    },
    {
      id: 'len101',
      description: '101 个字符应拒绝',
      name: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
      code: 'CUST-BAT-03',
      phone: '13800138000',
      expect: 'reject',
      errorHint: 'name_length'
    }
  ]
};

// 可选：仅顺序 id 列表，详情仍在客户对象表中。
output.customer.nameLengthBatchOrder = ['len1', 'len100', 'len101'];
