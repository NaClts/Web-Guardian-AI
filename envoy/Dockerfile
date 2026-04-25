FROM envoyproxy/envoy:dev-90594f45b3ed30bfd4bdf8bb300944b93e40959f

RUN apt-get update && apt-get install -y gettext-base

WORKDIR /home/envoy

COPY envoy.yaml.tpl .

CMD envsubst < envoy.yaml.tpl > envoy.yaml \
    && envoy -c envoy.yaml --log-level info
