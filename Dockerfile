# Use a stable Node.js base image (n8n runs on Node)
FROM node:18-alpine

# Install n8n globally
RUN npm install -g n8n

# Set working directory
WORKDIR /home/node/.n8n
# Set environment variables
ENV NODE_ENV=production
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=http

# Optional: Add basic auth for security
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=Hania
ENV N8N_BASIC_AUTH_PASSWORD=HaniaPassedBy123

# Expose port
EXPOSE 5678

# Start n8n
CMD ["n8n", "start"]