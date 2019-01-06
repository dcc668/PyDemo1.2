create table tp_accessor_task_price
(
  id                          number(16) not null,
  thirdparty_relevant_user_id number(16) not null,
  fee_code                    varchar2(40),
  task_type                   varchar2(40),
  price                       number(19,2),
  status                      varchar2(20),
  modify_date                 date
)
nologging;
comment on table tp_accessor_task_price
  is '公估人任务价格表';
comment on column tp_accessor_task_price.id
  is '物理主键';
comment on column tp_accessor_task_price.thirdparty_relevant_user_id
  is '关联人员关系表id';
comment on column tp_accessor_task_price.fee_code
  is '费用代码';
comment on column tp_accessor_task_price.task_type
  is '任务类型';
comment on column tp_accessor_task_price.price
  is '合作价格';
comment on column tp_accessor_task_price.status
  is '状态';
comment on column tp_accessor_task_price.modify_date
  is '修改日期';
alter table tp_accessor_task_price
  add primary key (id);

prompt creating tp_autostore_channel_base_info...
create table tp_autostore_channel_base_info
(
  id                number(16) not null,
  branch_code       varchar2(20) not null,
  auto_code         varchar2(100) not null,
  auto_name         varchar2(400),
  auto_type         varchar2(10),
  unique_code       varchar2(100),
  brand_code        varchar2(200),
  brand_name        varchar2(200),
  handler_code      varchar2(100),
  address_name      varchar2(1200),
  auto_grade        varchar2(20),
  orgcode_identify  varchar2(100),
  license_no        varchar2(100),
  business_type     varchar2(20),
  ischnprotect      varchar2(10),
  isadvancedpay     varchar2(10),
  isappreciate      varchar2(10),
  factory_code      varchar2(100),
  factory_name      varchar2(400),
  dealer_code       varchar2(100),
  dealer_name       varchar2(400),
  auto_contactor    varchar2(200),
  auto_cellphone    varchar2(200),
  auto_address_name varchar2(1000),
  isrepairfac       varchar2(10),
  isreturn          varchar2(10),
  isrecommend       varchar2(10),
  recommend_limit   number(10),
  return_limit      number(10),
  isgrouppriority   varchar2(10),
  isforother        varchar2(10),
  old_auto_code     varchar2(400),
  status            varchar2(10),
  modify_date       date,
  channel_type      varchar2(2)
)
nologging;
comment on table tp_autostore_channel_base_info
  is '车商基本信息';
comment on column tp_autostore_channel_base_info.branch_code
  is '分公司代码';
comment on column tp_autostore_channel_base_info.auto_code
  is '车商代码';
comment on column tp_autostore_channel_base_info.auto_name
  is '车商名称';
comment on column tp_autostore_channel_base_info.auto_type
  is '车商类型';
comment on column tp_autostore_channel_base_info.unique_code
  is '归属机构';
comment on column tp_autostore_channel_base_info.brand_code
  is '所属品牌代码';
comment on column tp_autostore_channel_base_info.brand_name
  is '所属品牌名称';
comment on column tp_autostore_channel_base_info.handler_code
  is '业务维护人';
comment on column tp_autostore_channel_base_info.address_name
  is '营业地址';
comment on column tp_autostore_channel_base_info.auto_grade
  is '车商等级';
comment on column tp_autostore_channel_base_info.orgcode_identify
  is '组织机构码';
comment on column tp_autostore_channel_base_info.license_no
  is '营业执照注册号';
comment on column tp_autostore_channel_base_info.business_type
  is '业务类型';
comment on column tp_autostore_channel_base_info.ischnprotect
  is '是否渠道保护';
comment on column tp_autostore_channel_base_info.isadvancedpay
  is '是否有直赔垫付服务';
comment on column tp_autostore_channel_base_info.isappreciate
  is '是否参加增值服务';
comment on column tp_autostore_channel_base_info.factory_code
  is '厂商代码';
comment on column tp_autostore_channel_base_info.factory_name
  is '厂商名称';
comment on column tp_autostore_channel_base_info.dealer_code
  is '集团经销商代码';
comment on column tp_autostore_channel_base_info.dealer_name
  is '集团经销商名称';
comment on column tp_autostore_channel_base_info.auto_contactor
  is '车商联系人姓名';
comment on column tp_autostore_channel_base_info.auto_cellphone
  is '车商联系人电话';
comment on column tp_autostore_channel_base_info.auto_address_name
  is '车商联系人地址';
comment on column tp_autostore_channel_base_info.isrepairfac
  is '是否指定修理厂';
comment on column tp_autostore_channel_base_info.isreturn
  is '是否约定返修';
comment on column tp_autostore_channel_base_info.isrecommend
  is '是否推荐送修';
comment on column tp_autostore_channel_base_info.recommend_limit
  is '每日送修限额';
comment on column tp_autostore_channel_base_info.return_limit
  is '每日返修限额';
comment on column tp_autostore_channel_base_info.isgrouppriority
  is '是否总对总优先';
comment on column tp_autostore_channel_base_info.isforother
  is '是否对其它车商送修';
comment on column tp_autostore_channel_base_info.old_auto_code
  is '原车商代码';
comment on column tp_autostore_channel_base_info.status
  is '车商状态';
comment on column tp_autostore_channel_base_info.modify_date
  is '修改时间';
comment on column tp_autostore_channel_base_info.channel_type
  is '渠道类型。1-车商渠道，0-非车商渠道';
create index idx_tp_autostore_base_inf_code on tp_autostore_channel_base_info (auto_code, branch_code);
alter table tp_autostore_channel_base_info
  add primary key (id);

prompt creating tp_bank_account...
create table tp_bank_account
(
  id                number(16) not null,
  third_party_id    number(16) not null,
  bank_code         varchar2(40),
  account_bank_code varchar2(40),
  remit_account     varchar2(400),
  province_code     varchar2(40),
  city_code         varchar2(40),
  province_name     varchar2(180),
  city_name         varchar2(120),
  bank_name         varchar2(400),
  account_bank_name varchar2(200),
  bankre_mark       varchar2(4000),
  payee             varchar2(200),
  nature            varchar2(20),
  certificate_type  varchar2(10),
  certificate_no    varchar2(100),
  default_account   varchar2(10),
  status            varchar2(10),
  modify_date       date,
  car_dealer        varchar2(10),
  paybackstatus     varchar2(8)
)
nologging;
comment on table tp_bank_account
  is '第三方机构银行帐户';
