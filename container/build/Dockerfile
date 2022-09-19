ARG build_base_image=gardenlinux/slim
FROM $build_base_image

ARG DEBIAN_FRONTEND=noninteractive
ARG BUILDARCH=amd64

RUN mkdir /etc/sudoers.d \
     && echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/wheel \
     && echo "deb-src https://deb.debian.org/debian testing main" >> /etc/apt/sources.list \
     && echo "#deb https://deb.debian.org/debian unstable main" >> /etc/apt/sources.list \
     && echo "#deb-src https://deb.debian.org/debian unstable main" >> /etc/apt/sources.list \
     && echo "APT::Install-Recommends false;\nAPT::Install-Suggests false;\nApt::AutoRemove::SuggestsImportant false;\n" > /etc/apt/apt.conf.d/no-recommends \
     && echo "force-confold\nforce-confdef" > /etc/dpkg/dpkg.cfg.d/forceold \
     && echo "progress=bar:force:noscroll" >> /etc/wgetrc \
     && apt-get update && apt-get install -y wget ca-certificates \
     && wget https://deb.debian.org/debian/pool/main/g/gcc-defaults/gcc_10.2.1-1_${BUILDARCH}.deb \
     && wget https://deb.debian.org/debian/pool/main/g/gcc-defaults/g++_10.2.1-1_${BUILDARCH}.deb \
     && wget https://deb.debian.org/debian/pool/main/g/gcc-defaults/cpp_10.2.1-1_${BUILDARCH}.deb \
     && if [ "${BUILDARCH}" = "amd64" ] ; then wget https://deb.debian.org/debian/pool/main/g/gcc-defaults/gcc-multilib_10.2.1-1_${BUILDARCH}.deb; fi \
     && apt-get install -y -f /*.deb \
     && rm -f /*.deb \
     && apt-mark auto gcc g++ cpp gcc-multilib \
     && dpkg -P gcc-9-base \
     && apt-get install -y build-essential fakeroot sudo gettext uuid-runtime efitools \
     && apt-get clean \
     && addgroup --system wheel \
     && adduser dev --disabled-password --gecos dev \
     && adduser dev wheel \
     && mkdir .gnupg && chmod 700 .gnupg

COPY install-cfssl.sh /setup/
RUN  /setup/install-cfssl.sh

USER dev
WORKDIR /home/dev
