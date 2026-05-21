ARG IMAGESRC
FROM $IMAGESRC

# The base image sets a non-root USER; switch back to root for setup.
USER root

ARG USER=user
ARG UID=1000
ARG GID=1000

# Add the current user so that files written inside the container are
# owned by the right UID/GID when the workspace is a host-mounted volume.
RUN set -x \
 && groupadd -g $GID $USER \
 && useradd -g $GID -u $UID -d /home/$USER -m $USER \
 && printf "$USER ALL= NOPASSWD: ALL\\n" >> /etc/sudoers

# Generate a MUNGE key so the broker can start.  The base image has
# munge installed but no key present.
RUN mkdir -p /var/run/munge \
 && dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key \
 && chown -R munge /etc/munge/munge.key /var/run/munge \
 && chmod 600 /etc/munge/munge.key

COPY entrypoint.sh /usr/local/sbin/
RUN chmod +x /usr/local/sbin/entrypoint.sh

USER $USER
WORKDIR /home/$USER
ENTRYPOINT ["/usr/local/sbin/entrypoint.sh"]
