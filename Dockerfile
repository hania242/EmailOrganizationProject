FROM n8nio/n8n:latest

ENV NODE_ENV=production
ENV N8N_HOST=emailorganizationproject.onrender.com
ENV N8N_PROTOCOL=https
ENV WEBHOOK_URL=https://emailorganizationproject.onrender.com
ENV N8N_USER_FOLDER=/home/node/.n8n
ENV EXECUTIONS_MODE=regular
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=Hania
ENV N8N_BASIC_AUTH_PASSWORD=HaniaPassedBy123

EXPOSE 5678