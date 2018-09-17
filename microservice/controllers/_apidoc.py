
"""
    @apiDefine UserNotFoundError 用户不存在或密码错误
    @apiError (Error 400) UserNotFound 用户不存在或密码错误
    @apiErrorExample Error-Response:
      HTTP/1.1 400 Not Found
      {
        "error": "用户名不存在或密码错误"
     }

"""

"""
    @apiDefine GetSheet 单据查询
    @apiParam  (入参) {int}  page=1  页数
    @apiParam  (入参) {string} sheet_no 单号,不传入则返回单据列表
    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Not Found
        {
            "message": "单号1234567890的单据不存在"
        }
        HTTP/1.1 400 Not Found
        {
            "message": "单据第2页不存在"
        }
"""


"""
    @apiDefine GetSheetByType 单据类型
    @apiParam (入参) {string} sheet_type 单据类型
    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Not Found
        {
            "message": "无效的单据类型"
        }
"""


"""
    @apiDefine supply 供应商
    此接口只能有供应商调用.
"""

"""
    @apiDefine AuthRequired 身份验证
    @apiParam (入参-签名) {string} token （必填）签名
    @apiError (AuthError 403) SignatureExpired 签名已过期
    @apiError (AuthError 401) SignatureExpired 签名不合法
"""



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
    @apiSuccess (order-details) {int} item_subnono 商品条码
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