comment on column tp_bank_account.third_party_id
  is '第三方机构id';
comment on column tp_bank_account.bank_code
  is '银行名称代码';
comment on column tp_bank_account.account_bank_code
  is '开户银行代码';
comment on column tp_bank_account.remit_account
  is '银行帐号';
comment on column tp_bank_account.province_code
  is '收款帐号省';
comment on column tp_bank_account.city_code
  is '收款帐号市';
comment on column tp_bank_account.province_name
  is '省份名称';
comment on column tp_bank_account.city_name
  is '城市名称';
comment on column tp_bank_account.bank_name
  is '银行名称';
comment on column tp_bank_account.account_bank_name
  is '开户银行名称';
comment on column tp_bank_account.bankre_mark
  is '银行备注';
comment on column tp_bank_account.payee
  is '收款人名称';
comment on column tp_bank_account.nature
  is '支付对象性质';
comment on column tp_bank_account.certificate_type
  is '收款人证件类型';
comment on column tp_bank_account.certificate_no
  is '收款人证件号码';
comment on column tp_bank_account.default_account
  is '是否默认支付帐号';
comment on column tp_bank_account.status
  is '状态';
comment on column tp_bank_account.modify_date
  is '记录修改时间';
comment on column tp_bank_account.car_dealer
  is '是否已上传车商 y-是 n-否';
comment on column tp_bank_account.paybackstatus
  is '0:退票申请中 1:退票完成 ';
create index idx1_tp_bank_account on tp_bank_account (third_party_id);
alter table tp_bank_account
  add primary key (id);

prompt creating tp_base_info...
create table tp_base_info
(
  id                     number(16) not null,
  organization_code      varchar2(100) not null,
  organization_type      varchar2(10),
  organization_name      varchar2(600),
  province               varchar2(40),
  city                   varchar2(40),
  district               varchar2(40),
  location               varchar2(600),
  legalname              varchar2(100),
  institutions           varchar2(40),
  licenseno              varchar2(200),
  registered_capital     number(19,2),
  registered_date        date,
  business_start_date    date,
  business_end_date      date,
  respondent             varchar2(10),
  fraud                  varchar2(10),
  blacklist              varchar2(10),
  remarks                varchar2(4000),
  cooperation            varchar2(10),
  status                 varchar2(10),
  province_name          varchar2(100),
  city_name              varchar2(100),
  district_name          varchar2(100),
  institution_name       varchar2(100),
  branch_code            varchar2(100),
  branch_name            varchar2(100),
  modify_date            date,
  car_dealer             varchar2(10),
  upload                 varchar2(10),
  related_third_party_id number(16),
  organization_name_py   varchar2(600),
  shrepairshopcode       varchar2(200),
  assessmentabstractions varchar2(200),
  institution_code       varchar2(200),
  autocode               varchar2(100),
  autocodemodify         varchar2(10),
  operator_code          varchar2(100),
  operator_branch        varchar2(100),
  audit_status           varchar2(40),
  nature                 varchar2(10)
)
nologging;
comment on table tp_base_info
  is '第三方机构基本信息';
comment on column tp_base_info.organization_code
  is '第三方机构编号';
comment on column tp_base_info.organization_type
  is '第三方机构类型';
comment on column tp_base_info.organization_name
  is '第三方机构名称';
comment on column tp_base_info.province
  is '省';
comment on column tp_base_info.city
  is '市';
comment on column tp_base_info.district
  is '区';
comment on column tp_base_info.location
  is '详细地址';
comment on column tp_base_info.legalname
  is '法定代表人姓名';
comment on column tp_base_info.institutions
  is '所属机构';
comment on column tp_base_info.licenseno
  is '工商营业执照注册号';
comment on column tp_base_info.registered_capital
  is '注册资本';
comment on column tp_base_info.registered_date
  is '成立日期';
comment on column tp_base_info.business_start_date
  is '营业开始日期';
comment on column tp_base_info.business_end_date
  is '营业结束日期';
comment on column tp_base_info.respondent
  is '被投诉';
comment on column tp_base_info.fraud
  is '涉及欺诈';
comment on column tp_base_info.blacklist
  is '黑名单';
comment on column tp_base_info.remarks
  is '备注';
comment on column tp_base_info.cooperation
  is '合作机构';
comment on column tp_base_info.status
  is '状态';
comment on column tp_base_info.province_name
  is '省名';
comment on column tp_base_info.city_name
  is '市名';
comment on column tp_base_info.district_name
  is '区名';
comment on column tp_base_info.institution_name
  is '所属机构名称';
comment on column tp_base_info.branch_code
  is '分公司代码';
comment on column tp_base_info.branch_name
  is '分公司名称';
comment on column tp_base_info.modify_date
  is '记录修改时间';
comment on column tp_base_info.car_dealer
  is '是否车商下发数据 y-是 n-否';
comment on column tp_base_info.upload
  is '是否已上传车商 y-是 n-否';
comment on column tp_base_info.related_third_party_id
  is '关联第三方id';
comment on column tp_base_info.organization_name_py
  is '第三方机构名称首字母拼音';
comment on column tp_base_info.shrepairshopcode
  is '标识上海/北京的修理厂平台代码';
comment on column tp_base_info.assessmentabstractions
  is '公估公司名称缩写（限3位）';
comment on column tp_base_info.institution_code
  is '组织机构代码';
comment on column tp_base_info.autocode
  is '车商代码';
comment on column tp_base_info.autocodemodify
  is '车商代码可修改';
comment on column tp_base_info.operator_code
  is '操作人代码';
comment on column tp_base_info.operator_branch
  is '操作人分公司';
comment on column tp_base_info.audit_status
  is '审核状态';
comment on column tp_base_info.nature
  is '第三方性质';
create index idx1_tp_base_info on tp_base_info (organization_code);
create index idx4_tp_base_info on tp_base_info (organization_name);
create index idx5_tp_base_info on tp_base_info (organization_name_py);
create index idx6_tp_base_info on tp_base_info (status, organization_type);
create index idx_tp_base_info_amas on tp_base_info (assessmentabstractions);
alter table tp_base_info
  add primary key (id);

