from enum import Enum
import re


class SheetBase:
    per_page = 10
    flag_done_yes = '1'

    @staticmethod
    def sheet_no_validator(sheet_no):
        pattern = re.compile(r'\d{8}[A-Z]{2}\d{4}')
        return pattern.match(sheet_no)


class SheetStatus(Enum):
    """单据状态"""
    draft = '0'     # 草稿
    submit = '1'    # 提交
    recall = '2'    # 召回
    approve = '5'   # 审核
    discard = '9'   # 作废


class SheetType(Enum):
    do = 'DO'  # 直配
    po = 'PO'  # 采购
    zo = 'ZO'  # 越库
    op = 'OP'  # 永续
    pi = 'PI'  # 采购收货
    ro = 'RO'  # 采购退货
    qs = "QS"
    qt = "QT"


class SheetSlice:
    """单据切片"""
    sheet_grp_slice = slice(6, 8)


class ErrorCode(Enum):
    sheet_not_found = "SheetNotFound"
    page_of_sheet_not_found = "PageOfSheetNotFound"
    permission_not_allowed = "PermissionNotAllowed"
    sheet_already_done = "SheetAlreadyDone"
    sheet_type_required = "SheetTypeRequired"
    signature_expired = "SignatureExpired"
    signature_required = "SignatureExpired"
    user_not_found = "UserNotFound"
    sheet_no_not_valid = "SheetNoNotValid"



