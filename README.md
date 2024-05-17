# secure-prometheus-target-connection
A simple script to enable basic auth and TLS encryption to the connection of prometheus server to a target server.

# How to use
- On Target server:
  1. Clone repo to your target server  (server with NodeExporter installed)
  2. cd to NodeExporter dir.
  3. Execute script using 'sudo bash secure_node_exporter.sh'
  4. Enter password for use with Basic Auth when prompted. (Not to be confused with sudo password prompt)
  5. node_exporter.crt is generated on current working directory, copy it to Prometheus server with scp command or any other tool or method of your choice.

- On Prometheus server:
  1. Clone repo to your Prometheus server.
  2. Move node_exporter.crt from step 5 above to PrometheusServer dir.
  3. cd to PrometheusServer dir.
  4. Execute script using 'sudo bash configure_server.sh'
  5. Enter same password used on target server script.
  6. Enter job_name of target server (can be found at /etc/prometheus/prometheus.yml), THIS IS IMPORTANT AND CASE-SENSITIVE!
     Specifying wrong name breaks the script, and it will not modify config file.
  7. If it prompts 'Config updated successfully.', then you are done.

  and you have completed!
  Now, scraping of metric data from targets is secured using TLS and Basic Authentication.

# Modifying parameters in script
  - On target script, you can edit openssl cmd to customize your ssl
        openssl req -x509 \
        -newkey rsa:4096 \
        -nodes \
        -days 365 \    # This no of days the certificate will remain valid.
        -keyout /etc/node_exporter/node_exporter.key \
        -out /etc/node_exporter/node_exporter.crt \
        -subj "/O=MyCompany/OU=MyDivision/CN=mydomain.local" \ #This CN, OU and other names, customize to your preference.
	      -addext "subjectAltName = DNS:mydomain.local"      # This should match CN for prometheus server to be able to validate target identity.

    You can as well, use your own certificate if you have one for your owned domain and not issue this command at all.