prompt creating tp_base_info_20150305...
create table tp_base_info_20150305
(
  id                     number(16) not null,
  organization_code      varchar2(100) not null,
  organization_type      varchar2(10),
  organization_name      varchar2(600),
  province               varchar2(40),
  city                   varchar2(40),
  district               varchar2(40),
  location               varchar2(600),
  legalname              varchar2(100),
  institutions           varchar2(40),
  licenseno              varchar2(200),
  registered_capital     number(19,2),
  registered_date        date,
  business_start_date    date,
  business_end_date      date,
  respondent             varchar2(10),
  fraud                  varchar2(10),
  blacklist              varchar2(10),
  remarks                varchar2(600),
  cooperation            varchar2(10),
  status                 varchar2(10),
  province_name          varchar2(60),
  city_name              varchar2(60),
  district_name          varchar2(60),
  institution_name       varchar2(100),
  branch_code            varchar2(100),
  branch_name            varchar2(100),
  modify_date            date,
  car_dealer             varchar2(10),
  upload                 varchar2(10),
  related_third_party_id number(16),
  organization_name_py   varchar2(600),
  shrepairshopcode       varchar2(200),
  assessmentabstractions varchar2(200)
)
nologging;

prompt creating tp_brand_audit...
create table tp_brand_audit
(
  id                        number(16) not null,
  third_party_id            number(16) not null,
  brand_code                varchar2(100),
  modify_date               date,
  status                    varchar2(10),
  mainbrand                 varchar2(10),
  right_show_org_price      varchar2(10),
  right_show_contract_price varchar2(10),
  right_show_market_price   varchar2(10),
  right_show_fit_price      varchar2(10),
  metal_price               number(16,2),
  dismounting_price         number(16,2),
  spray_paint_price         number(16,2),
  hour_regulated_rate       number(16,2),
  hour_discount_rate        number(16,2),
  parts_regulated_rate      number(16,2),
  parts_discount_rate       number(16,2),
  spray_paint_ratio         number(16,2),
  price_right               varchar2(40),
  operator_code             varchar2(100),
  operator_branch           varchar2(100),
  audit_status              varchar2(40)
)
nologging;
comment on table tp_brand_audit
  is '品牌审核信息表';
comment on column tp_brand_audit.third_party_id
  is '第三方机构id';
comment on column tp_brand_audit.brand_code
  is '关联品牌代码';
comment on column tp_brand_audit.modify_date
  is '记录修改日期';
comment on column tp_brand_audit.status
  is '状态';
comment on column tp_brand_audit.mainbrand
  is '主品牌';
comment on column tp_brand_audit.right_show_org_price
  is '4s店价格';
comment on column tp_brand_audit.right_show_contract_price
  is '协议价格';
comment on column tp_brand_audit.right_show_market_price
  is '市场价格';
comment on column tp_brand_audit.right_show_fit_price
  is '适用价格';
comment on column tp_brand_audit.metal_price
  is '钣金工时单价';
comment on column tp_brand_audit.dismounting_price
  is '拆装工时单价';
comment on column tp_brand_audit.spray_paint_price
  is '喷漆工时单价';
comment on column tp_brand_audit.hour_regulated_rate
  is '工时上调比率';
comment on column tp_brand_audit.hour_discount_rate
  is '工时折扣率';
comment on column tp_brand_audit.parts_regulated_rate
  is '换件上调比率';
comment on column tp_brand_audit.parts_discount_rate
  is '换件折扣率';
comment on column tp_brand_audit.spray_paint_ratio
  is '喷漆系数';
comment on column tp_brand_audit.operator_code
  is '操作人代码';
comment on column tp_brand_audit.operator_branch
  is '操作人分公司';
comment on column tp_brand_audit.audit_status
  is '审核状态';
create index idx1_tp_brand_audit on tp_brand_audit (third_party_id);
alter table tp_brand_audit
  add primary key (id);

prompt creating tp_brand_baseinfo...
create table tp_brand_baseinfo
(
  id          number(16) not null,
  brand_code  varchar2(100),
  brand_name  varchar2(100),
  brand_py    varchar2(100),
  modify_date date,
  workdate    number(8),
  status      varchar2(10)
)
nologging;
comment on table tp_brand_baseinfo
  is '车辆品牌基础信息表';
comment on column tp_brand_baseinfo.brand_code
  is '品牌代码';
comment on column tp_brand_baseinfo.brand_name
  is '品牌名称';
comment on column tp_brand_baseinfo.brand_py
  is '品牌名称拼音';
comment on column tp_brand_baseinfo.modify_date
  is '记录修改日期';
comment on column tp_brand_baseinfo.workdate
  is '启用日期';
comment on column tp_brand_baseinfo.status
  is '状态';
create index idx1_tp_brand_baseinfo on tp_brand_baseinfo (brand_code);
create index idx2_tp_brand_baseinfo on tp_brand_baseinfo (brand_name);
alter table tp_brand_baseinfo
  add primary key (id);

prompt creating tp_businesss_cope...
create table tp_businesss_cope
(
  id             number(16) not null,
  third_party_id number(16) not null,
  scope_type     varchar2(40),
  business_code  varchar2(10),
  business_name  varchar2(200),
  status         varchar2(10),
  remarks        varchar2(600),
  modify_date    date,
  car_dealer     varchar2(10)
)
nologging;
comment on table tp_businesss_cope
  is '第三方机构经营范围';
comment on column tp_businesss_cope.third_party_id
  is '第三方机构id';
comment on column tp_businesss_cope.scope_type
  is '范围类别';
comment on column tp_businesss_cope.business_code
  is '范围代码';
comment on column tp_businesss_cope.business_name
  is '范围名称';
comment on column tp_businesss_cope.status
  is '状态';
comment on column tp_businesss_cope.remarks
  is '其他说明';
comment on column tp_businesss_cope.modify_date
  is '记录修改时间';
comment on column tp_businesss_cope.car_dealer
  is '是否已上传车商 y-是 n-否';
create index idx1_tp_businesss_cope on tp_businesss_cope (third_party_id);
alter table tp_businesss_cope
  add primary key (id);

prompt creating tp_business_area...
create table tp_business_area
(
  id             number(16) not null,
  third_party_id number(16) not null,
  area_code      varchar2(100),
  area_name      varchar2(1000),
  area_level     varchar2(10),
  full_area_code varchar2(200),
  status         varchar2(10),
  modify_date    date,
  car_dealer     varchar2(10)
)
nologging;
comment on table tp_business_area
  is '第三方机构经营区域';
comment on column tp_business_area.third_party_id
  is '第三方机构id';
comment on column tp_business_area.area_code
  is '服务区域代码';
