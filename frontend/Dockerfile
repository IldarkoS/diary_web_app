FROM node:lts-alpine

WORKDIR /src/

ENV PATH /node_modules/.bin:$PATH

COPY package.json /package.json
RUN npm install
# RUN npm install react-scripts@1.1.1 -g --silent

COPY . ./

RUN npm run build

# start app
CMD ["npm", "run", "dev"]