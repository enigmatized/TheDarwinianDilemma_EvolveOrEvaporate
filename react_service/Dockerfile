# Use an official Node.js runtime as the base image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install app dependencies
RUN npm install --production

# Copy the built React app
#COPY build/ ./
COPY ./ .

# Expose the container port
EXPOSE 8021

# Start the app
CMD ["npm", "start"]
