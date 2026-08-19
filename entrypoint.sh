#!/bin/sh
set -e

# 1. Substitute environment variables using sed
sed "s|\${ALERT_SLACK_WEBHOOK}|$ALERT_SLACK_WEBHOOK|g" \
  /etc/alertmanager/alertmanager.template.yml > /tmp/alertmanager.yml

# 2. Start Alertmanager with the substituted config
exec /bin/alertmanager \
  --config.file=/tmp/alertmanager.yml \
  --storage.path=/alertmanager