comment on column tp_business_area.area_name
  is '服务区域名称';
comment on column tp_business_area.area_level
  is '服务区域级别';
comment on column tp_business_area.full_area_code
  is '完整服务区域代码';
comment on column tp_business_area.status
  is '有效状态';
comment on column tp_business_area.modify_date
  is '记录修改时间';
comment on column tp_business_area.car_dealer
  is '是否已上传车商 y-是 n-否';
create index idx1_tp_business_area on tp_business_area (third_party_id);
alter table tp_business_area
  add primary key (id);

prompt creating tp_contact...
create table tp_contact
(
  id              number(16) not null,
  third_party_id  number(16) not null,
  name            varchar2(100),
  tel             varchar2(120),
  mobile1         varchar2(40),
  mobile2         varchar2(40),
  email           varchar2(100),
  remarks         varchar2(600),
  status          varchar2(10),
  send_msg        varchar2(10),
  default_contact varchar2(10),
  address         varchar2(1000),
  modify_date     date,
  car_dealer      varchar2(10)
)
nologging;
comment on table tp_contact
  is '第三方机构联系人';
comment on column tp_contact.third_party_id
  is '第三方机构id';
comment on column tp_contact.name
  is '姓名';
comment on column tp_contact.tel
  is '联系电话';
comment on column tp_contact.mobile1
  is '手机';
comment on column tp_contact.mobile2
  is '备用手机';
comment on column tp_contact.email
  is '电子邮件';
comment on column tp_contact.remarks
  is '备注';
comment on column tp_contact.status
  is '状态';
comment on column tp_contact.send_msg
  is '是否发送短信';
comment on column tp_contact.default_contact
  is '是否默认联系人';
comment on column tp_contact.address
  is '联系地址';
comment on column tp_contact.modify_date
  is '记录修改时间';
comment on column tp_contact.car_dealer
  is '是否已上传车商 y-是 n-否';
create index idx1_tp_contact on tp_contact (third_party_id);
alter table tp_contact
  add primary key (id);

prompt creating tp_contract...
create table tp_contract
(
  id                       number(16) not null,
  third_party_id           number(16) not null,
  branch_code              varchar2(100),
  contract_type            varchar2(20),
  change_reason            varchar2(20),
  contract_new             varchar2(20),
  contract_no              varchar2(100),
  contract_running_no      varchar2(100),
  version_no               varchar2(20),
  head_contract            varchar2(20),
  head_contract_no         varchar2(100),
  start_date               date,
  end_date                 date,
  status                   varchar2(20),
  create_date              date,
  operator                 varchar2(100),
  operator_branch          varchar2(100),
  modify_date              date,
  memo                     varchar2(1000),
  attachment               varchar2(20),
  cancel_date              date,
  head_contract_running_no varchar2(100),
  history_version          varchar2(10),
  pre_contract_id          number(16),
  auto_renew               varchar2(10),
  audit_opinion            varchar2(10),
  audit_description        varchar2(1000),
  audit_operator           varchar2(100),
  audit_operator_branch    varchar2(100),
  audit_date               date
)
nologging;
comment on table tp_contract
  is '第三方合同表';
comment on column tp_contract.third_party_id
  is '乙方id';
comment on column tp_contract.branch_code
  is '甲方代码';
comment on column tp_contract.contract_type
  is '合同类型';
comment on column tp_contract.change_reason
  is '变更原因';
comment on column tp_contract.contract_new
  is '新合同/续签合同';
comment on column tp_contract.contract_no
  is '合同编号';
comment on column tp_contract.contract_running_no
  is '合同流水号';
comment on column tp_contract.version_no
  is '合同版本号';
comment on column tp_contract.head_contract
  is '总对总合同';
comment on column tp_contract.head_contract_no
  is '总对总合同编号';
comment on column tp_contract.start_date
  is '合同开始日期';
comment on column tp_contract.end_date
  is '合同结束日期';
comment on column tp_contract.status
  is '合同状态';
comment on column tp_contract.create_date
  is '合同创建日期';
comment on column tp_contract.operator
  is '最后操作人员代码';
comment on column tp_contract.operator_branch
  is '最后操作人员分公司';
comment on column tp_contract.modify_date
  is '最后操作日期';
comment on column tp_contract.memo
  is '备注';
comment on column tp_contract.attachment
  is '合同附件';
comment on column tp_contract.cancel_date
  is '合同解除日期';
comment on column tp_contract.head_contract_running_no
  is '总对总合同流水号';
comment on column tp_contract.history_version
  is '历史版本';
comment on column tp_contract.pre_contract_id
  is '续签原合同id';
comment on column tp_contract.auto_renew
  is '自动续签';
comment on column tp_contract.audit_opinion
  is '审核意见';
comment on column tp_contract.audit_description
  is '审核说明';
comment on column tp_contract.audit_operator
  is '审核人员代码';
comment on column tp_contract.audit_operator_branch
  is '审核人员分公司代码';
comment on column tp_contract.audit_date
  is '审核时间';
create index idx1_tp_contract on tp_contract (third_party_id);
create index idx2_tp_contract on tp_contract (branch_code);
alter table tp_contract
  add primary key (id);

prompt creating tp_contract_discount...
create table tp_contract_discount
(
  id                  number(16) not null,
  organization_code   varchar2(100) not null,
  organization_branch varchar2(100) not null,
  discount_rate       number(5,4),
  effective_date      date,
  status              varchar2(20),
  operator            varchar2(100),
  operator_branch     varchar2(100),
  modify_date         date,
  application_scope   varchar2(1000),
  memo                varchar2(1000)
)
nologging;
comment on table tp_contract_discount
  is '合同折扣率表';
comment on column tp_contract_discount.organization_code
  is '第三方机构代码';
comment on column tp_contract_discount.organization_branch
  is '第三方机构分公司';
comment on column tp_contract_discount.discount_rate
  is '折扣率';
comment on column tp_contract_discount.effective_date
  is '生效时间';
comment on column tp_contract_discount.status
  is '折扣状态';
comment on column tp_contract_discount.operator
  is '操作人代码';
comment on column tp_contract_discount.modify_date
  is '最后操作时间';
comment on column tp_contract_discount.application_scope
  is '适用范围';
comment on column tp_contract_discount.memo
  is '备注';
alter table tp_contract_discount
  add primary key (id);

