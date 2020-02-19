
# =====================================
# https://blocko.atlassian.net/wiki/spaces/~423089300/pages/745504821/Aergo+TLS

echo ""
echo "Create a Key certificate for Server"
# no password
openssl genrsa -out server.key 4096

echo ""
echo "Create a signing Certificate Signing Request (CSR) for Server"
openssl req -new -key server.key -out server.csr -config openssl.conf

echo ""
echo "Generate a certificate of the signed certificate for Server"
openssl x509 -req -days 365 -extfile openssl.conf -extensions v3_user -in server.csr -CA ../rootca/rootca.crt -CAkey ../rootca/rootca.key -CAcreateserial -out server.pem

echo ""
echo "Print the signed certificate for Server"
openssl x509 -text -in server.pem

