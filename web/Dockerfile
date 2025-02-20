FROM node:20-alpine

WORKDIR /app

# Install pnpm with specific version
RUN corepack enable
RUN corepack prepare pnpm@9.15.4 --activate

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy application code
COPY . .

# Build application
RUN pnpm build

# Expose port
EXPOSE 3000
ENV PORT 3000
ENV NODE_ENV production
ENV HOSTNAME "0.0.0.0"

# Start the application
CMD ["pnpm", "start"]
