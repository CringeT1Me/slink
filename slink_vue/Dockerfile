FROM node:lts-alpine

WORKDIR .

COPY package*.json ./

RUN npm install ci

COPY . .

RUN npm run build

CMD [ "npm", "run", "serve" ]
