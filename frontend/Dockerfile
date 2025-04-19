# Use Node.js to build the React app
FROM node:16 as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build --force
# The --force flag is used to bypass any warnings or errors that may occur during the build process.

# Use nginx to serve the built React app
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
