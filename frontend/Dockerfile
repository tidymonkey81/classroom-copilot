FROM node:latest
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . 8501
CMD ["npm", "run", "start"]