prompt creating tp_contract_fee...
create table tp_contract_fee
(
  id               number(16) not null,
  contract_id      number(16) not null,
  fee_code         varchar2(100),
  task_type        varchar2(100),
  amount           number(10,2),
  status           varchar2(20),
  modify_date      date,
  parent_task_type varchar2(100)
)
nologging;
comment on table tp_contract_fee
  is '第三方合同费用表';
comment on column tp_contract_fee.contract_id
  is '第三方合同id';
comment on column tp_contract_fee.fee_code
  is '费用代码';
comment on column tp_contract_fee.task_type
  is '任务类型';
comment on column tp_contract_fee.amount
  is '金额';
comment on column tp_contract_fee.status
  is '状态';
comment on column tp_contract_fee.modify_date
  is '最后操作日期';
comment on column tp_contract_fee.parent_task_type
  is '父类任务类型';
create index idx1_tp_contract_fee on tp_contract_fee (contract_id);
alter table tp_contract_fee
  add primary key (id);

prompt creating tp_contract_repair...
create table tp_contract_repair
(
  id                   number(16) not null,
  contract_id          number(16) not null,
  metal_price          number(16,2),
  dismounting_price    number(16,2),
  spray_paint_price    number(16,2),
  hour_regulated_rate  number(20,4),
  hour_discount_rate   number(20,4),
  parts_regulated_rate number(20,4),
  parts_discount_rate  number(20,4),
  modify_date          date,
  spray_paint_ratio    number(16,2)
)
nologging;
comment on table tp_contract_repair
  is '第三方合同维修厂折扣表';
comment on column tp_contract_repair.contract_id
  is '第三方合同id';
comment on column tp_contract_repair.metal_price
  is '修理厂钣金工时单价';
comment on column tp_contract_repair.dismounting_price
  is '修理厂拆装工时单价';
comment on column tp_contract_repair.spray_paint_price
  is '修理厂喷漆工时单价';
comment on column tp_contract_repair.hour_regulated_rate
  is '工时上调比率';
comment on column tp_contract_repair.hour_discount_rate
  is '工时折扣率';
comment on column tp_contract_repair.parts_regulated_rate
  is '换件上调比率';
comment on column tp_contract_repair.parts_discount_rate
  is '换件折扣率';
comment on column tp_contract_repair.modify_date
  is '最后操作日期';
comment on column tp_contract_repair.spray_paint_ratio
  is '喷漆系数';
create index idx1_tp_contract_repair on tp_contract_repair (contract_id);
alter table tp_contract_repair
  add primary key (id);

prompt creating tp_expense_log...
create table tp_expense_log
(
  id             number(16) not null,
  casefolderid   number(16),
  businessno     varchar2(100),
  taskid         number(16),
  tasktype       varchar2(200),
  amount         number(10,2),
  feetype        varchar2(40),
  thirdpartycode varchar2(40),
  opcode         varchar2(40),
  opunitcode     varchar2(40),
  b_unitcode     varchar2(40),
  status         varchar2(40),
  opdate         date,
  feekind        varchar2(100)
)
nologging;
comment on table tp_expense_log
  is '第三方费用日志表';
comment on column tp_expense_log.id
  is '费用日志id';
comment on column tp_expense_log.casefolderid
  is '案卷id';
comment on column tp_expense_log.businessno
  is '业务节点id或编号';
comment on column tp_expense_log.taskid
  is '任务id';
comment on column tp_expense_log.tasktype
  is '费用发起环节';
comment on column tp_expense_log.amount
  is '费用金额';
comment on column tp_expense_log.feetype
  is '费用类型';
comment on column tp_expense_log.thirdpartycode
  is '第三方机构代码';
comment on column tp_expense_log.opcode
  is '任务处理人';
comment on column tp_expense_log.opunitcode
  is '任务处理人所属机构';
comment on column tp_expense_log.b_unitcode
  is '保单所属机构';
comment on column tp_expense_log.status
  is '状态';
comment on column tp_expense_log.opdate
  is '操作时间';
comment on column tp_expense_log.feekind
  is '费用分类';
create index idx_tp_expense_log_1 on tp_expense_log (casefolderid);
alter table tp_expense_log
  add primary key (id);

prompt creating tp_garage_info_temp...
create table tp_garage_info_temp
(
  organization_code          varchar2(200),
  organization_name          varchar2(600),
  province_name              varchar2(100),
  city_name                  varchar2(100),
  district_name              varchar2(100),
  location                   varchar2(600),
  legalname                  varchar2(100),
  branch_name                varchar2(100),
  licenseno                  varchar2(200),
  registered_capital         number(19,2),
  registered_date            date,
  business_start_date        date,
  business_end_date          date,
  respondent                 varchar2(10),
  fraud                      varchar2(10),
  blacklist                  varchar2(10),
  remarks                    varchar2(600),
  cooperation                varchar2(10),
  institution_code           varchar2(200),
  autocode                   varchar2(100),
  organization_category      varchar2(40),
  organization_level         varchar2(20),
  special_vehicle_repair     varchar2(10),
  direct_compensation_repair varchar2(10),
  contact_name               varchar2(40),
  contact_tel                varchar2(40),
  mobile1                    varchar2(40),
  mobile2                    varchar2(40),
  email                      varchar2(100),
  contact_remarks            varchar2(600),
  account_bank_name          varchar2(400),
  bank_name                  varchar2(400),
  bank_province_name         varchar2(100),
  bank_city_name             varchar2(100),
  remit_account              varchar2(200),
  payee                      varchar2(200),
  certificate_type           varchar2(40),
  certificate_no             varchar2(100),
  bankre_mark                varchar2(600),
  first_scope                varchar2(400),
  first_scope_remarks        varchar2(600),
  secondscope                varchar2(400),
  secondscope_remarks        varchar2(600),
  business_area              varchar2(400),
  user_branch_name           varchar2(100),
  user_code                  varchar2(40),
  certificateno              varchar2(100),
  sex                        varchar2(40),
  birthday                   date,
  eduaction                  varchar2(100),
  major                      varchar2(200),
  years_of_employees         number(19),
  brand_name                 varchar2(400),
  org_price                  varchar2(10),
  market_price               varchar2(10),
  fit_price                  varchar2(10),
  contract_price             varchar2(10),
  metal_manhour_price        number(16,2),
  dismounting_price          number(16,2),
  spray_paint_price          number(16,2),
  hour_regulated_rate        number(20,4),
  hour_discount_rate         number(20,4),
  parts_regulated_rate       number(20,4),
  parts_discount_rate        number(20,4),
  spray_paint_ratio          number(20,4),
  task_id                    number(16) not null,
  status                     varchar2(10),
  operate_time               date,
  operator                   varchar2(40),
  operator_branch            varchar2(40),
  serial_no                  varchar2(40),
  modify_time                date,
  error_msg                  varchar2(4000),
  import_type                varchar2(20),
  main_brand                 varchar2(10),
  price_right                varchar2(40),
  iud_type                   varchar2(20)
)
nologging;
comment on column tp_garage_info_temp.organization_code
  is '第三方机构代码';
