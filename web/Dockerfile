# Define the base image as node:20 and name it as base.
FROM node:20 AS base

# Set the working directory inside the container to /app.
# We need to set the working directory so Docker knows where to run the commands.
WORKDIR /app

# Globally install the package manager pnpm.
RUN npm i -g pnpm

# Copy the package.json and pnpm-lock.yaml files to the working directory in the container.
# This command is necessary for Docker to install project dependencies.
COPY package.json pnpm-lock.yaml ./

# Install project dependencies using pnpm.
RUN pnpm install

# Copy all files from the context directory (where the Dockerfile is located) to the working directory in the container.
COPY . .

# Run the project build command using pnpm.
RUN pnpm build

# Define a second stage of the image based on node:20-alpine3.19 and name it as release.
# Alpine image is a lighter version of node, which helps reduce the final image size.
FROM node:20-alpine3.19 AS release

# Set the working directory inside the container to /app.
WORKDIR /app

# Globally install the package manager pnpm.
RUN npm i -g pnpm

# Copy the node_modules folder from the base stage to the node_modules directory in the release stage.
COPY --from=base /app/node_modules ./node_modules

# Copy the package.json file from the base stage to the current directory in the release stage.
COPY --from=base /app/package.json ./package.json

# Copy the .next folder from the base stage to the .next directory in the release stage.
COPY --from=base /app/.next ./.next

COPY --from=base /app/public ./public

# Define the default command to be executed when the container is started with pnpm start.
CMD ["pnpm", "start"]