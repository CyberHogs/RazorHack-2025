FROM alpine:3.20
RUN apk add --no-cache python3 socat
WORKDIR /app
COPY flag.txt /app/flag.txt
COPY luck /app/luck
COPY start.sh /app/start.sh
RUN chmod +x /app/luck /app/start.sh
# Run as non-root; only use ports >=1024
USER nobody
ENV PORTS=11001,11002,11003,11004,11005,11006,11007,11008,11009,11011,11011,11012,11013,11014,11015,11016,11017,11018,11019,11020,11021,11022,11023,11024,11025,11026,11027,11028,11029,11030,11031,11032,11033,11034
EXPOSE 11001-11034
CMD ["/app/start.sh"]