comment on column tp_garage_info_temp.organization_name
  is '第三方机构名称';
comment on column tp_garage_info_temp.province_name
  is '省';
comment on column tp_garage_info_temp.city_name
  is '市';
comment on column tp_garage_info_temp.district_name
  is '区';
comment on column tp_garage_info_temp.location
  is '详细地址';
comment on column tp_garage_info_temp.legalname
  is '法人名称';
comment on column tp_garage_info_temp.branch_name
  is '分公司名称';
comment on column tp_garage_info_temp.licenseno
  is '营业执照';
comment on column tp_garage_info_temp.registered_capital
  is '注册资本';
comment on column tp_garage_info_temp.registered_date
  is '成立日期';
comment on column tp_garage_info_temp.business_start_date
  is '营业开始日期';
comment on column tp_garage_info_temp.business_end_date
  is '营业结束日期';
comment on column tp_garage_info_temp.respondent
  is '是否有投诉';
comment on column tp_garage_info_temp.fraud
  is '是否有欺诈';
comment on column tp_garage_info_temp.blacklist
  is '是否黑名单';
comment on column tp_garage_info_temp.remarks
  is '备注';
comment on column tp_garage_info_temp.cooperation
  is '是否合作机构';
comment on column tp_garage_info_temp.institution_code
  is '组织机构代码';
comment on column tp_garage_info_temp.autocode
  is '车商代码';
comment on column tp_garage_info_temp.organization_category
  is '车辆维修单位类别';
comment on column tp_garage_info_temp.organization_level
  is '车辆维修单位级别';
comment on column tp_garage_info_temp.special_vehicle_repair
  is '特种车维修';
comment on column tp_garage_info_temp.direct_compensation_repair
  is '直赔维修';
comment on column tp_garage_info_temp.contact_name
  is '默认联系人名';
comment on column tp_garage_info_temp.contact_tel
  is '电话';
comment on column tp_garage_info_temp.mobile1
  is '手机1';
comment on column tp_garage_info_temp.mobile2
  is '手机2';
comment on column tp_garage_info_temp.email
  is '电子邮件';
comment on column tp_garage_info_temp.contact_remarks
  is '联系人备注';
comment on column tp_garage_info_temp.account_bank_name
  is '默认开户行';
comment on column tp_garage_info_temp.bank_name
  is '开户行总行';
comment on column tp_garage_info_temp.bank_province_name
  is '开户行省';
comment on column tp_garage_info_temp.bank_city_name
  is '开户行市';
comment on column tp_garage_info_temp.remit_account
  is '银行帐号';
comment on column tp_garage_info_temp.payee
  is '收款人名';
comment on column tp_garage_info_temp.certificate_type
  is '证件类型';
comment on column tp_garage_info_temp.certificate_no
  is '证件号';
comment on column tp_garage_info_temp.bankre_mark
  is '银行备注';
comment on column tp_garage_info_temp.first_scope
  is '一级经营范围';
comment on column tp_garage_info_temp.first_scope_remarks
  is '一级经营范围备注';
comment on column tp_garage_info_temp.secondscope
  is '专项维修子范围';
comment on column tp_garage_info_temp.secondscope_remarks
  is '专项维修子范围备注';
comment on column tp_garage_info_temp.business_area
  is '经营区域';
comment on column tp_garage_info_temp.user_branch_name
  is '登录人员分公司';
comment on column tp_garage_info_temp.user_code
  is '登录人员代码';
comment on column tp_garage_info_temp.certificateno
  is '登录人员身份证';
comment on column tp_garage_info_temp.sex
  is '登录人员性别';
comment on column tp_garage_info_temp.birthday
  is '登录人员出生日期';
comment on column tp_garage_info_temp.eduaction
  is '登录人员学历';
comment on column tp_garage_info_temp.major
  is '登录人员专业';
comment on column tp_garage_info_temp.years_of_employees
  is '登录人员从业时间（整数）';
comment on column tp_garage_info_temp.brand_name
  is '主品牌名称';
comment on column tp_garage_info_temp.org_price
  is '4s店价格';
comment on column tp_garage_info_temp.market_price
  is '市场价格';
comment on column tp_garage_info_temp.fit_price
  is '适用价格';
comment on column tp_garage_info_temp.contract_price
  is '合同价格';
comment on column tp_garage_info_temp.metal_manhour_price
  is '钣金工时单价';
comment on column tp_garage_info_temp.dismounting_price
  is '拆装工时单价';
comment on column tp_garage_info_temp.spray_paint_price
  is '喷漆工时单价';
comment on column tp_garage_info_temp.hour_regulated_rate
  is '工时上调比率';
comment on column tp_garage_info_temp.hour_discount_rate
  is '工时折扣率';
comment on column tp_garage_info_temp.parts_regulated_rate
  is '管理费率';
comment on column tp_garage_info_temp.parts_discount_rate
  is '换件折扣率';
comment on column tp_garage_info_temp.spray_paint_ratio
  is '喷漆系数';
comment on column tp_garage_info_temp.task_id
  is '任务id';
comment on column tp_garage_info_temp.status
  is '状态';
comment on column tp_garage_info_temp.operate_time
  is '操作时间';
comment on column tp_garage_info_temp.operator
  is '操作人';
comment on column tp_garage_info_temp.operator_branch
  is '操作人分公司';
comment on column tp_garage_info_temp.serial_no
  is '批次号';
comment on column tp_garage_info_temp.modify_time
  is '更新时间';
comment on column tp_garage_info_temp.error_msg
  is '错误信息';
comment on column tp_garage_info_temp.import_type
  is '导入类型';
comment on column tp_garage_info_temp.main_brand
  is '是否主品牌';
comment on column tp_garage_info_temp.price_right
  is '价格方案';
comment on column tp_garage_info_temp.iud_type
  is '修改类型：新增，删除，修改';
