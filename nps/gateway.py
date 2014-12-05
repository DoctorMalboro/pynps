# -*- coding: utf-8 *-*

import hashlib
from suds.client import Client


class NPSGateway(object):

    def create_secure_hash_for(self, transaction):
        """ Permite al NPS controlar la integridad del mensaje enviado
        por el cliente. El campo psp_SecureHash es una firma md5 generada
        de la siguiente forma:
            md5_input = Contenido de campos del mensaje concatenados +
                        Secure Hash Secret
            psp_SecureHash = md5(md5_input)
        Nota: Los campos deben estar ordenados, por nombre de campo,
        alfabéticamente en forma ascendente.
        """

        request = transaction.request
        keys = sorted(request.items.keys())
        hash_values = []
        for kw in keys:
            if kw == 'psp_SecureHash':
                continue
            value = request.items[kw] if request.items[kw] != None else ''
            hash_values.append(str(value))
        hash_values.append(transaction.secret)
        input_ = ''.join([v for v in hash_values if v])
        m = hashlib.md5()
        m.update(input_.encode('utf-8'))

        return m.hexdigest()

    def process(self, transaction):
        """Procesa la transaccion dada contra el WSDL de NPS.
        Retorna el objeto transaccion pasado.
        """

        request = transaction.request
        url = transaction.url

        factory = transaction.factory
        method = transaction.method
        client = Client(url)

        request.psp_SecureHash = self.create_secure_hash_for(transaction)
        ws_factory = client.factory.create(factory)
        ws_method = getattr(client.service, method)

        for key, value in request.items.items():
            if not value:
                continue
            ws_factory[key] = value

        response = ws_method(ws_factory)  # call the webservice
        if hasattr(response, 'psp_Transaction'):
            transaction.response.user_data = getattr(response,
                                                'psp_Transaction')
        for kw in transaction.response.items.keys():
            if response.__contains__(kw):
                value = getattr(response, kw)
                transaction.response[kw] = value

        return transaction  # return the transaction
