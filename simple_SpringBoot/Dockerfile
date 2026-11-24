FROM gradle:8-jdk21

USER root
WORKDIR /app

COPY settings.gradle build.gradle ./
RUN gradle dependencies --no-daemon

COPY src ./src

EXPOSE 8080

CMD ["gradle", "bootRun", "--no-daemon"]
