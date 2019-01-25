import uuid, sys, time, os, shutil, json, cx_Oracle, codecs, traceback
from flask import (
    Flask, request, render_template, Blueprint
)
from flask_json import FlaskJSON, JsonError, json_response, as_json


app = Flask(__name__)
FlaskJSON(app)
bp = Blueprint('paymentIn', __name__, url_prefix='/maintain/paymentIn', static_folder='static')
username, password, dbUrl = "username", "password", "127.0.0.1:1521/orcl"
appStatus = {"01": "暂存"}
appStatus["02"] = "申报中"
appStatus["03"] = "发送电子口岸成功"
appStatus["04"] = "发送电子口岸失败"
appStatus["05"] = "电子口岸校验失败"
appStatus["120"] = "海关入库"
appStatus["100"] = "海关退单"
appStatus["2"] = "电子口岸申报中"


def executeSql(sql, **kw):
    con = cx_Oracle.connect(username, password, dbUrl)
    cursor = con.cursor()
    result = None
    try:
        cursor.prepare(sql)
        cursor.execute(None, kw)
        result = cursor.fetchall()
        con.commit()
    except Exception as e:
        traceback.print_exc()
        con.rollback()
    finally:
        cursor.close()
        con.close()
    return result


@bp.route('/queryByOrderNo')
def queryByOrderNo():
    orderNo = request.values.get('orderNo')
    print("orderNo=[", orderNo, "]")
    sql = '''
    select cph.ord_no, cph.ebp_name, cph.ebp_code, cph.pay_transaction_id, cph.pay_name, cph.pay_code, time_to_char(cph.sys_date), cph.app_status from ceb2_pay_head cph
where cph.ord_no = :orderNo
    '''
    result = []
    if orderNo:
        result = executeSql(sql, orderNo = orderNo)
    return render_template('query_by_order_no.html', result = result, appStatus = appStatus, key = orderNo)


@bp.route('/queryByPaymentNumber')
def queryByPaymentNumber():
    paymentNumber = request.values.get('paymentNumber')
    print("paymentNumber=[", paymentNumber, "]")
    sql = '''
    select cph.ord_no, cph.ebp_name, cph.ebp_code, cph.pay_transaction_id, cph.pay_name, cph.pay_code, time_to_char(cph.sys_date), cph.app_status from ceb2_pay_head cph
where cph.pay_transaction_id = :paymentNumber
    '''
    result = []
    if paymentNumber:
        result = executeSql(sql, paymentNumber = paymentNumber)
    return render_template('query_by_payment_number.html', result = result, appStatus = appStatus, key = paymentNumber)


app.register_blueprint(bp)
