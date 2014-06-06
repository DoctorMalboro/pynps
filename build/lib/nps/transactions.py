# -*- coding: utf-8 *-*


from nps import fields
from nps.config import settings


class BaseRequestResponse(object):

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @property
    def items(self):
        data = dict()
        for k in [k for k in self.__class__.__dict__ if
            k.startswith('psp')]:
            data[k] = getattr(self, k)
        return data


class PayOnlineTransactionThreeStepsRequest(BaseRequestResponse):
    """Camos utilizados en un request de tres pasos."""

    psp_ReturnURL = fields.Url()
    psp_SecureHash = fields.MD5()
    psp_CustomerMail = fields.Email()
    psp_MerchantMail = fields.Email()
    psp_FrmBackButtonURL = fields.Url()
    psp_PosDateTime = fields.DateTime()
    psp_Amount = fields.Amount(max_length=12)
    psp_Product = fields.Numeric(max_length=3)
    psp_Currency = fields.Alfanumeric(length=3)
    psp_MerchTxRef = fields.Order(max_length=64)
    psp_MerchOrderId = fields.Order(max_length=64)
    psp_NumPayments = fields.Numeric(max_length=2)
    psp_MerchantId = fields.MerchantId(max_length=14)
    psp_PurchaseDescription = fields.Alfa(max_length=15)
    psp_FrmLanguage = fields.Order(min_length=2, max_length=5)
    psp_Version = fields.Order(max_length=12, default='2.2')

    psp_Country = fields.Country(length=3,
        in_=settings.ALLOWED_COUNTRIES, default='ARG')
    psp_TxSource = fields.Alfa(max_length=13,
        in_=settings.ALLOWED_TX_SOURCES, default='WEB')


class PayOnlineTransactionThreeStepsResponse(BaseRequestResponse):
    """Camos de respuesta ante un request de tres pasos."""

    psp_ResponseCod = fields.Numeric(max_length=3)
    psp_ResponseMsg = fields.Text(max_length=255)
    psp_TransactionId = fields.Numeric(max_length=19)
    psp_Session3p = fields.Alfanumeric(max_length=64)
    psp_FrontPSP_URL = fields.Url()
    psp_MerchantId = fields.MerchantId(max_length=14)
    psp_MerchTxRef = fields.Order(max_length=64)
    psp_MerchOrderId = fields.Order(max_length=64)
    psp_CustomerMail = fields.Email()
    psp_MerchantMail = fields.Email()
    psp_PosDateTime = fields.Text(max_length=255)
    psp_ResponseExtended = fields.Text(max_length=255)


class PayOnlineTransactionThreeSteps(object):
    """ Clase para las transacciones de Compras en Linea.
        Se produce la autorización y la confirmación de la compra en el mismo
        instante, descontándose los fondos de la cuenta del poseedor de la
        tarjeta.
    """

    method = u'PayOnLine_3p'
    factory = u'RequerimientoStruct_PayOnLine_3p'

    def __init__(self, url, merchant_id, secret):
        """ Parametros del constructor:
                url: Url del servicio de NPS.
                merchant_id: Usuario dado por NPS
                secret: El password utilizado con merchant_id.
        """
        self.url = url
        self.merchant_id = merchant_id
        self.secret = secret
        self.request = PayOnlineTransactionThreeStepsRequest()
        self.response = PayOnlineTransactionThreeStepsResponse()

    @property
    def success(self):
        return len(self.errors) == 0

    @property
    def errors(self):
        errors = list()
        if 'Error' in self.response.psp_ResponseMsg:
            errors.append(
                dict(
                    psp_ResponseMsg=self.response.psp_ResponseMsg,
                    psp_ResponseCod=self.response.psp_ResponseCod,
                    psp_ResponseExtended=self.response.psp_ResponseExtended,
                    psp_MerchantId=self.response.psp_MerchantId,
                    psp_MerchOrderId=self.response.psp_MerchOrderId,
                    psp_CustomerMail=self.response.psp_CustomerMail,
                    psp_MerchTxRef=self.response.psp_MerchTxRef
                    )
                )
        return errors


class SimpleQueryTxRquest(BaseRequestResponse):
    """Campos de request de una consulta SimpleQueryTx."""

    psp_Version = fields.Order(max_length=12, default='2.2')
    psp_MerchantId = fields.MerchantId(max_length=14)
    psp_QueryCriteria = fields.Alfanumeric(length=1)
    psp_QueryCriteriaId = fields.Alfanumeric(max_length=64)
    psp_PosDateTime = fields.DateTime()
    psp_SecureHash = fields.MD5()


class SimpleQueryTxResponse(BaseRequestResponse):
    """Campos de response de una consulta SimpleQueryTx."""

    psp_ResponseCod = fields.Numeric(max_length=3)
    psp_ResponseMsg = fields.Text(max_length=255)
    psp_ResponseExtended = fields.Text(max_length=255)
    psp_MerchantId = fields.MerchantId(max_length=14)
    psp_QueryCriteria = fields.Alfanumeric(length=1)
    psp_QueryCriteriaId = fields.Alfanumeric(max_length=64)
    psp_PosDateTime = fields.Text(max_length=255)


class SimpleQueryTx(object):
    """Transaccion para obtener los detalles de una compra hecha."""

    method = 'SimpleQueryTx'
    factory = u'RequerimientoStruct_SimpleQueryTx'

    def __init__(self, url, merchant_id, secret,  psp_TransactionId, psp_MerchTxRef):
        """ Parametros del constructor:
                url: Url del servicio de NPS.
                merchant_id: Usuario dado por NPS
                secret: El password utilizado con merchant_id.
        """
        self.url = url
        self.merchant_id = merchant_id
        self.secret = secret
        self.request = SimpleQueryTxRquest()
        self.request.psp_MerchantId = merchant_id
        self.request.psp_QueryCriteriaId = int(psp_MerchTxRef)
        self.response = SimpleQueryTxResponse()
