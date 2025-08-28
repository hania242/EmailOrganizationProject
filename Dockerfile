FROM n8nio/n8n:latest

# Set environment variables
ENV NODE_ENV=production
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV N8N_USER_FOLDER=/home/node/.n8n
ENV EXECUTIONS_MODE=regular

# Optional: Add basic auth for security
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=Hania
ENV N8N_BASIC_AUTH_PASSWORD=HaniaPassedBy123

# Expose port
EXPOSE 5678