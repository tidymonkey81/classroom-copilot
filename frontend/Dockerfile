FROM node:latest
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
EXPOSE 9501
CMD ["npm", "run", "start"]