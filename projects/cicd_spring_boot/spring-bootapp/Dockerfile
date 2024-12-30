# Use OpenJDK to run the application - run time image
FROM 9902736822/java_24:latest as build

#patch the image
RUN apt-get update -y

# Set the working directory
WORKDIR /app

# Copy the built JAR file from the build stage
COPY ./target/demo-0.0.1-SNAPSHOT.jar app.jar


# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the JAR file
ENTRYPOINT ["java", "-jar", "app.jar"]
