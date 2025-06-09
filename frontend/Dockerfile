FROM nginx:alpine

# Elimina el archivo de configuración por defecto de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia tu archivo de configuración de Nginx personalizado
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia el index.html y la carpeta static desde el contexto de construcción (frontend/)
COPY index.html /usr/share/nginx/html/index.html
COPY static /usr/share/nginx/html/static