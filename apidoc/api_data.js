define({ "api": [
  {
    "type": "post",
    "url": "/api/auth",
    "title": "获取令牌",
    "version": "1.0.0",
    "name": "auth",
    "group": "安全校验",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "user_no",
            "description": "<p>（必须）  用户名</p>"
          },
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "password",
            "description": "<p>（必须）  密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "回参": [
          {
            "group": "回参",
            "type": "string",
            "optional": false,
            "field": "token",
            "description": "<p>令牌</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"token\": \"1234567890\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "MicroService/controllers/auth.py",
    "groupTitle": "安全校验",
    "error": {
      "fields": {
        "Error 400": [
          {
            "group": "Error 400",
            "optional": false,
            "field": "UserNotFound",
            "description": "<p>用户不存在或密码错误</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": " HTTP/1.1 400 Not Found\n {\n   \"error\": \"用户名不存在或密码错误\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/order/:sheet_no",
    "title": "获取订单信息",
    "version": "1.0.0",
    "name": "order",
    "group": "订单",
    "permission": [
      {
        "name": "supply",
        "title": "供应商",
        "description": "<p>此接口只能有供应商调用.</p>"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]\n}",
          "type": "json"
        }
      ],
      "fields": {
        "回参": [
          {
            "group": "回参",
            "type": "object[]",
            "optional": false,
            "field": "order",
            "description": "<p>订单</p>"
          }
        ],
        "order": [
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "sheet_type",
            "description": "<p>单据类型</p>"
          },
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "sup_no",
            "description": "<p>供应商编码</p>"
          },
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "sup_name",
            "description": "<p>供应商名称</p>"
          },
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "brh_no",
            "description": "<p>机构编码</p>"
          },
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "brh_name",
            "description": "<p>机构名称</p>"
          },
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "po_brh_no",
            "description": "<p>订货机构编码</p>"
          },
          {
            "group": "order",
            "type": "decimal",
            "optional": false,
            "field": "sum_amt",
            "description": "<p>合计金额</p>"
          },
          {
            "group": "order",
            "type": "date",
            "optional": false,
            "field": "deliver_date",
            "description": "<p>送货日期</p>"
          },
          {
            "group": "order",
            "type": "date",
            "optional": false,
            "field": "valid_date",
            "description": "<p>失效日期</p>"
          },
          {
            "group": "order",
            "type": "date",
            "optional": false,
            "field": "cr_date",
            "description": "<p>制单日期</p>"
          },
          {
            "group": "order",
            "type": "time",
            "optional": false,
            "field": "cr_time",
            "description": "<p>制单时间</p>"
          },
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "status",
            "description": "<p>单据状态</p>"
          },
          {
            "group": "order",
            "type": "string",
            "optional": false,
            "field": "cr_oper_no",
            "description": "<p>制单人</p>"
          },
          {
            "group": "order",
            "type": "object[]",
            "optional": false,
            "field": "details",
            "description": "<p>订单明细</p>"
          },
          {
            "group": "order",
            "type": "object[]",
            "optional": false,
            "field": "brs",
            "description": "<p>门店列表</p>"
          }
        ],
        "order-details": [
          {
            "group": "order-details",
            "type": "int",
            "optional": false,
            "field": "line_id",
            "description": "<p>行号</p>"
          },
          {
            "group": "order-details",
            "type": "int",
            "optional": false,
            "field": "item_id",
            "description": "<p>商品ID</p>"
          },
          {
            "group": "order-details",
            "type": "int",
            "optional": false,
            "field": "item_subnono",
            "description": "<p>商品条码</p>"
          },
          {
            "group": "order-details",
            "type": "string",
            "optional": false,
            "field": "item_name",
            "description": "<p>商品名称</p>"
          },
          {
            "group": "order-details",
            "type": "string",
            "optional": false,
            "field": "unit_no",
            "description": "<p>单位</p>"
          },
          {
            "group": "order-details",
            "type": "decimal",
            "optional": false,
            "field": "pack_qty",
            "description": "<p>件数</p>"
          },
          {
            "group": "order-details",
            "type": "decimal",
            "optional": false,
            "field": "unit_qty",
            "description": "<p>包装因子</p>"
          },
          {
            "group": "order-details",
            "type": "decimal",
            "optional": false,
            "field": "qty",
            "description": "<p>数量</p>"
          },
          {
            "group": "order-details",
            "type": "decimal",
            "optional": false,
            "field": "price",
            "description": "<p>价格</p>"
          },
          {
            "group": "order-details",
            "type": "decimal",
            "optional": false,
            "field": "amt",
            "description": "<p>金额</p>"
          }
        ],
        "order-brs": [
          {
            "group": "order-brs",
            "type": "int",
            "optional": false,
            "field": "line_id",
            "description": "<p>行号</p>"
          },
          {
            "group": "order-brs",
            "type": "int",
            "optional": false,
            "field": "item_id",
            "description": "<p>商品ID</p>"
          },
          {
            "group": "order-brs",
            "type": "string",
            "optional": false,
            "field": "brh_no",
            "description": "<p>机构编码</p>"
          },
          {
            "group": "order-brs",
            "type": "decimal",
            "optional": false,
            "field": "qty",
            "description": "<p>数量</p>"
          }
        ]
      }
    },
    "filename": "MicroService/controllers/order.py",
    "groupTitle": "订单",
    "parameter": {
      "fields": {
        "入参-签名": [
          {
            "group": "入参-签名",
            "type": "string",
            "optional": false,
            "field": "token",
            "description": "<p>（必填）签名</p>"
          }
        ],
        "入参": [
          {
            "group": "入参",
            "type": "int",
            "optional": false,
            "field": "page",
            "defaultValue": "1",
            "description": "<p>页数</p>"
          },
          {
            "group": "入参",
            "type": "string",
            "optional": false,
            "field": "sheet_no",
            "description": "<p>单号,不传入则返回单据列表</p>"
          },
          {
            "group": "入参",
            "type": "string",
            "optional": false,
            "field": "sheet_type",
            "description": "<p>单据类型</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "AuthError 403": [
          {
            "group": "AuthError 403",
            "optional": false,
            "field": "SignatureExpired",
            "description": "<p>签名已过期</p>"
          }
        ],
        "AuthError 401": [
          {
            "group": "AuthError 401",
            "optional": false,
            "field": "SignatureExpired",
            "description": "<p>签名不合法</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Not Found\n{\n    \"message\": \"单号1234567890的单据不存在\"\n}\nHTTP/1.1 400 Not Found\n{\n    \"message\": \"单据第2页不存在\"\n}",
          "type": "json"
        },
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Not Found\n{\n    \"message\": \"无效的单据类型\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/order/do/:sheet_no",
    "title": "直配订单",
    "version": "1.0.0",
    "name": "order_do",
    "group": "订单",
    "parameter": {
      "fields": {
        "入参": [
          {
            "group": "入参",
            "type": "int",
            "optional": false,
            "field": "page",
            "defaultValue": "1",
            "description": "<p>页数</p>"
          },
          {
            "group": "入参",
            "type": "string",
            "optional": false,
            "field": "sheet_no",
            "description": "<p>单号,不传入则返回单据列表</p>"
          }
        ]
      }
    },
    "permission": [
      {
        "name": "supply",
        "title": "供应商",
        "description": "<p>此接口只能有供应商调用.</p>"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    [{'sheet_no': '18091700DO0130', 'sheet_type': 'DO', 'sup_no': '203701', 'sup_name': '湖北致远天下贸易有限公司', 'brh_no': '9999', 'brh_name': '中百好邦干货物流仓', 'po_brh_no': '', 'sum_amt': 8324.0, 'deliver_date': '2018-09-20', 'valid_date': '2018-09-21', 'cr_date': '2018-09-17', 'cr_time': '15:41:36', 'status': '5', 'cr_oper_no': '0122', 'details': [{'line_id': 1, 'item_id': 6386, 'item_subno': '3211203450258', 'item_name': 'CASTEL卡柏莱美乐干红（木盒）750ml', 'unit_no': '瓶', 'pack_qty': 12.0, 'unit_qty': 1.0, 'qty': 12.0, 'price': 102.0, 'amt': 1224.0}, {'line_id': 2, 'item_id': 8759, 'item_subno': '8004385033310', 'item_name': '天使之手干红葡萄酒', 'unit_no': '瓶', 'pack_qty': 100.0, 'unit_qty': 1.0, 'qty': 100.0, 'price': 71.0, 'amt': 7100.0}], 'brs': [{'line_id': 1, 'item_id': 6386, 'brh_no': '0001', 'qty': 6.0}, {'line_id': 2, 'item_id': 6386, 'brh_no': '0002', 'qty': 6.0}, {'line_id': 3, 'item_id': 8759, 'brh_no': '0001', 'qty': 50.0}, {'line_id': 4, 'item_id': 8759, 'brh_no': '0002', 'qty': 50.0}]}]\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 Not Found\n{\n    \"message\": \"订单1234567890不存在\"\n}\nHTTP/1.1 400 Not Found\n{\n    \"message\": \"订单第2页不存在\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "MicroService/controllers/order.py",
    "groupTitle": "订单"
  }
] });