create index idx_tgit_sno on tp_garage_info_temp (serial_no);
alter table tp_garage_info_temp
  add primary key (task_id);

prompt creating tp_option...
create table tp_option
(
  id              number(16) not null,
  third_party_id  number(16) not null,
  modify_date     date,
  status          varchar2(10),
  operator_code   varchar2(100),
  operator_branch varchar2(100),
  memo            varchar2(4000)
)
nologging;
comment on table tp_option
  is '品牌审核意见历史表';
comment on column tp_option.third_party_id
  is '第三方机构id';
comment on column tp_option.modify_date
  is '记录修改日期';
comment on column tp_option.operator_code
  is '操作人代码';
comment on column tp_option.operator_branch
  is '操作人分公司';
comment on column tp_option.memo
  is '审核意见';
create index idx1_tp_option on tp_option (third_party_id);
alter table tp_option
  add primary key (id);

prompt creating tp_relevant_branch...
create table tp_relevant_branch
(
  id             number(16) not null,
  third_party_id number(16),
  branch_code    varchar2(20),
  branch_name    varchar2(100),
  status         varchar2(10)
)
nologging;
comment on table tp_relevant_branch
  is '公估公司权限表';
comment on column tp_relevant_branch.third_party_id
  is '第三方机构id';
comment on column tp_relevant_branch.branch_code
  is '分公司代码';
comment on column tp_relevant_branch.branch_name
  is '分公司名称';
comment on column tp_relevant_branch.status
  is '状态 0-无效1-有效';
create index idx1_tp_relevant_branch on tp_relevant_branch (third_party_id);
alter table tp_relevant_branch
  add primary key (id);

prompt creating tp_relevant_brand...
create table tp_relevant_brand
(
  id                        number(16) not null,
  third_party_id            number(16) not null,
  brand_code                varchar2(100),
  modify_date               date,
  status                    varchar2(10),
  mainbrand                 varchar2(10),
  right_show_org_price      varchar2(10),
  right_show_contract_price varchar2(10),
  right_show_market_price   varchar2(10),
  right_show_fit_price      varchar2(10),
  metal_price               number(16,2),
  dismounting_price         number(16,2),
  spray_paint_price         number(16,2),
  hour_regulated_rate       number(16,2),
  hour_discount_rate        number(16,2),
  parts_regulated_rate      number(16,2),
  parts_discount_rate       number(16,2),
  spray_paint_ratio         number(16,2),
  price_right               varchar2(40)
)
nologging;
comment on table tp_relevant_brand
  is '第三方机构关联品牌表';
comment on column tp_relevant_brand.third_party_id
  is '第三方机构id';
comment on column tp_relevant_brand.brand_code
  is '关联品牌代码';
comment on column tp_relevant_brand.modify_date
  is '记录修改日期';
comment on column tp_relevant_brand.status
  is '状态';
comment on column tp_relevant_brand.mainbrand
  is '主品牌';
comment on column tp_relevant_brand.right_show_org_price
  is '4s店价格';
comment on column tp_relevant_brand.right_show_contract_price
  is '协议价格';
comment on column tp_relevant_brand.right_show_market_price
  is '市场价格';
comment on column tp_relevant_brand.right_show_fit_price
  is '适用价格';
comment on column tp_relevant_brand.metal_price
  is '钣金工时单价';
comment on column tp_relevant_brand.dismounting_price
  is '拆装工时单价';
comment on column tp_relevant_brand.spray_paint_price
  is '喷漆工时单价';
comment on column tp_relevant_brand.hour_regulated_rate
  is '工时上调比率';
comment on column tp_relevant_brand.hour_discount_rate
  is '工时折扣率';
comment on column tp_relevant_brand.parts_regulated_rate
  is '换件上调比率';
comment on column tp_relevant_brand.parts_discount_rate
  is '换件折扣率';
comment on column tp_relevant_brand.spray_paint_ratio
  is '喷漆系数';
comment on column tp_relevant_brand.price_right
  is '价格方案';
create index idx1_tp_relevant_brand on tp_relevant_brand (third_party_id);
alter table tp_relevant_brand
  add primary key (id);

prompt creating tp_relevant_org...
create table tp_relevant_org
(
  id                   number(16) not null,
  third_party_id       number(16) not null,
  organization_code    varchar2(100),
  organization_name    varchar2(400),
  location             varchar2(600),
  default_organization varchar2(10),
  status               varchar2(10),
  province             varchar2(40),
  city                 varchar2(40),
  district             varchar2(40),
  province_name        varchar2(60),
  cityname             varchar2(60),
  district_name        varchar2(60),
  modify_date          date,
  car_dealer           varchar2(10)
)
nologging;
comment on table tp_relevant_org
  is '第三方机构相关机构';
comment on column tp_relevant_org.third_party_id
  is '第三方机构id';
comment on column tp_relevant_org.organization_code
  is '相关机构代码';
comment on column tp_relevant_org.organization_name
  is '相关机构名称';
comment on column tp_relevant_org.location
  is '相关机构地址';
comment on column tp_relevant_org.default_organization
  is '是否默认';
comment on column tp_relevant_org.status
  is '有效状态';
comment on column tp_relevant_org.province
  is '省名';
comment on column tp_relevant_org.city
  is '市名';
comment on column tp_relevant_org.district
  is '区名';
comment on column tp_relevant_org.province_name
  is '省名';
comment on column tp_relevant_org.cityname
  is '市名';
comment on column tp_relevant_org.district_name
  is '区名';
comment on column tp_relevant_org.modify_date
  is '记录修改时间';
comment on column tp_relevant_org.car_dealer
  is '是否已上传车商 y-是 n-否';
alter table tp_relevant_org
  add primary key (id);

prompt creating tp_relevant_user...
create table tp_relevant_user
(
  id                   number(16) not null,
  third_party_id       number(16) not null,
  user_code            varchar2(40),
  branch_code          varchar2(40),
  modify_date          date,
  status               varchar2(10),
  name                 varchar2(100),
  cpicuid              varchar2(100),
  sex                  varchar2(40),
  birthday             date,
  certificateno        varchar2(100),
  eduaction            varchar2(100),
  major                varchar2(200),
  years_of_employees   number(19),
  authority_of_branch  varchar2(510),
  relevant_type        varchar2(40),
  institution_code     varchar2(100),
  third_party_org_code varchar2(100),
  user_type            varchar2(40),
  licenseno            varchar2(100),
  tel                  varchar2(40),
  mobile               varchar2(40),
  email                varchar2(100),
  memo                 varchar2(4000)
)
nologging;
comment on table tp_relevant_user
  is '第三方机构关联人员关系表';
