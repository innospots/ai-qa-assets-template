// 业务域：创建客户场景数据集（Skill 示例；正式资产见 data/customer/customers.js）。
output.customer = output.customer || {};
output.customer.customers = {
  validFull: {
    description: '全部字段合法且编号未占用',
    name: '测试客户A',
    code: 'CUST001',
    phone: '13800138000'
  },
  requiredOnly: {
    description: '仅必填字段，手机号为空',
    name: '测试客户B',
    code: 'CUST002',
    phone: null
  },
  emptyName: {
    description: '名称为空，反向校验',
    name: '',
    code: 'CUST101',
    phone: '13800138000'
  },
  emptyCode: {
    description: '编号为空，反向校验',
    name: '测试客户',
    code: '',
    phone: '13800138000'
  },
  existing: {
    description: '已存在客户，用于编号重复',
    name: '已有客户',
    code: 'CUST_EXIST',
    phone: '13800138000',
    status: 'NORMAL'
  },
  duplicateCode: {
    description: '与 existing 同编号的新资料',
    name: '新客户',
    code: 'CUST_EXIST',
    phone: '13900139000'
  },
  invalidPhone: {
    description: '手机号格式非法',
    name: '手机号异常客户',
    code: 'CUST104',
    phone: '123'
  },
  validPermission: {
    description: '权限场景用合法客户资料',
    name: '权限测试客户',
    code: 'CUST105',
    phone: '13800138000'
  },
  idempotent: {
    description: '连续重复提交相同资料',
    name: '重复提交客户',
    code: 'CUST106',
    phone: '13800138000'
  },
  timeoutRetry: {
    description: '首次超时后相同编号重试',
    name: '超时重试客户',
    code: 'CUST107',
    phone: '13800138000'
  },
  nameLength1: {
    description: '名称长度边界 1',
    name: 'A',
    code: 'CUST20101',
    phone: '13800138000'
  },
  nameLength100: {
    description: '名称长度边界 100',
    name: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    code: 'CUST20102',
    phone: '13800138000'
  },
  nameLength101: {
    description: '名称长度边界 101，应拒绝',
    name: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    code: 'CUST20103',
    phone: '13800138000'
  },
  codeLength1: {
    description: '编号长度边界 1',
    name: '编号最小边界客户',
    code: 'C',
    phone: '13800138000'
  },
  codeLength32: {
    description: '编号长度边界 32',
    name: '编号最大边界客户',
    code: 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
    phone: '13800138000'
  },
  codeLength33: {
    description: '编号长度边界 33，应拒绝',
    name: '编号超限客户',
    code: 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
    phone: '13800138000'
  },
  blankName: {
    description: '名称为纯空格',
    name: '     ',
    code: 'CUST203',
    phone: '13800138000'
  },
  validForFailure: {
    description: '保存失败专项场景用合法资料',
    name: '保存失败测试客户',
    code: 'CUST301',
    phone: '13800138000'
  }
};
