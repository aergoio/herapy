
rm *.key *.csr *.crt

# =====================================
# https://blocko.atlassian.net/wiki/spaces/~423089300/pages/745504821/Aergo+TLS

echo ""
echo "Create Root signing Key"
#openssl genrsa -aes256 -out rootca.key 4096
# no password
openssl genrsa -out rootca.key 4096

echo ""
echo "Create self-signed Root certificate"
openssl req -new -key rootca.key -out rootca.csr -config rootca_openssl.conf

echo ""
echo "Generate a certificate of the self-signed Root certificate"
openssl x509 -req -days 365 -extfile rootca_openssl.conf -extensions v3_ca -in rootca.csr -signkey rootca.key -out rootca.crt

echo ""
echo "Print the self-signed Root certificate"
openssl x509 -text -in rootca.crt

