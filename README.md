# secure-prometheus-target-conn-script
A simple script to enable basic auth and TLS encryption to the connection of Prometheus server to a target server written with python and bash scripting.

# How to use 
- On Target server: (See Modifying parameters first, to set CN and subjectAltName in TLS cert to your own)
  1. Clone repo to your target server  (server with NodeExporter installed)
  2. cd to NodeExporter dir.
  3. Execute script using 'sudo bash secure_node_exporter.sh'
  4. Enter password for use with Basic Auth when prompted. (Not to be confused with sudo password prompt)
  5. node_exporter.crt is generated on current working directory, copy it to Prometheus server with scp command or any other tool or method of your choice.

- On Prometheus server:
  * Target server must be configured in /etc/prometheus/prometheus.yml using hostname (same as cert's CN and subjectAltName) instead of IP for TLS to work, you can use /etc/hosts to achieve this.
  1. Clone repo to your Prometheus server.
  2. Move node_exporter.crt from step 5 above to PrometheusServer dir.
  3. cd to PrometheusServer dir.
  4. Execute script using 'sudo bash configure_server.sh'
  5. Enter same password used on target server script.
  6. Enter job_name of target server (can be found at /etc/prometheus/prometheus.yml), <br />
     THIS IS IMPORTANT AND CASE-SENSITIVE!
     Specifying wrong name breaks the script, and it will not modify config file.
  8. If it prompts 'Config updated successfully.', then you are done.

  and you have completed!
  Now, scraping of metric data from targets is secured using TLS and Basic Authentication.
# Important!
  - If use IPs instead of hostnames as generated using openssl
# Modifying parameters in script
  - On target script 'secure_node_exporter.sh', you can edit openssl cmd to customize your ssl
        openssl req -x509 \
        -newkey rsa:4096 \
        -nodes \
        -days 365 \ <br />     # This no of days the certificate will remain valid. <br />
        -keyout /etc/node_exporter/node_exporter.key \ <br />
        -out /etc/node_exporter/node_exporter.crt \  <br />
        -subj "/O=MyCompany/OU=MyDivision/CN=mydomain.local" \ <br />
	 #This CN, OU and other names, customize to your preference. <br />
	      -addext "subjectAltName = DNS:mydomain.local"      <br /> # This should match CN for prometheus server to be able to validate target identity. <br />

    You can as well, use your own certificate if you have one for your own domain and not issue this command at all.
