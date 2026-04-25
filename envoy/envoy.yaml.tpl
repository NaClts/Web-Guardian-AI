static_resources:
  listeners:
  - name: listener_0
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 80
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          access_log:
          - name: envoy.access_loggers.stdout
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.access_loggers.stream.v3.StdoutAccessLog
          http_filters:
            # 1) External authz filter FIRST (before router)
            - name: envoy.filters.http.ext_authz
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
                http_service:
                  server_uri:
                    uri: http://auth-service-py:60680
                    cluster: ext_authz
                    timeout: 60s
                  authorization_request:
                    allowed_headers:
                      patterns:
                      # Include all headers
                      - safe_regex:
                          google_re2: {}
                          regex: ".*"
                with_request_body:
                  max_request_bytes: 8192
                  allow_partial_message: true
                  pack_as_bytes: true
                include_peer_certificate: false
                include_tls_session: true
                failure_mode_allow: false
            # 2) Router filter
            - name: envoy.filters.http.router
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
          route_config:
            name: local_route
            virtual_hosts:
            - name: app_vhost
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                route:
                  host_rewrite_literal: ${WEB_APP_HOST}
                  cluster: web_app_service

  clusters:
    - name: web_app_service
      type: LOGICAL_DNS
      # Comment out the following line to test on v6 networks
      dns_lookup_family: V4_ONLY
      load_assignment:
        cluster_name: web_app_service
        endpoints:
        - lb_endpoints:
          - endpoint:
              address:
                socket_address:
                  address: ${WEB_APP_HOST}
                  port_value: ${WEB_APP_PORT}
      # transport_socket:
      #   name: envoy.transport_sockets.tls
      #   typed_config:
      #     "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext
      #     sni: ${WEB_APP_HOST}
    - name: ext_authz
      type: LOGICAL_DNS
      lb_policy: ROUND_ROBIN
      load_assignment:
        cluster_name: ext_authz
        endpoints:
        - lb_endpoints:
          - endpoint:
              address:
                socket_address:
                  address: auth-service-py
                  port_value: 60680
