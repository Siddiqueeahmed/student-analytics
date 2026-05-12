FROM node:20-slim

WORKDIR /app

# Copy manifest first for layer caching
COPY frontend/package.json .
RUN npm install

COPY frontend/ .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
