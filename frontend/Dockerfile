FROM node:20-alpine

WORKDIR /frontend

# Install dependencies first for better caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy application code
COPY . .

EXPOSE 5173

# Run Vite dev server exposed on all interfaces
CMD ["npm", "run", "dev", "--", "--host"]