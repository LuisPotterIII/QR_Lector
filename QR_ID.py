import pyqrcode

ncuenta = 1926618

id = str(ncuenta)
qr = pyqrcode.create(id, error = 'L')

qr.png('ICO' + str(ncuenta) + '.png', scale = 6)