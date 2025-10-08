FROM node:20-alpine 
 
WORKDIR /app 
 
COPY package*.json ./ 
 
RUN npm install -g vite && npm install -D tailwindcss postcss autoprefixer && npm install 
 
COPY . . 
 
EXPOSE 3000 
 
CMD ["npm", "run", "dev"]