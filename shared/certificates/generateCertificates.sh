validity_contract_cert=730
validity_mo_subca1_cert=1460
validity_mo_subca2_cert=1460
validity_oem_prov_cert=1460
validity_oem_subca1_cert=1460
validity_oem_subca2_cert=1460
validity_cps_leaf_cert=90
validity_cps_subca1_cert=1460
validity_cps_subca2_cert=730
validity_secc_cert=60
validity_cpo_subca1_cert=1460
validity_cpo_subca2_cert=365
validity_v2g_root_cert=9125
validity_oem_root_cert=3650
validity_mo_root_cert=3650
validity_vehicle_subca1_cert=3650
validity_vehicle_subca1_cert=3650
validity_vehicle_subca2_cert=3650
validity_vehicle_cert=3650

mkdir -p certs
mkdir -p privateKeys
mkdir -p csrs


# TLS_CHACHA20_POLY1305_SHA256 cipher suite is used to encrypt private keys for local storage.
# This has no effect in the use of TLS_AES_256_GCM_SHA384 cipher suite or TLS_CHACHA20_POLY1305_SHA256

# v2gRootCA
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/v2gRootCA.key 
openssl req -new -key privateKeys/v2gRootCA.key -passin file:passphrase.txt -config configs/v2gRootCACert.cnf -out csrs/v2gRootCA.csr
openssl x509 -req -in csrs/v2gRootCA.csr -extfile configs/v2gRootCACert.cnf -extensions ext -signkey privateKeys/v2gRootCA.key -passin file:passphrase.txt -sha256 -set_serial 12345 -out certs/v2gRootCACert.pem -days $validity_v2g_root_cert

# cpoSubCA1
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/cpoSubCA1.key  
openssl req -new -key privateKeys/cpoSubCA1.key -passin file:passphrase.txt -config configs/cpoSubCA1Cert.cnf -out csrs/cpoSubCA1.csr
openssl x509 -req -in csrs/cpoSubCA1.csr -extfile configs/cpoSubCA1Cert.cnf -extensions ext -CA certs/v2gRootCACert.pem -CAkey privateKeys/v2gRootCA.key -passin file:passphrase.txt -set_serial 12345 -out certs/cpoSubCA1Cert.pem -days $validity_cpo_subca1_cert

# cpoSubCA2
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/cpoSubCA2.key
openssl req -new -key privateKeys/cpoSubCA2.key -passin file:passphrase.txt -config configs/cpoSubCA2Cert.cnf -out csrs/cpoSubCA2.csr
openssl x509 -req -in csrs/cpoSubCA2.csr -extfile configs/cpoSubCA2Cert.cnf -extensions ext -CA certs/cpoSubCA1Cert.pem -CAkey privateKeys/cpoSubCA1.key -passin file:passphrase.txt -set_serial 12345 -out certs/cpoSubCA2Cert.pem -days $validity_cpo_subca2_cert 

# seccCert
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/secc.key 
openssl req -new -key privateKeys/secc.key -passin file:passphrase.txt -config configs/seccCert.cnf -out csrs/seccCert.csr
openssl x509 -req -in csrs/seccCert.csr -extfile configs/seccCert.cnf -extensions ext -CA certs/cpoSubCA2Cert.pem -CAkey privateKeys/cpoSubCA2.key -passin file:passphrase.txt -set_serial 12345 -out certs/seccCert.pem -days $validity_secc_cert 

# seccCertChain
cat certs/seccCert.pem certs/cpoSubCA2Cert.pem certs/cpoSubCA1Cert.pem > certs/seccCertChain.pem

# oemRootCA
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/oemRootCA.key 
openssl req -new -key privateKeys/oemRootCA.key -passin file:passphrase.txt -config configs/oemRootCACert.cnf -out csrs/oemRootCA.csr
openssl x509 -req -in csrs/oemRootCA.csr -extfile configs/oemRootCACert.cnf -extensions ext -signkey privateKeys/oemRootCA.key -passin file:passphrase.txt -sha256 -set_serial 12345 -out certs/oemRootCACert.pem -days $validity_oem_root_cert

# vehicleSubCA1
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/vehicleSubCA1.key  
openssl req -new -key privateKeys/vehicleSubCA1.key -passin file:passphrase.txt -config configs/vehicleSubCA1Cert.cnf -out csrs/vehicleSubCA1.csr
openssl x509 -req -in csrs/vehicleSubCA1.csr -extfile configs/vehicleSubCA1Cert.cnf -extensions ext -CA certs/oemRootCACert.pem -CAkey privateKeys/oemRootCA.key -passin file:passphrase.txt -set_serial 12345 -out certs/vehicleSubCA1Cert.pem -days $validity_vehicle_subca1_cert

# vehicleSubCA2
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/vehicleSubCA2.key
openssl req -new -key privateKeys/vehicleSubCA2.key -passin file:passphrase.txt -config configs/vehicleSubCA2Cert.cnf -out csrs/vehicleSubCA2.csr
openssl x509 -req -in csrs/vehicleSubCA2.csr -extfile configs/vehicleSubCA2Cert.cnf -extensions ext -CA certs/vehicleSubCA1Cert.pem -CAkey privateKeys/vehicleSubCA1.key -passin file:passphrase.txt -set_serial 12345 -out certs/vehicleSubCA2Cert.pem -days $validity_vehicle_subca2_cert 

# vehicleCert
openssl ecparam -genkey -name secp521r1 | openssl ec -chacha20 -passout file:passphrase.txt -out privateKeys/vehicle.key 
openssl req -new -key privateKeys/vehicle.key -passin file:passphrase.txt -config configs/vehicleCert.cnf -out csrs/vehicleCert.csr
openssl x509 -req -in csrs/vehicleCert.csr -extfile configs/vehicleCert.cnf -extensions ext -CA certs/vehicleSubCA2Cert.pem -CAkey privateKeys/vehicleSubCA2.key -passin file:passphrase.txt -set_serial 12345 -out certs/vehicleCert.pem -days $validity_vehicle_cert 

# vehicleCertChain
cat certs/vehicleCert.pem certs/vehicleSubCA2Cert.pem certs/vehicleSubCA1Cert.pem > certs/vehicleCertChain.pem
