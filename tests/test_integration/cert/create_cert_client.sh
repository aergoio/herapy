
# =====================================
# https://blocko.atlassian.net/wiki/spaces/~423089300/pages/745504821/Aergo+TLS

echo ""
echo "Create a Key certificate for Server"
# no password
openssl genrsa -out client.key 4096

echo ""
echo "Create a signing Certificate Signing Request (CSR) for Server"
openssl req -new -key client.key -out client.csr -config openssl.conf

echo ""
echo "Generate a certificate of the signed certificate for Server"
openssl x509 -req -days 365 -extfile openssl.conf -extensions v3_user -in client.csr -CA ../rootca/rootca.crt -CAkey ../rootca/rootca.key -CAcreateserial -out client.pem

echo ""
echo "Print the signed certificate for Server"
openssl x509 -text -in client.pem

