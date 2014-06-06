import os

from flaskext.enterprise import Enterprise
from soaplib.core.model.primitive import Any
from flask import Flask

app = Flask(__name__)

enterprise = Enterprise(app)
String = enterprise._sp.String
Integer = enterprise._sp.Integer
Boolean = enterprise._sp.Boolean
Array = enterprise._scls.Array
RequerimientoStruct_PayOnline_3p = Any
psp_MerchOrderId = String
psp_MerchTxRef = String
psp_CustomerMail = String
psp_SecureHash = String
psp_Amount = String
psp_MerchantId = String


class Service(enterprise.SOAPService):
    """Soap Service Class

    Attributes:
        __soap_target_namespace__ : namespace for soap service
        __soap_server_address__ : address of soap service
    """
    __soap_target_namespace__ = 'NPSFakeSoapService'
    __soap_server_address__ = '/soap'

    @enterprise.soap(Any, _returns=Any)
    def PayOnLine_3p(self, request, psp_MerchOrderId, psp_MerchTxRef,
        psp_CustomerMail, psp_SecureHash, psp_Amount, psp_MerchantId):
        """Autorizamos el inicio de un pago.
        """
        return request

    @enterprise.soap(Any, _returns=Any)
    def psp_MerchOrderId(self, request, psp_MerchOrderId, psp_MerchTxRef,
        psp_CustomerMail, psp_SecureHash, psp_Amount, psp_MerchantId):
        """Autorizamos el inicio de un pago.
        """
        return request


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5051))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