comment on column tp_relevant_user.third_party_id
  is '第三方机构id';
comment on column tp_relevant_user.user_code
  is '关联人员代码';
comment on column tp_relevant_user.branch_code
  is '关联人员分公司代码';
comment on column tp_relevant_user.modify_date
  is '记录修改日期';
comment on column tp_relevant_user.status
  is '状态';
comment on column tp_relevant_user.name
  is '人员姓名';
comment on column tp_relevant_user.cpicuid
  is 'cpicuid';
comment on column tp_relevant_user.sex
  is '性别';
comment on column tp_relevant_user.birthday
  is '出生日期';
comment on column tp_relevant_user.certificateno
  is '身份证号码';
comment on column tp_relevant_user.eduaction
  is '学历';
comment on column tp_relevant_user.major
  is '专业';
comment on column tp_relevant_user.years_of_employees
  is '从业年限';
comment on column tp_relevant_user.authority_of_branch
  is '机构权限';
comment on column tp_relevant_user.relevant_type
  is '关联机构类型';
comment on column tp_relevant_user.institution_code
  is '保险公司分公司代码';
comment on column tp_relevant_user.third_party_org_code
  is '第三方机构代码';
comment on column tp_relevant_user.user_type
  is '人员类型';
comment on column tp_relevant_user.licenseno
  is '执照编号';
comment on column tp_relevant_user.tel
  is '电话';
comment on column tp_relevant_user.mobile
  is '手机';
comment on column tp_relevant_user.email
  is '邮件地址';
comment on column tp_relevant_user.memo
  is '备注';
create index idx1_tp_relevant_user on tp_relevant_user (third_party_id);
alter table tp_relevant_user
  add primary key (id);

prompt creating tp_special_info...
create table tp_special_info
(
  id                         number(16) not null,
  third_party_id             number(16) not null,
  organization_category      varchar2(10),
  organization_level         varchar2(10),
  hospital_level             varchar2(10),
  hospital_rank              varchar2(10),
  identification_type        varchar2(10),
  validate_time              date,
  brand                      varchar2(40),
  brand_name                 varchar2(100),
  maintenance                varchar2(40),
  org_code                   varchar2(40),
  business_type              varchar2(10),
  channel_protection         varchar2(10),
  direct_compensation        varchar2(10),
  appreciation               varchar2(10),
  manufacturer_code          varchar2(100),
  manufacturer_name          varchar2(100),
  group_dealer               varchar2(100),
  group_dealer_name          varchar2(100),
  contact_name               varchar2(40),
  contact_tel                varchar2(40),
  contact_address            varchar2(600),
  specified_repair           varchar2(10),
  agreed_repair              varchar2(10),
  recommended_repair         varchar2(10),
  maintenance_limit          number(10),
  repair_limit               number(10),
  total_priority             varchar2(10),
  other_repair               varchar2(10),
  old_code                   varchar2(100),
  modify_date                date,
  car_dealer                 varchar2(10),
  right_show_org_price       varchar2(10),
  right_show_contract_price  varchar2(10),
  right_show_market_price    varchar2(10),
  right_show_fit_price       varchar2(10),
  special_vehicle_repair     varchar2(10),
  direct_compensation_repair varchar2(10),
  head_dispatch              varchar2(10)
)
nologging;
comment on table tp_special_info
  is '第三方机构特殊信息';
comment on column tp_special_info.third_party_id
  is '第三方机构id';
comment on column tp_special_info.organization_category
  is '车辆维修单位类别';
comment on column tp_special_info.organization_level
  is '车辆维修单位级别';
comment on column tp_special_info.hospital_level
  is '医院综合水平等级';
comment on column tp_special_info.hospital_rank
  is '医院等级';
comment on column tp_special_info.identification_type
  is '鉴定机构类别';
comment on column tp_special_info.validate_time
  is '拍卖经营批准证书有效期限';
comment on column tp_special_info.brand
  is '所属品牌';
comment on column tp_special_info.brand_name
  is '品牌名称';
comment on column tp_special_info.maintenance
  is '业务维护人';
comment on column tp_special_info.org_code
  is '组织机构码';
comment on column tp_special_info.business_type
  is '业务类型 1-总对总、2-分对分、3-一般业务';
comment on column tp_special_info.channel_protection
  is '是否渠道保护';
comment on column tp_special_info.direct_compensation
  is '是否有直赔垫付服务';
comment on column tp_special_info.appreciation
  is '是否参加增值服务';
comment on column tp_special_info.manufacturer_code
  is '车商代码';
comment on column tp_special_info.manufacturer_name
  is '车商名称';
comment on column tp_special_info.group_dealer
  is '集团经销商代码';
comment on column tp_special_info.group_dealer_name
  is '集团经销商名称';
comment on column tp_special_info.contact_name
  is '联系人姓名';
comment on column tp_special_info.contact_tel
  is '联系电话';
comment on column tp_special_info.contact_address
  is '联系地址';
comment on column tp_special_info.specified_repair
  is '是否指定修理厂';
comment on column tp_special_info.agreed_repair
  is '是否约定返修';
comment on column tp_special_info.recommended_repair
  is '是否推荐送修';
comment on column tp_special_info.maintenance_limit
  is '每日送修限额';
comment on column tp_special_info.repair_limit
  is '每日返修限额';
comment on column tp_special_info.total_priority
  is '是否总对总优先';
comment on column tp_special_info.other_repair
  is '是否对其他车商送修';
comment on column tp_special_info.old_code
  is '原车商代码';
comment on column tp_special_info.modify_date
  is '记录修改时间';
comment on column tp_special_info.car_dealer
  is '是否已上传车商 y-是 n-否';
comment on column tp_special_info.right_show_org_price
  is '是否有权查看4s店价格';
comment on column tp_special_info.right_show_contract_price
  is '是否有权查看协议价格';
comment on column tp_special_info.right_show_market_price
  is '是否有权查看市场价格';
comment on column tp_special_info.right_show_fit_price
  is '是否有权查看适用价格';
comment on column tp_special_info.head_dispatch
  is '是否总调';
create index idx1_tp_special_info on tp_special_info (third_party_id);
alter table tp_special_info
  add primary key (id);