###############################################
"""
    @apiDefine UserNotFoundError 用户不存在或密码错误
    @apiError (Error 400) UserNotFound 用户不存在或密码错误
"""
###############################################


###############################################
"""
   @apiDefine ErrorExample
   @apiErrorExample {json} Error-Response:
   HTTP/1.1 4xx
   {
        "message": "ErrorMessage"
        "code": "ErrorCode "
   }
"""
###############################################


###############################################
"""
    @apiDefine GetSheet 单据查询
    @apiParam  (入参) {int}  page=1  页数
    @apiError  (SheetError 400) SheetNoNotValid 无效的单号
    @apiParam  (入参) {string} sheet_no 单号,不传入则返回单据列表
    @apiError  (SheetError 400) SheetNotFound 单据不存在
    @apiError  (SheetError 400) PageOfSheetNotFound 单据页不存在
"""
###############################################


###############################################
"""
    @apiDefine PutSheet 单据修改
    @apiParam  (入参) {string} sheet_no （必须）单号
    @apiError  (SheetError 400) SheetNoNotValid 无效的单号
    @apiError  (SheetError 400) SheetNotFound 单据不存在  
    @apiError  (SheetError 401) PermissionNotAllowed 权限不足 
    @apiError  (SheetError 400) SheetAlreadyDone 单据已处理 
    @apiSuccess (回参) {string} sheet_no 单据编号
"""
###############################################


###############################################
"""
    @apiDefine GetSheetByType 单据类型
    @apiParam (入参) {string} sheet_type 单据类型
    @apiError (SheetError 403)SheetTypeRequired  无效的单据类型
"""
###############################################


###############################################
"""
    @apiDefine supply 供应商权限
    此接口只能有供应商调用.
"""
###############################################


###############################################
"""
    @apiDefine AuthRequired 身份验证
    @apiParam (入参-签名) {string} Token （必填） 签名
    @apiError (AuthError 403) SignatureExpired 签名已过期
    @apiError (AuthError 401) SignatureExpired 签名不合法
"""
###############################################


###############################################
"""
    @apiDefine OrderReturnParam 订单回传参数
    @apiSuccess (回参) {object[]} order 订单
    @apiSuccess (order) {string} sheet_type 单据类型
    @apiSuccess (order) {string} sup_no 供应商编码
    @apiSuccess (order) {string} sup_name 供应商名称
    @apiSuccess (order) {string} brh_no 机构编码
    @apiSuccess (order) {string} brh_name 机构名称
    @apiSuccess (order) {string} po_brh_no 订货机构编码
    @apiSuccess (order) {decimal} sum_amt 合计金额
    @apiSuccess (order) {date} deliver_date 送货日期
    @apiSuccess (order) {date} valid_date 失效日期
    @apiSuccess (order) {date} cr_date 制单日期
    @apiSuccess (order) {time} cr_time 制单时间
    @apiSuccess (order) {string}  status 单据状态
    @apiSuccess (order) {string}  cr_oper_no 制单人
    @apiSuccess (order) {object[]}  details 订单明细
    @apiSuccess (order) {object[]}  brs 门店列表

    @apiSuccess (order-details) {int} line_id 行号
    @apiSuccess (order-details) {int} item_id 商品ID
    @apiSuccess (order-details) {int} item_subno 商品条码
    @apiSuccess (order-details) {string} item_name 商品名称
    @apiSuccess (order-details) {string} unit_no 单位
    @apiSuccess (order-details) {decimal} pack_qty 件数
    @apiSuccess (order-details) {decimal} unit_qty 包装因子
    @apiSuccess (order-details) {decimal} qty 数量
    @apiSuccess (order-details) {decimal} price 价格
    @apiSuccess (order-details) {decimal} amt 金额
    @apiSuccess (order-brs) {int} line_id 行号
    @apiSuccess (order-brs) {int} item_id 商品ID
    @apiSuccess (order-brs) {string} brh_no 机构编码
    @apiSuccess (order-brs) {decimal} qty 数量

"""
###############################################


###############################################
"""
    @apiDefine InoutReturnParam 出入库回传参数
    @apiSuccess (回参) {object[]} inout 出入库单据
    @apiSuccess (inout) {string} sheet_no 单号
    @apiSuccess (inout) {string} sheet_type 单据类型
    @apiSuccess (inout) {string} src_no 来源单据
    @apiSuccess (inout) {string} sup_no 供应商编码
    @apiSuccess (inout) {string} sup_name 供应商名称
    @apiSuccess (inout) {string} brh_no 机构编码
    @apiSuccess (inout) {string} brh_name 机构名称
    @apiSuccess (inout) {decimal} sum_amt 合计金额
    @apiSuccess (inout) {date} cr_date 制单日期
    @apiSuccess (inout) {time} cr_time 制单时间
    @apiSuccess (inout) {string}  status 单据状态
    @apiSuccess (inout) {string}  cr_oper_no 制单人
    @apiSuccess (inout) {object[]}  details 单据明细


    @apiSuccess (inout-details) {int} line_id 行号
    @apiSuccess (inout-details) {int} item_id 商品ID
    @apiSuccess (inout-details) {int} item_subno 商品条码
    @apiSuccess (inout-details) {string} item_name 商品名称
    @apiSuccess (inout-details) {string} unit_no 单位
    @apiSuccess (inout-details) {decimal} pack_qty 件数
    @apiSuccess (inout-details) {decimal} unit_qty 包装因子
    @apiSuccess (inout-details) {decimal} qty 数量
    @apiSuccess (inout-details) {decimal} price 价格
    @apiSuccess (inout-details) {decimal} amt 金额


"""
###############################################


###############################################
"""
    @apiDefine StockSuccessParam 
    @apiSuccess (Stock) {string} brh_no   门店编码
    @apiSuccess (Stock) {string} brh_name 门店名称
    @apiSuccess (Stock) {string} wh_no    仓库编码
    @apiSuccess (Stock) {string} wh_name  仓库名称
    @apiSuccess (Stock) {string} item_no  商品编码
    @apiSuccess (Stock) {string} item_subno  商品条码
    @apiSuccess (Stock) {string} item_name  商品名称
    @apiSuccess (Stock) {decimal} qty  库存数量（最小单位）
"""
###############################################
