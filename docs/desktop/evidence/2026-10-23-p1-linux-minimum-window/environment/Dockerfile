FROM bee-linux-task6-product-probe:latest
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends libwebkit2gtk-4.1-0 libayatana-appindicator3-1 librsvg2-2 libxdo3 libgtk-3-0t64 procps git dbus-x11 xvfb xauth xdotool x11-utils imagemagick fonts-noto-cjk libfuse2t64 curl file ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --uid 1001 beeqa
USER beeqa
WORKDIR /home/beeqa
