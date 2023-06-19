FROM node:18-alpine  as builder

WORKDIR /usr/src/app
COPY . ./
RUN npm install
RUN npm run build


# Stage 2 - Deploy with NGNIX
FROM nginx:1.15.2-alpine

COPY --from=builder /usr/src/app/dist /var/www
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 6000

ENTRYPOINT ["nginx","-g","daemon off;"]
