import qrcode
import cStringIO
import base64

def render(data):

    """
    This function renders the QR code containing the input data
    :param data: Data to be encoded into the QR code
    :return: dataURI of the QR code
    """
    code = qrcode.QRCode(version=None, error_correction=qrcode.ERROR_CORRECT_H,)
    code.add_data(data)
    code.make(fit=True)

    buff = cStringIO.StringIO()
    img = code.make_image()
    img.save(buff, "PNG")

    o = base64.b64encode(buff.getvalue())
    return 'data:image/png;base64,' + o



if __name__ == '__main__':
    test = "Hello! This message is encoded in the QR Code"
    print render(test)