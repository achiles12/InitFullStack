# ---------------------------------------------------------
# FRONTEND: React + Vite + TailwindCSS + PostCSS
# ---------------------------------------------------------
# Use lightweight Node image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm install

# Install Vite and Tailwind v4 plugin
RUN npm install -D vite tailwindcss @tailwindcss/vite

# Install React plugin for Vite
RUN npm install -D @vitejs/plugin-react


# Copy the rest of the frontend source code
COPY . .

# Expose Vite’s dev port
EXPOSE 5173

# Run Vite dev server (binds to all interfaces for Docker)
CMD ["npm", "run", "dev", "--", "--host"]
