FROM alpine:3.19

# Install PDF processing tools directly from Alpine repositories
RUN apk add --no-cache \
    poppler-utils \
    qpdf \
    python3 \
    py3-pip \
    bash

# Install nushell from Alpine edge repository (latest versions)
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    apk add --no-cache nushell

# Create working directory
WORKDIR /pdf-tools

# Copy scripts
COPY scripts/ /pdf-tools/scripts/

CMD ["bash"]
