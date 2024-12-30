# Use an official OpenJDK runtime as a parent image
FROM openjdk:11-jre-slim

# Set the working directory inside the container


# Copy the JAR file into the container at /app
COPY ./target/*.jar ./myapp.jar

# Run the JAR file
ENTRYPOINT ["java", "-jar", "./myapp.jar"]
CMD [ "/usr/sbin/init" ]